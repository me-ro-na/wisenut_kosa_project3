// 모달에 넘길 데이터
function start_chat() {
    let query = "";
    // send(query)
    $('#send-button').on('click', function(){
        query = ($('#my-message').val());
        if(query == "quit") {
            $('.chat-body').append('<div class="chat-info">종료를 원하시면 종료 버튼을 눌러주세요</div>');
            $('#my-message').val('');
            return false;
        } else if(!query) {
            $('.chat-body').append('<div class="chat-info">입력되지 않았습니다.</div>');
            $('#my-message').val('');
            return false;
        }
        send(query)
        $('#my-message').val('');
        $('.chat-body').append('<div class="chat-bubble me">' + query + '</div>');
        // load = $("#loading").clone();
        // $('.chat-body').append(load);
        // load.removeClass("hide");
    });
    $('.end-chat').click(function () {
        send("quit");
        $('.chat-body').addClass('hide');
        $('.chat-input').addClass('hide');
        $('.chat-session-end').removeClass('hide');
        $('.chat-header-option').addClass('hide');
    });
}

function send(query) {
    $.ajax({
        url: "/server",
        type: "post",
        data: {"query": query},
        success: function(data) {
            if(data){
                answer = data.Answer;
                $('.chat-body').append('<div class="chat-bubble you">' + answer + '</div>');
            }
        },
        error: function(request,status,error){
            // console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            console.log(request.responseText);
            // console.log("code:"+request.status+"\n"+"message:"+"\n"+"error:"+error);
        }
    });
    return false;
}