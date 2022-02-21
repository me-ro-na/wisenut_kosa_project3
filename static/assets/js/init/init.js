$(document).ready(function(){
    //Toggle fullscreen
    $(".chat-bot-icon").click(function (e) {
        $(this).children('img').toggleClass('hide');
        $(this).children('svg').toggleClass('animate');
        $('.chat-screen').toggleClass('show-chat');
    });
    $('.chat-mail button').click(function () {
        start_chat()
        $('.chat-mail').addClass('hide');
        $('.chat-body').removeClass('hide');
        $('.chat-input').removeClass('hide');
        $('.chat-header-option').removeClass('hide');
    });

    $(document).on("click", "#lists-body>tr", function(e) {
        no = parseInt(e.currentTarget.id.split("_")[1]);
        get_modal_data(no);
    
        $('#popupModal').modal();
        // $('#popupModal').modal('hide');
    });

    let week = new Array("Sun", "Mon", "Tues", "Wednes", "Thurs", "Fri", "Satur");
    let now = new Date();
    let todayLabel = week[now.getDay()] + "day";
    let hour = now.getHours();
    let h = hour < 12 ? " AM" : " PM";
    let result = todayLabel + ", " + hour + ":" + now.getMinutes() + h;

    $(".chat-body>.chat-start").text(result);

    get_chart1();
    get_chart2();
    get_chart3();
    get_chart4();
    get_chart5();
});

function getNow() {
    let week = new Array("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat");
    let now = new Date();
    let todayLabel = week[now.getDay()] + "day";
    let hour = now.getHours();
    let h = hour < 12 ? "AM" : "PM";
    let result = todayLabel + ", " + hour + ":" + now.getMinutes() + h;

    $(".chart-body>chart-start").text(getNow());
}

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

$(function() {
    $('.job-table').DataTable({
        searching: false
        // info: false
    });
})

addr = "전체";
fors = "전체";
jobs = "전체";
$(function() {
    $('#experience_addr').on('select2:selecting', function(e) {
        addr = e.params.args.data.text;
        
        if((fors == "전체" && jobs == "전체") || (fors != "전체" && jobs != "전체")) {
            get_fors(addr, jobs);
            get_jobs(addr, fors);
        } else if(fors == "전체" && jobs != "전체"){
            get_fors(addr, jobs);
        } else if(fors != "전체" && jobs == "전체"){
            get_jobs(addr, fors);
        }
        get_result_data(addr, fors, jobs)
    });
    $('#experience_for').on('select2:selecting', function(e) {
        fors = e.params.args.data.text;
        
        if((addr == "전체" && jobs == "전체") || (addr != "전체" && jobs != "전체")) {
            get_addrs(fors, jobs);
            get_jobs(addr, fors);
        } else if(addr == "전체" && fors != "전체"){
            get_addrs(fors, jobs);
        } else if(addr != "전체" && fors == "전체"){
            get_jobs(addr, fors);
        }
        get_result_data(addr, fors, jobs)
    });
    $('#experience_job').on('select2:selecting', function(e) {
        jobs = e.params.args.data.text;
        if((addr == "전체" && fors == "전체") || (addr != "전체" && fors != "전체")) {
            get_addrs(fors, jobs);
            get_fors(addr, jobs);
        } else if(addr == "전체" && fors != "전체"){
            get_addrs(fors, jobs);
        } else if(addr != "전체" && fors == "전체"){
            get_fors(addr, jobs);
        }
        get_result_data(addr, fors, jobs)
    });
})

function get_addrs(fors, jobs) {
    $.ajax({
        url: "/get_addrs",
        type: "get",
        data: {"fors": fors, "jobs": jobs},
        success: function(data) {
            addrList = data.addrs;
            optLen = $("#experience_addr").find("option").length;

            $('#experience_addr').val(null).trigger('change');
            $('#experience_addr').html('').select2({data: [{value: '', id: '', text: '전체'}]});

            for(var i=0; i<addrList.length; i++) {
                if ($('#experience_addr').find("option[value='" + addrList[i] + "']").length) {
                    $('#experience_addr').val(addrList[i]).trigger('change');
                } else { 
                    var newOption = new Option(addrList[i], addrList[i], true, false);
                    $('#experience_addr').append(newOption).trigger('change');
                }
            }
            if(addrList.includes(addr)) {
                $('#experience_addr').val(addr).trigger('change');
            }
        }
    });
}

