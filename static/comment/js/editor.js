$(function() {
	var text = "";
	 
//    点击回复
	$(".rep-btn").click(function(){
	    
	    var u = $(this).data('repuser')
	    var i = $(this).data('repid')
	    sessionStorage.setItem('rep_id',i);
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

//    点击提交评论
    $("#push-test-com").click(function(e) {
    	// 获取评论的内容
    	var content_all = document.getElementById("test-editormd").getElementsByTagName("pre");
		for(var i=0; i<content_all.length;i++){
			var x =content_all[i].innerText;
			text = x+"<br/>" +text;
		}
        var content = text;
        if (content.length == 0) {
            alert("评论内容不能为空！");
            return;
        }
        var base_t = sessionStorage.getItem('base_t');
        var now_t = Date.parse(new Date());
        if (base_t) {
            var tt = now_t - base_t;
            // if (tt < 40000) {
            //     alert('两次评论时间间隔必须大于40秒，还需等待' + (40 - parseInt(tt / 1000)) + '秒');
            //     return;
            // } else {
            //     sessionStorage.setItem('base_t', now_t);
            // }
            sessionStorage.setItem('base_t', now_t);
        } else {
            sessionStorage.setItem('base_t', now_t)
        };
        var csrf = $(this).data('csrf');
        var article_id = $(this).data('article-id');
        var URL = $(this).data('ajax-url');
        var rep_id = sessionStorage.getItem('rep_id');
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
                'content': text,
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

//    提交评论后定位到新评论处
    if(sessionStorage.getItem('new_point')){
        var top = $(sessionStorage.getItem('new_point')).offset().top-100;
        $('body,html').animate({scrollTop:top}, 200);
        window.location.hash = sessionStorage.getItem('new_point');
        sessionStorage.removeItem('new_point');
    };
    sessionStorage.removeItem('rep_id');

    $(".comment-body a").attr("target","_blank");
})