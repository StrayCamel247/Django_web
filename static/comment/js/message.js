$(function() {
//    点击回复
	$(".rep-btn").click(function(){
	    var u = $(this).data('repuser')
	    var i = $(this).data('repid')
        sessionStorage.setItem('rep_id', i);
	    $("#rep-to").text("回复 @"+u).removeClass('hidden');
        $("#no-rep").removeClass('hidden');
		$(".rep-btn").css("color", "#868e96");
		$(this).css("color", "red");
		$('html, body').animate({
			scrollTop: $($.attr(this, 'href')).offset().top - 55
		}, 500);
	});

//    点击取消回复
	$("#no-rep").click(function(){
	    
	    sessionStorage.removeItem('rep_id');
	    $("#rep-to").text('').addClass('hidden');
		$("#no-rep").addClass('hidden');
		$(".rep-btn").css("color", "#868e96");
	});

//    点击提交留言
    $("#push-message").click(function(e) {
        // 获取留言的内容
        var content = $("#mdeditor").val();
        
        if (content.length == 0) {
            alert("留言内容不能为空！");
            return;
        }
        var base_t = sessionStorage.getItem('base_t');
        var now_t = Date.parse(new Date());
        if (base_t) {
            var tt = now_t - base_t;
            // if (tt < 40000) {
            //     alert('两次留言时间间隔必须大于40秒，还需等待' + (40 - parseInt(tt / 1000)) + '秒');
            //     return;
            // } else {
            //     sessionStorage.setItem('base_t', now_t);
            // }
            sessionStorage.setItem('base_t', now_t);
        } else {
            sessionStorage.setItem('base_t', now_t)
        };
        var csrf = $(this).data('csrf');
        var URL = $(this).data('ajax-url');
        var rep_id = sessionStorage.getItem('rep_id');
        var article_id = $(this).data('article-id');
        $.ajaxSetup({
            data: {
                'csrfmiddlewaretoken': csrf
            }
        });
        $.ajax({
            type: 'post',
            url: URL,
            data: {
                'rep_id': rep_id,
                'content': content,
                'article_id': article_id
            },

            dataType: 'json',
            success: function(ret) {
                sessionStorage.removeItem('rep_id');
                sessionStorage.setItem('new_point', ret.new_point);
                window.location.reload();
            },
            error: function(ret) {
                alert(ret.msg);
            }
        });
    });
//    点击撤回评论
    $(".del-message").click(function(e) {
        var csrf = $(this).data('csrf');
        var URL = $(this).data('ajax-url');
        var mes_id = $(this).data('mes-id');
        var article_id = $(this).data('article-id');
        console.log(article_id)
        $.ajaxSetup({
            data: {
                'csrfmiddlewaretoken': csrf
            }
        });
        $.ajax({
            type: 'post',
            url: URL,
            data: {
                'mes_id': mes_id,
                'article_id': article_id
            },

            dataType: 'json',
            success: function(ret) {
                $('html, body').animate({
                    scrollTop: $("#mdeditor").offset().top - 55
                }, 500);
            },
            error: function(ret) {
                alert(ret.msg);
            }
        });
    });
//    提交留言后定位到新留言处
    if (sessionStorage.getItem('new_point')) {
        console.log(sessionStorage.getItem('new_point'))
        // $('body,html').animate({scrollTop: $(sessionStorage.getItem('new_point')).offset().top}, 500);
        window.location.hash = sessionStorage.getItem('new_point');
        sessionStorage.removeItem('new_point');
    };
    sessionStorage.removeItem('rep_id');


    
})