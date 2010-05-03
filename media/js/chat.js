var chat = {
    
    options: {
        message_length: 140
    },
    
    ele: false,

    loading: {
        users: false,
        chat: false,
        send: false
    },
    user: username,
    state: 0,
    userid: 0,
    
    updateUserlist: function(user) {
        if (chat.loading.users) return false;
        chat.loading.users = true;
        $.ajax({
            url: url_updateUserList,
            data: {
                'userid': chat.userid
            },
            dataType: 'json',
            type: 'POST',
            success: function (data) {
                if (data.error) {
                    chat.loading.users = true;
                    chat.loading.chat = true;
                    chat.loading.send = true;
                    chat.ele.timeout.fadeIn('fast');
                }
                chat.ele.errors.html('');
                chat.ele.userlist.html('');
                for (var i in data) {
                    chat.ele.userlist.append('<li>' + data[i].fields.name + '</li>');
                    i++;
                }
            },
            error: function (req, err) {
            
            },
            complete: function (req, stat) {
                chat.loading.users = false;
                setTimeout('chat.updateUserlist(chat.user)', 10000);
            }
        });
    },
    
    updateChat: function() {
        if (chat.loading.chat) return false;
        chat.loading.chat = true;
        $.ajax({
            url: url_updateChat,
            data: {
                'state': chat.state,
            },
            dataType: 'json',
            type: 'POST',
            success: function (data) {
				var myself = '';
                chat.ele.errors.html('');
                for (var i in data) {
					if (data[i].chatter == username) { myself = 'myself'; } else { myself = ''; }
                    chat.ele.chatarea.append('<li class="' + myself + '"><span class="username">' + data[i].chatter + '</span><span class="timestamp">{' + data[i].timestamp + '}</span><p class="text">' + data[i].message + '</p></li>');
                    chat.state = data[i].id;
                    i++;
                }
                $('p > a').attr('target', '_blank');
				if (i > 0) {
					chat.ele.chatarea.animate({
						scrollTop: chat.ele.chatarea.attr("scrollHeight") - chat.ele.chatarea.height()
					}, 1000);
				}
            },
            error: function (req, err) {
                chat.ele.errors.html(' Offline');
            },
            complete: function (req, stat) {
                chat.loading.chat = false;
                setTimeout('chat.updateChat()', 1000);
            }
        });
    },
    
    sendMessage: function(user, message) {
        if (chat.loading.send) return false;
        chat.loading.send = true;
        $.ajax({
            url: url_sendMessage,
            data: {
                'userid': chat.userid,
                'message': chat.ele.message.val()
            },
            dataType: 'text',
            type: 'POST',
            success: function (data) {
                chat.ele.errors.html('');
                chat.ele.message.val('');
            },
            error: function (req, err) {
                chat.ele.errors.html(' Please wait...');
            },
            complete: function (req, stat) {
                chat.loading.send = false;
            }
        });
    },
    
    init: function (user) {
        $.ajax({
            url: url_init,
            data: {
                'user': user
            },
            dataType: 'text',
            type: 'POST',
            success: function (data) {
                chat.ele.errors.html('');
                chat.userid = parseInt(data);
                
                chat.updateChat();
                chat.updateUserlist(chat.userid);
            },
            error: function (req, err) {
                chat.ele.errors.html(' Fatal Error!');
            },
            complete: function (req, stat) {
                
            }
        });
    }
}

$(function() {
    chat.ele = {
        errors: $('#offline'),
        message: $('textarea#messageinput'),
        userlist: $('div#userlist'),
        chatarea: $('div#chatarea'),
        timeout: $('div#timeout')
    }

    chat.ele.message.keydown(function(event) {  
        var key = event.which;  
        if (key >= 33) {
            var maxLength = $(this).attr('maxlength');  
            var length = this.value.length;
            if (length >= maxLength) {  
                event.preventDefault();  
            }  
        }
    });
    	 
    chat.ele.message.keyup(function(e) {	
        if (e.keyCode == 13) { 
            var text = $(this).val();
            var maxLength = $(this).attr('maxlength');  
            var length = text.length; 
            if (length <= maxLength + 1) {  
                chat.sendMessage(username, text);
            } else {
                $(this).val(text.substring(0, maxLength));
            }	
        }
    });

    chat.init(chat.user);
    
});
