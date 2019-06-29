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
            $("#eskimo-gototop").css('bottom', '40px');
        } else {
            $("#eskimo-gototop").css('bottom', '-40px');
        }
    });
    
    $("#eskimo-gototop").on('click', function (e) {
        e.preventDefault();
        $("html, body").animate({
            scrollTop: 0
        }, 500);
        return false;
    });
    
    /* FULLSCREEN SEARCH */
    $("#eskimo-open-search").on('click', function (e) {
        e.preventDefault();
        $("#eskimo-fullscreen-search").fadeIn(200);
    });
    
    $("#eskimo-close-search").on('click', function (e) {
        e.preventDefault();
        $("#eskimo-fullscreen-search").fadeOut(200);
    });
    /* MAIN MENU */
    $('#eskimo-main-menu').find(".eskimo-menu-ul > li > a").on('click', function () {
        var nxtLink = $(this).next();
        if ((nxtLink.is('ul')) && (nxtLink.is(':visible'))) {
            nxtLink.slideUp(300);
            $(this).removeClass("eskimo-menu-up").addClass("eskimo-menu-down");
        }
        if ((nxtLink.is('ul')) && (!nxtLink.is(':visible'))) {
            $('#eskimo-main-menu').find('.eskimo-menu-ul > li > ul:visible').slideUp(300);
            nxtLink.slideDown(300);
            $('#eskimo-main-menu').find('.eskimo-menu-ul > li:has(ul) > a').removeClass("eskimo-menu-up").addClass("eskimo-menu-down");
            $(this).addClass("eskimo-menu-up");
        }
        if (nxtLink.is('ul')) {
            return false;
        } else {
            return true;
        }
    });
    
    /* MOBILE MENU */
    $("#eskimo-menu-toggle").on('click', function () {
        $("#eskimo-social-cell,#eskimo-main-menu").toggle();
    });
    /* EVENTS */
    $(document).ready(function () {
        // adjustPageTitle();
        cardImages();
        $('#eskimo-main-menu').find('.eskimo-menu-ul > li:has(ul) > a').addClass("eskimo-menu-down");
        $('body').find('select').addClass('custom-select');
        $('body').find('.eskimo-masonry-grid').css('opacity', '1');
    });
    
    $(window).on('resize orientationchange', function () {
        // adjustPageTitle();
        var ww = document.body.clientWidth;
        if (ww < 1200) {
            $("#eskimo-social-cell,#eskimo-main-menu").hide();
        } else {
            $("#eskimo-social-cell,#eskimo-main-menu").show();
        }
    });
    
})(jQuery);

