import cherrypy
import sys
import time
from pyspark import SparkContext, SparkConf
import logging
import pandas as pd
import os
apps_floder = os.path.dirname(__file__)
ML_1M_RATINGS_FILE = os.path.join(apps_floder, 'ml-1m\\ratings.csv')
BX_CSV_DUMP_FLODER = os.path.join(apps_floder, 'BX-CSV-Dump')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# IMPORTANT: pass aditional Python modules to each worker
_sparkcontext = SparkContext(conf=SparkConf().setAppName(
    "django_react"))


def test():
    # Load ratings data for later use
    logger.info("Loading Ratings data...")
    ratings_raw_RDD = _sparkcontext.textFile(os.path.join(BX_CSV_DUMP_FLODER, 'BX-Book-Ratings.csv'))
    ratings_raw_data_header = ratings_raw_RDD.take(1)[0]
    ratings_RDD = ratings_raw_RDD.filter(lambda line: line!=ratings_raw_data_header)\
        .map(lambda line: line.split(";"))\
        .map(lambda tokens: (int(tokens[0][1:-1]), abs(hash(tokens[1][1:-1])) % (10 ** 8), int(tokens[2][1:-1]))).cache()
    # Load books data for later use
    logger.info("Loading Books data...")
    books_raw_RDD = _sparkcontext.textFile(os.path.join(BX_CSV_DUMP_FLODER, 'BX-Books.csv'))
    books_raw_data_header = books_raw_RDD.take(1)[0]
    books_RDD = books_raw_RDD.filter(lambda line: line!=books_raw_data_header)\
        .map(lambda line: line.split(";"))\
        .map(lambda tokens: (abs(hash(tokens[0][1:-1])) % (10 ** 8), tokens[1][1:-1], tokens[2][1:-1], tokens[3][1:-1], tokens[4][1:-1], tokens[5][1:-1])).cache()
    books_titles_RDD = books_RDD.map(lambda x: (int(x[0]), x[1], x[2], x[3], x[4], x[5])).cache()
    
    
    # Pre-calculate books ratings counts
    """Updates the books ratings counts from 
    the current data self.ratings_RDD
    """
    logger.info("Counting book ratings...")
    book_ID_with_ratings_RDD = ratings_RDD.map(lambda x: (x[1], x[2])).groupByKey()
    def get_counts_and_averages(ID_and_ratings_tuple):
        """Given a tuple (bookID, ratings_iterable) 
        returns (bookID, (ratings_count, ratings_avg))
        """
        nratings = len(ID_and_ratings_tuple[1])
        return ID_and_ratings_tuple[0], (nratings, float(sum(x for x in ID_and_ratings_tuple[1]))/nratings)
    book_ID_with_avg_ratings_RDD = book_ID_with_ratings_RDD.map(get_counts_and_averages)
    books_rating_counts_RDD = book_ID_with_avg_ratings_RDD.map(lambda x: (x[0], x[1][0]))

    
    # Train the model
    rank = 16
    seed = 5
    iterations = 10
    regularization_parameter = 0.1
    """Train the ALS model with the current dataset
    """
    logger.info("Training the ALS model...")
    
    from pyspark.mllib.recommendation import ALS
    model = ALS.train(ratings_RDD, rank, seed=seed,
                            iterations=iterations, lambda_=regularization_parameter)
    logger.info("ALS model built!")
    
    """Recommends up to books_count top unrated books to user_id
    """
    # Get pairs of (userID, bookID) for user_id unrated books
    user_id = 100
    books_count = 10
    user_unrated_books_RDD = ratings_RDD.filter(lambda rating: not rating[0] == user_id)\
                                                .map(lambda x: (user_id, x[1])).distinct()
    # Get predicted ratings
    
    predicted_RDD = model.predictAll(user_unrated_books_RDD)
    predicted_rating_RDD = predicted_RDD.map(lambda x: (x.product, x.rating))
    predicted_rating_title_and_count_RDD = \
        predicted_rating_RDD.join(books_titles_RDD.map(lambda x: (x[0], (x[1], x[2], x[3], x[4], x[5])))).join(books_rating_counts_RDD)
    predicted_rating_title_and_count_RDD = \
        predicted_rating_title_and_count_RDD.map(lambda r: (r[1][0][1][0], r[1][0][0], r[1][1], r[1][0][1][1], r[1][0][1][2], r[1][0][1][3], r[1][0][1][4]))
    ratings = predicted_rating_title_and_count_RDD.filter(lambda r: r[2]>=25).takeOrdered(books_count, key=lambda x: -x[1])
    print(ratings)


def get_ml_1m_ratings_df():
    ratings_df = pd.read_csv(ML_1M_RATINGS_FILE, sep=',', engine='python')
    return ratings_df
if __name__ == "__main__":
    test()