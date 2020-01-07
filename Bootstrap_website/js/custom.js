(function ($) {
    "use strict";
    
    /* CALCULATE PAGE TITLE NEGATIVE MARGIN */
    var adjustPageTitle = function () {
        var distance = $('#eskimo-main-container > .container').offset().left - 295;
        $('#eskimo-main-container').find('.eskimo-page-title').css('margin-right', -distance);
        $('#eskimo-main-container').find('.eskimo-page-title').css('padding-right', distance);
        $('#eskimo-main-container').find('.eskimo-page-title').css('opacity', 1);
    };

    /* HORIZONTAL CARD IMAGES */
    var cardImages = function () {
        $('body').find(".card-horizontal-right").each(function () {
            if ($(this).attr('data-img')) {
                var card_img = $(this).data('img');
                $(this).css('background-image', 'url("' + card_img + '")');
            }
        });
    };
    
    /* GO TO TOP BUTTON */
    $(window).on('scroll', function () {
        if ($(this).scrollTop() > 300) {
            $("#eskimo-gototop").css('bottom', 0);
        } else {
            $("#eskimo-gototop").css('bottom', '-50px');
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
        adjustPageTitle();
        cardImages();
        $('#eskimo-main-menu').find('.eskimo-menu-ul > li:has(ul) > a').addClass("eskimo-menu-down");
        $('body').find('select').addClass('custom-select');
        $('body').find('.eskimo-masonry-grid').css('opacity', '1');
    });
    
    $(window).on('resize orientationchange', function () {
        adjustPageTitle();
        var ww = document.body.clientWidth;
        if (ww < 1200) {
            $("#eskimo-social-cell,#eskimo-main-menu").hide();
        } else {
            $("#eskimo-social-cell,#eskimo-main-menu").show();
        }
    });
    
})(jQuery);