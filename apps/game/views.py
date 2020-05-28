from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "index.html")


def game(request):
    return render(request, "game_dir.html")


def snake(request):
    return render(request, "snake.html")


def street_fighter(request):
    return render(request, "StreetFighter.html")


def minesweeper(request):
    return render(request, "Minesweeper.html")


def study(request):
    return render(request, "Study.html")
