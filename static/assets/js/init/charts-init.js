
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
                xAxes: [ {
                    display: true,
                    gridLines: {
                        display: false,
                        drawBorder: false
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
                        beginAtZero: true,
                        stepSize: 2000
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
            legend: {
                position: 'top'
            },
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
                    backgroundColor: 'rgba(0,200,155,.35)',
                    borderColor: 'rgba(0,200,155,0.60)',
                    borderWidth: 3.5,
                    pointStyle: 'circle',
                    pointRadius: 5,
                    pointBorderColor: 'transparent',
                    pointBackgroundColor: 'rgba(0,200,155,0.60)',
                    data: values
                }]
            }
            ct1(chart1Data);
        },
        error: function(request,status,error){
            // console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            console.log(request.responseText);
            // console.log("code:"+request.status+"\n"+"message:"+"\n"+"error:"+error);
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
                    borderColor: "rgba(0, 194, 146, 0.9)",
                    borderWidth: "0",
                    backgroundColor: "rgba(0, 194, 146, 0.5)"
                }]
            }
            ct2(chart2Data);
        },
        error: function(request,status,error){
            // console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            console.log(request.responseText);
            // console.log("code:"+request.status+"\n"+"message:"+"\n"+"error:"+error);
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
                    borderColor: "rgba(0, 194, 146, 0.6)",
                    borderWidth: "1",
                    backgroundColor: "rgba(0, 194, 146, 0.4)"
                }]
            }
            ct3(chart3Data);
        },
        error: function(request,status,error){
            // console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            console.log(request.responseText);
            // console.log("code:"+request.status+"\n"+"message:"+"\n"+"error:"+error);
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
                        "rgba(0, 194, 146,0.9)",
                        "rgba(0, 194, 146,0.8)",
                        "rgba(0, 194, 146,0.7)",
                        "rgba(0,0,0,0.2)",
                        "rgba(0, 194, 146,0.5)"
                    ]
                }],
                labels: labels
            }
            ct4(chart4Data);
        },
        error: function(request,status,error){
            // console.log("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            console.log(request.responseText);
            // console.log("code:"+request.status+"\n"+"message:"+"\n"+"error:"+error);
        }
    });
    return false;
}