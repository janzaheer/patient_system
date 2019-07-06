$.get('/daily/reports/', function(result, status){

    var amount = [];
    var discount = [];
    var total = [];
    var sales_date = [];

    $.each(result.bill_data, function(index, value){

        $('.daily-sales-tbody').append('<tr><td>'+ value.date + '</td><td>' + value.amount + '</td><td>' + value.discount + '</td><td>' + value.total + '</td></tr>');

        amount.push(value.amount);
        discount.push(value.discount);
        total.push(value.total);
        sales_date.push(value.date);

    });
    Highcharts.chart('daily_graph', {
        chart: {
            type: 'area'
        },
        title: {
            text: 'Daily Reports'
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            categories: sales_date.reverse(),
            tickmarkPlacement: 'on',
            title: {
                enabled: false
            }
        },
        yAxis: {
            title: {
                text: ''
            },
            labels: {
                formatter: function () {
                    return this.value;
                }
            }
        },
        tooltip: {
            split: true,
            valueSuffix: 'Rs'
        },
        plotOptions: {
            area: {
                stacking: 'normal',
                lineColor: '#666666',
                lineWidth: 1,
                marker: {
                    lineWidth: 1,
                    lineColor: '#666666'
                }
            }
        },

        series: [{
            name: 'Reports',
            data: total.reverse()
        }]
    });

});

$.get('/monthly/reports/', function (result, status) {
    var amount = [];
    var discount = [];
    var total = [];
    var day = [];
    $.each(result.bill_data , function (index, value) {
        $('.monthly-sales-tbody').append('<tr><td>'+ value.day + '</td><td>' + value.amount + '</td><td>' + value.discount + '</td><td>' + value.total + '</td></tr>');


        amount.push(value.amount);
        discount.push(value.discount);
        total.push(value.total);
        day.push(value.day);
    });

    Highcharts.chart('monthly-graph', {
        chart: {
            type: 'area'
        },
        title: {
            text: 'Monthly Reports'
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            categories: day.reverse(),
            tickmarkPlacement: 'on',
            title: {
                enabled: false
            }
        },
        yAxis: {
            title: {
                text: 'Billions'
            },
            labels: {
                formatter: function () {
                    return this.value;
                }
            }
        },
        tooltip: {
            split: true,
            valueSuffix: ' Rupees'
        },
        plotOptions: {
            area: {
                stacking: 'normal',
                lineColor: '#666666',
                lineWidth: 1,
                marker: {
                    lineWidth: 1,
                    lineColor: '#666666'
                }
            }
        },
        series: [{
            name: 'Reports',
            data: total.reverse()
        }]
    });
});
