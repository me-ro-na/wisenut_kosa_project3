function start_chat() {
    $('#my-message').focus();
    $('#send-button').on('click', function(){
        send_message()
        $('#my-message').focus();
    });
    $(".chat-input").keypress(function(e){
        if(e.keyCode === 13) {
            $('#my-message').focus();
            send_message()
        }
    })
    $('.end-chat').click(function () {
        send("quit");
        $('.chat-body').addClass('hide');
        $('.chat-input').addClass('hide');
        $('.chat-session-end').removeClass('hide');
        $('.chat-header-option').addClass('hide');
    })
}

function send_message() {
    let query = "";
    query = ($('#my-message').val());
    if(query == "quit") {
        $('.chat-body').append('<div class="chat-info">종료를 원하시면 종료 버튼을 눌러주세요</div>');
        $('#my-message').val('');
        return false;
    } else if(!query) {
        return false;
    }
    send(query)
    $('#my-message').val('');
    $('.chat-body').append('<div class="chat-bubble me">' + query + '</div>');
};

function send(query) {
    $.ajax({
        url: "/start_jobabot",
        type: "post",
        data: {"query": query},
        success: function(data) {
            if(data){
                answer = data.Answer;
                for(let i=0; i<answer.length; i++) {
                    $('.chat-body').append('<div class="chat-bubble you">' + answer[i] + '</div>');
                }
            }
            $(".chat-body").scrollTop($(".chat-body")[0].scrollHeight);
        },
        error: function(request,status,error){
            $('.chat-body').append('<div class="chat-bubble you">죄송합니다. 접속이 원할하지 않습니다.</div>');
            // console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            // console.log(request.responseText);
            console.log("code:"+request.status+"\n"+"message:"+"\n"+"error:"+error);
        }
    });
    return false;
}