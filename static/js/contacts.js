$(function() {
	var text = "";

	// 点击从通讯录删除人员
    $("#del_member").click(function(e) {

  		var member_id = $(this).data('member-id');
        var csrf = $(this).data('csrf');
        var contact_id = $(this).data('contact-id');
        var URL = $(this).data('ajax-url');
        $.ajaxSetup({
            data: {
                'csrfmiddlewaretoken': csrf
            }
        });
        $.ajax({
            type: 'post',
            url: URL,
            data: {
                'member_id': member_id,
                'contact_id': contact_idd
            },

            dataType: 'json',
            success: function(ret) {
                alert("!")
            },
            error: function(ret) {
                alert(ret.msg);
            }
        });
    });

})