(function ($) {
    "use strict";

    // window.onload =function(){
    //     var progress = document.getElementById("category_progress").style.width; 
    //     $('#category_progress').val(progress);
    // }
    /* HORIZONTAL CARD IMAGES */
    var cardImages = function () {
        $('body').find(".card-featured-img").each(function () {
            if ($(this).attr('data-img')) {
                var card_img = $(this).data('img');
                $(this).css('background-image', 'url("' + card_img + '")');
            }
        });
    };
    /* NAV ICON*/
    $("#nav-icon").on('click', function(e) {
        // $(this).removeClass("open");
        if ($(this).hasClass("open")){
             $(this).removeClass("open");
        }
        else{
            $(this).addClass("open");
        }
    });
    /* GO TO TOP BUTTON */
    $(window).on('scroll', function () {
        if ($(this).scrollTop() > 300) {
            $("#freen-gototop").css('bottom', '40px');
        } else {
            $("#freen-gototop").css('bottom', '-40px');
        }
    });
    
    $("#freen-gototop").on('click', function (e) {
        e.preventDefault();
        $("html, body").animate({
            scrollTop: 0
        }, 500);
        return false;
    });
    
    /* FULLSCREEN SEARCH */
    $("#freen-open-search").on('click', function (e) {
        e.preventDefault();
        $("#freen-fullscreen-search").fadeIn(200);
    });
    
    $("#freen-close-search").on('click', function (e) {
        e.preventDefault();
        $("#freen-fullscreen-search").fadeOut(200);
    });
    /* MAIN MENU */
    $('#freen-main-menu').find(".freen-menu-ul > li > a").on('click', function () {
        var nxtLink = $(this).next();
        if ((nxtLink.is('ul')) && (nxtLink.is(':visible'))) {
            nxtLink.slideUp(300);
            $(this).removeClass("freen-menu-up").addClass("freen-menu-down");
        }
        if ((nxtLink.is('ul')) && (!nxtLink.is(':visible'))) {
            $('#freen-main-menu').find('.freen-menu-ul > li > ul:visible').slideUp(300);
            nxtLink.slideDown(300);
            $('#freen-main-menu').find('.freen-menu-ul > li:has(ul) > a').removeClass("freen-menu-up").addClass("freen-menu-down");
            $(this).addClass("freen-menu-up");
        }
        if (nxtLink.is('ul')) {
            return false;
        } else {
            return true;
        }
    });
    
    /* MOBILE MENU */
    $("#freen-menu-toggle").on('click', function () {
        $("#freen-social-cell,#freen-main-menu").toggle();
    });
    /* EVENTS */
    $(document).ready(function () {
        // adjustPageTitle();
        cardImages();
        $('#freen-main-menu').find('.freen-menu-ul > li:has(ul) > a').addClass("freen-menu-down");
        $('body').find('select').addClass('custom-select');
        $('body').find('.freen-masonry-grid').css('opacity', '1');
    });
    
    $(window).on('resize orientationchange', function () {
        // adjustPageTitle();
        var ww = document.body.clientWidth;
        if (ww < 1200) {
            $("#freen-social-cell,#freen-main-menu").hide();
        } else {
            $("#freen-social-cell,#freen-main-menu").show();
        }
    });
    
})(jQuery);

