
function ct1(chart1Data) {
    var ctx = $("#chart1")
    
    var chart1 = new Chart(ctx,{
        type: 'line',
        data: chart1Data,
        options: {
            responsive: true,
            tooltips: {
                mode: 'index',
                titleFontSize: 12,
                titleFontColor: '#000',
                bodyFontColor: '#000',
                backgroundColor: '#fff',
                titleFontFamily: 'Montserrat',
                bodyFontFamily: 'Montserrat',
                cornerRadius: 3,
                intersect: false,
            },
            legend: {
                display: false,
                position: 'top',
                labels: {
                    usePointStyle: true,
                    fontFamily: 'Montserrat',
                },
            },
            scales: {
                xAxes: [{
                    display: true,
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        fontSize: 14
                    }
                    
                } ],
                yAxes: [ {
                    display: true,
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                    scaleLabel: {
                        display: true,
                        labelString: '합계'
                    },
                    ticks: {
                        fontSize: 14,
                        stepSize: 1
                    }
                }]
            },
            title: {
                display: false,
            }
        }
    } );
}

function ct2(chart2Data) {
    var ctx = $("#chart2")
    
    var chart2 = new Chart( ctx, {
        type: 'bar',
        data: chart2Data,
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        fontSize: 16,
                        beginAtZero: true,
                        stepSize: 2000
                    }
                }],
                xAxes: [{
                    ticks: {
                        fontSize: 14
                    }
                }]
            }
        }
    } );
}

function ct3(chart3Data) {
    var ctx = $("#chart3");
    ctx.height = 160;
    var chart3 = new Chart(ctx,{
        type: 'radar',
        data: chart3Data,
        options: {
            scale: {
                ticks: {
                    beginAtZero: true
                }
            }
        }
    });
};

function ct4(chart4Data) {
    var ctx = $("#chart4");
    ctx.height = 160;
    var chart4 = new Chart(ctx,{
        type: 'polarArea',
        data: chart4Data,
        options: {
            responsive: true
        }
    });
};

function ct5(chart5Data) {
    var ctx = document.getElementById("chart5").getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: chart5Data,
        options: {
            scales: {
                xAxes: [{
                    stacked: true,
                    ticks: {
                        fontSize: 16
                    }
                }, {
                    id: 'x-axis-2',
                    type: 'linear',
                    position: 'bottom',
                    display: true,
                    ticks: {
                    beginAtZero: true,
                    min: 0,
                    max: 15,
                    stepSize: 1
                    }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        max: 1.2,
                        fontSize: 16
                    },
                    stacked: true,
                }]
            }
        }
    });
}
  


  

function get_chart1() {
    $.ajax({
        url: "/get_chart1",
        type: "get",
        success: function(data) {
            let labels = data.labels;
            let values = data.values;
            // console.log(labels)
            // console.log(values)

            var chart1Data = {
                labels : labels,
                datasets: [{
                    backgroundColor: 'rgba(176, 18, 0, 0.12)',
                    borderColor: 'rgba(176, 18, 0, 0.26)',
                    borderWidth: 3.5,
                    pointStyle: 'circle',
                    pointRadius: 5,
                    pointBorderColor: 'transparent',
                    pointBackgroundColor: 'rgba(176, 18, 0, 0.26)',
                    data: values
                }]
            }
            ct1(chart1Data);
        },
        error: function(request,status,error){
            // console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            // console.log(request.responseText);
            console.log("code:"+request.status+"\n"+"message:"+"\n"+"error:"+error);
        }
    });
    return false;
}

function get_chart2() {
    $.ajax({
        url: "/get_chart2",
        type: "get",
        success: function(data) {
            let labels = data.labels;
            let values = data.values;

            var chart2Data = {
                labels: labels,
                datasets: [{
                    label: "연봉",
                    data: values,
                    backgroundColor: [
                        "rgb(54,39,6,.58)",
                        "rgba(142,128,106,.58)",
                        "rgba(195,176,145,.58)",
                        "rgba(228,205,167,.58)",
                        "rgba(255,230,188,.58)"
                    ],
                    borderColor: [
                        "rgb(54, 39, 6)",
                        "rgb(142, 128, 106)",
                        "rgb(195, 176, 145)",
                        "rgb(228, 205, 167)",
                        "rgb(255, 230, 188)"
                    ],
                    borderWidth: "0"
                }]
            }
            ct2(chart2Data);
        },
        error: function(request,status,error){
            // console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            // console.log(request.responseText);
            console.log("code:"+request.status+"\n"+"message:"+"\n"+"error:"+error);
        }
    });
    return false;
}

function get_chart3() {
    $.ajax({
        url: "/get_chart3",
        type: "get",
        success: function(data) {
            let labels = data.labels;
            let values = data.values;
            // console.log(labels)
            // console.log(values)

            var chart3Data = {
                labels: labels,
                datasets: [{
                    label: 'Degree',
                    data: values,
                    borderColor: "rgb(152, 180, 170)",
                    borderWidth: "1",
                    backgroundColor: "rgba(152, 180, 170, .58)"
                }]
            }
            ct3(chart3Data);
        },
        error: function(request,status,error){
            // console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            // console.log(request.responseText);
            console.log("code:"+request.status+"\n"+"message:"+"\n"+"error:"+error);
        }
    });
    return false;
}

function get_chart4() {
    $.ajax({
        url: "/get_chart4",
        type: "get",
        success: function(data) {
            let labels = data.labels;
            let values = data.values;

            var chart4Data = {
                datasets: [{
                    data: values,
                    backgroundColor: [
                        "rgba(101, 93, 138, .58)",
                        "rgba(120, 151, 171, .58)",
                        "rgba(216, 133, 163, .58)",
                        "rgba(253, 206, 185, .58)",
                        "rgba(0,0,0,0.2)"
                    ]
                }],
                labels: labels
            }
            ct4(chart4Data);
        },
        error: function(request,status,error){
            // console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            // console.log(request.responseText);
            console.log("code:"+request.status+"\n"+"message:"+"\n"+"error:"+error);
        }
    });
    return false;
}

function get_chart5() {
    $.ajax({
        url: "/get_chart5",
        type: "get",
        success: function(data) {
            let loss_people = data.loss_people;
            let loss_percent = data.loss_percent;
            let get_people = data.get_people;
            let xticks = data.xticks;
            let models = data.models;
            
            let chart5Data = {
                labels: xticks,
                datasets: [
                    {
                        label: models[0],
                        backgroundColor: "rgba(211, 222, 220, 0.9)",
                        data: loss_people,
                        stack: 'Stack 1'
                    },
                    {
                        label: models[1],
                        backgroundColor: "rgba(146, 169, 189, 0.9)",
                        data: loss_percent,
                        stack: 'Stack 2'
                    },
                    {
                        label: models[2],
                        backgroundColor: "rgba(255, 239, 239, 0.9)",
                        data: get_people,
                        stack: 'Stack 3'
                    }
                ]
            };
            ct5(chart5Data);
        },
        error: function(request,status,error){
            // console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            // console.log(request.responseText);
            console.log("code:"+request.status+"\n"+"message:"+"\n"+"error:"+error);
        }
    });
    return false;
}