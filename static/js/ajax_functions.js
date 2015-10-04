$(document).ready(function(){
    body = $('body');
    $('#send_request').click(function(){
        var username;
        username = $(this).attr("data-username");
        $.get('/send_request/', {'username':username}, function(data){
            $('#send_request').hide()

            $('#friend_field').append($('<button id=\'cancel_request\' class=\'btn btn-mini btn-secondary\' type=\'button\' data-username=\'' +
                username + '\'>Cancel request</button>'));
        });
    });
     $('#cancel_request').click(function(){
    //body.on('click', '#follow_btn', function(e) {
        var username;
        username = $(this).attr("data-username");
        $.get('/cancel_request/', {'username':username}, function(data){
            $('#cancel_request').hide()

            $('#friend_field').append($('<button id=\'send_request\' class=\'btn btn-mini btn-primary\' type=\'button\' data-username=\'' +
                username + '\'>Send request</button>'));
        });
    });

    body.on('click', '#follow_btn', function(e) {
        var pk = $(this).attr('data-user-pk');
        $.get('/follow/', {'pk':pk}, function(data){
            $('#follow_btn').hide();
            $('#user_menu').prepend($('<button id=\'unfollow_btn\' class=\'btn btn-default\' type=\'button\' data-user-pk=\'' +
                pk + '\'>Unfollow</button>'));
            $('#followers_btn').val()
        });
    });

    body.on('click', '#unfollow_btn', function(e) {
        var pk = $(this).attr('data-user-pk');
        $.get('/unfollow/', {'pk':pk}, function(data){
            $('#unfollow_btn').hide();
            $('#user_menu').prepend($('<button id=\'follow_btn\' class=\'btn btn-primary\' type=\'button\' data-user-pk=\'' +
                pk + '\'>Follow</button>'));
        });
    });

    body.on('mouseover', '.post', function(e) {
        $(this).find('.edit_post').stop().fadeIn('fast');
    });
    body.on('mouseout', '.post', function(e) {
        $(this).find('.edit_post').stop().fadeOut('fast');
    });
    function delete_comment() {
         var comment;
        comment = $(this).attr("data-comment_id");
         var button = $(this);
         $.get('/manage_comment/', {'comment_id':comment, 'action':'delete'}, function(data){
            button.parent().slideUp()
         });
    }
    function edit_comment() {
          var comment;
        comment = $(this).attr("data-comment_id");
        var field = $(this).parent().children('.edit_comment_field');
         var text = $(this).parent().children('.comment_text');
         if (field.is(':visible')) {
                $.get('/manage_comment/', {'comment_id':comment, 'edited_text':field.val(), 'action':'edit'}, function(data){
                field.hide();
                text.text(field.val())
                text.show()

            })
         } else {
             field.show();
             text.hide();
             field.val(text.text());
         }
    }
     $('.edit_comment').click(edit_comment)
     $('.delete_comment').click(delete_comment)

     $('.delete_post').click(function(e){
        var post_pk;
        post_pk = $(this).attr("data-post_pk");
         $.get('/manage_post/', {'pk':post_pk, 'action':'delete'}, function(data){
            $('#post_' + post_pk).parent().hide();
         });
     });
    $('#delete_post').click(function(e) {//on the Manage post page
        var post_pk;
        post_pk = $(this).attr("data-post_pk");
         $.get('/manage_post/', {'pk':post_pk, 'action':'delete'}, function(data){
            window.location = "/profile/";
         });
    });
    $('.add_comment').click(function(e){
        var comment_text = $(this).parent().parent().children('.comment_text');
        var post_id = $(this).attr("data-post_id");

        $.get('/manage_comment/', {'post_id':post_id, 'text': comment_text.val(), 'action': 'add'}, function(data){

            obj = $.parseJSON(data)[0]['fields'];
            comment_id = $.parseJSON(data)[0].pk;
            var datetime = new Date(obj.timestamp)
            var datetimeString = (new Date(datetime.getTime() + datetime.getTimezoneOffset())).format("dd mmm, yyyy, h:MM tt")

            $('#comments_'+post_id).append(
                "<div class='comment' id='comment_"+comment_id+"'>" +
                    "<a href='/profile/"+obj.user+"'><img src='/media/avatars/"+ obj.user + "_small.jpg' />" +
                    obj.first_name + " " + obj.last_name + "</a>" +
                    "<div class='comment_text'>" + obj.text + "</div>" +
                    "<p class='timestamp'>" + datetimeString + "</p>" +
                    "<textarea cols='40' class='edit_comment_field' name='text input-group' id='styled' rows='1' " +
                    "style='display:none'></textarea><button data-comment_id='"+comment_id+"' class='edit_comment btn btn-default btn-xs' " +
                    "type='button'>edit</button><button data-comment_id='"+comment_id+"' class='delete_comment btn btn-default btn-xs' " +
                    "type='button'>x</button></div>");

            $('#comment_'+comment_id).hide().slideDown();
            });


            $(document).on("click", ".edit_comment", edit_comment)
            $(document).on("click", ".delete_comment", delete_comment)
            comment_text.val("")
        });
    $('#send_message').click(function(e) {
       var text = $('#message_text').val();
        var pk = $(this).attr('data-user');
        var button = $(this);
        button.attr("disabled", true);
        $.get('/send_message/', {'pk': pk, 'text':text}, function(data){
            window.location.replace('/inbox')
        });
    });
    $('#register_form').submit(function(e) {
       var email_input = $('#email_input');
        var button = $(this);
        var code = 1;
        if (email_input.parsley().isValid() === false) {
            return;
        }
        window.ParsleyUI.removeError(email_input.parsley(), "email_exists");
        e.preventDefault();


        $.get('/api/check_email/', {'email': email_input.val()}, function(data){
        }).always(function (jqxhr) {
            var field = email_input.parsley();
            if (jqxhr.status == 800) {
                window.ParsleyUI.addError(field, "email_exists",  "This email is already registered")

            } else {
                window.ParsleyUI.removeError(field, "email_exists");
                button.unbind('submit').submit();
            }

        });
    });
    $('#email_input').keyup(function() {
        window.ParsleyUI.removeError($(this).parsley(), "email_exists");

    });


});