function get_fors(addr, jobs) {
    $.ajax({
        url: "/get_fors",
        type: "get",
        data: {"addr": addr, "jobs": jobs},
        success: function(data) {
            forList = data.fors;
            optLen = $("#experience_for").find("option").length;

            $('#experience_for').val(null).trigger('change');
            $('#experience_for').html('').select2({data: [{value: '', id: '', text: '전체'}]});

            for(var i=0; i<forList.length; i++) {
                if ($('#experience_for').find("option[value='" + forList[i] + "']").length) {
                    $('#experience_for').val(forList[i]).trigger('change');
                } else { 
                    var newOption = new Option(forList[i], forList[i], true, false);
                    $('#experience_for').append(newOption).trigger('change');
                }
            }
            if(forList.includes(fors)) {
                $('#experience_for').val(fors).trigger('change');
            }
        }
    });
}

function get_jobs(addr, fors) {
    $.ajax({
        url: "/get_jobs",
        type: "get",
        data: {"addr": addr, "fors": fors},
        success: function(data) {
            jobList = data.jobs;
            optLen = $("#experience_job").find("option").length;

            $('#experience_job').val(null).trigger('change');
            $('#experience_job').html('').select2({data: [{value: '', id: '', text: '전체'}]});

            for(var i=0; i<jobList.length; i++) {
                if ($('#experience_job').find("option[value='" + jobList[i] + "']").length) {
                    $('#experience_job').val(jobList[i]).trigger('change');
                } else { 
                    var newOption = new Option(jobList[i], jobList[i], true, false);
                    $('#experience_job').append(newOption).trigger('change');
                }
            }
            if(jobList.includes(jobs)) {
                $('#experience_job').val(jobs).trigger('change');
            }
        }
    });
}

function get_result_data(addr, fors, jobs) {
    $.ajax({
        url: "/get_search_result",
        type: "get",
        data: {"addr": addr, "fors": fors, "jobs": jobs},
        success: function(data) {
            let results = data.result_lists;
            let temp = results.slice(2, results.length).split("[");
            
            if(temp[0].length > 0) {
                let lists = [];
                let indexes = [];
                
                for(let i=0; i<temp.length; i++) {
                    if(i == temp.length-1) {
                        temp[i] = temp[i].slice(0, -2);
                    } else {
                        temp[i] = temp[i].slice(0, -3);
                    }
                    let tmp = temp[i].split(",");
                    lists[i] = rep_str(tmp);
                    indexes[i] = tmp[0];
                }
                $('.job-table').DataTable({
                    destroy: true,
                    "searching": false,
                    data: lists
                });
                let trs = $("#lists-body>tr");
                for(let i=0; i<trs.length; i++) {
                    $("#lists-body").children().eq(i).attr({
                        'id': ('detail_' + indexes[i])
                        // "class": "lists-row"
                    });
                }
            } else {
                let table = $('.job-table').DataTable();
                table.clear().draw();
            }
        },
        error: function(request,status,error){
            // console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            console.log("code:"+request.status+"\n"+"message:"+"\n"+"error:"+error);
        }
    });
    return false;
}

function rep_str(list) {
    let resultList = []
    if(list.length > 1) {
        resultList[0] = list[1].split("'")[1];
        resultList[1] = (list[4].split("'")[1]).split("&").join(",");
        resultList[2] = (list[15].split("|")).join(",").split("'")[1];
        resultList[3] = list[8].split("'")[1];
        let star = "";
        for(let i=0; i<list[18]; i++){
            star += "⭐";
        }
        resultList[4] = star;
        star = "";
        for(let i=0; i<list[19]; i++) {
            star += "⭐";
        }
        resultList[5] = star;
        resultList[6] = list[13];
    }
    return resultList
}

// 모달에 넘길 데이터
function get_modal_data(no) {
    $.ajax({
        url: "/get_modal_data",
        type: "get",
        data: {"dataNo": no},
        success: function(data) {
            let modal_data = data.modal_data;
            set_modal_data(modal_data);
        },
        error: function(request,status,error){
            // console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            console.log(request.responseText);
            // console.log("code:"+request.status+"\n"+"message:"+"\n"+"error:"+error);
        }
    });
    return false;
}

function set_modal_data(modal_data) {
    $("#prog-name").text(modal_data[0])
    $("#prog-type").text(modal_data[1])
    $("#prog-loc").text(modal_data[2])
    $("#prog-comp").text(modal_data[3])
    $("#prog-comp-type").text(modal_data[4])
    $("#prog-edu").text(modal_data[5])
    $("#prog-job").text(modal_data[6])
    $("#prog-sched").text(modal_data[7])
    $("#prog-peop").text(modal_data[8])
    $("#prog-hour").text(modal_data[9])
    $("#prog-price").text(modal_data[10])
    $("#prog-ava-loc").text(modal_data[11])
    $("#prog-for").text(modal_data[12])
    star = ""
    for(let i=0; i<modal_data[13]; i++) {
        star += "⭐";
    }
    $("#prog-good").text(star)
    star = ""
    for(let i=0; i<modal_data[14]; i++) {
        star += "⭐";
    }
    $("#prog-safe").text(star)
}