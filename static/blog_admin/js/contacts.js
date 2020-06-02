

jQuery(document).ready(function($) {
    
    // 点击增加人员
    $("#add_member").on('click', function(ep) {
        
        var member_id = $(this).data('member-id');
        var csrf = $(this).data('csrf');
        var contact_id = $(this).data('contact-id');
        var URL = $(this).data('ajax-url');
        // alert(member_id+csrf)
        // alert(contact_id)
        $.ajax({
            type: 'POST',
            url: URL,
            data: {
                'member_id': member_id,
                'contact_id': contact_id,
                'csrfmiddlewaretoken': csrf
            },

            dataType: 'json',
            success: function(ret) {
                alert(ret.msg);
                window.location.reload();
            },
            error: function(ret) {
                alert(ret.msg);
            }
        }); 
    });
    // 点击从通讯录删除人员
    $("#del_member").on('click', function(e) {

        var member_id = $(this).data('member-id');
        var csrf = $(this).data('csrf');
        var contact_id = $(this).data('contact-id');
        var URL = $(this).data('ajax-url');
        // alert(member_id+csrf)
        // alert(contact_id)
        $.ajax({
            type: 'POST',
            url: URL,
            data: {
                'member_id': member_id,
                'contact_id': contact_id,
                'csrfmiddlewaretoken': csrf
            },

            dataType: 'json',
            success: function(ret) {
                alert(ret.msg);
                window.location.reload();
            },
            error: function(ret) {
                alert(ret.msg);
            }
        }); 
    });
     // 点击从通讯录查找人员
    $("#search_member_submit").on('click', function(e) {
        var member_id = $("#search_member_id").val();
        var member_name= $("#search_member_name").val();
        var csrf = $(this).data('csrf');
        var URL = $(this).data('ajax-url');
        if (member_id==""||member_name==""){
            // alert("");
            $("#danger_info").css("display","block");
            $("#danger_info").find("span").eq(1).html("id和姓名不能为空！兄嘚");

            return;
        }

        // alert(member_id+csrf)
        // alert(member_id)
        $.ajax({
            type: 'POST',
            url: URL,
            data: {
                'member_id': member_id,
                'member_name': member_name,
                'csrfmiddlewaretoken': csrf
            },

            dataType: 'json',
            success: function(ret) {
                for (var i = $("#all_user").find(".id").length - 1; i >= 0; i--) {
                    if ($("#all_user").find(".id").eq(i).html() == ret.msg) {
                        $("#all_user").find(".id").eq(i).css("background-color","rgb(210,236,218)");
                            $("#success_info").css("display","block");
                            $("#success_info").find("span").eq(1).html('他绿了');
                    }

                }
                
                // alert(ret.msg);
            },
            error: function(ret) {
                $("#danger_info").css("display","block");
                $("#danger_info").find("span").eq(1).html('搞错了吧 没得这个人');
                
            }
        }); 
    });

})