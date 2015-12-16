
function viewGroup(code, name) {

    // Create the chart 1
    $.getJSON('http://localhost:8080/json/quotes/' + code + '.json', function (data) {

        $('#container1').highcharts('StockChart', {

            rangeSelector : {
                selected : 1
            },

            title : {
                text : name + ' Stock Price'
            },

            series : [{
                name : name + ' Stock Price',
                data : data,
		type: 'area',                
                threshold : null,
                tooltip : {
                    valueDecimals : 2
                },
                fillColor : {
                    linearGradient : {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1
                    },
                    stops : [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                }
            },
	],


        });
    });


    // Create the chart 2    
    var options = {
        chart: {
            renderTo: 'container2',
            type: 'area'
        },
        xAxis: {
            type: 'datetime',
	    title: {text: "Time"}
        },
        legend: {
            enabled: false
        },
        series: [{data: [], color: 'rgba(233,30,0,0.5)'}, {data: [], color: 'rgba(55,233,41,0.5)'}],
	title : { 
	    text: "Mean Reversion Strategy with Bollinger Bands (50-day MA +/- 2&sigma;)",
	    useHTML: true
	},
	yAxis: {
	    title : { text: "Returns"}
	}
    };

    $.getJSON('http://localhost:8080/json/profits/' + code + '.json', function (data) {
        options.series[0].data = data['neg'];
        options.series[1].data = data['pos'];
        var chart = new Highcharts.Chart(options);
    });

    // Create the chart 3
    var options2 = {
        chart: {
            renderTo: 'container3',
            type: 'area'
        },
        xAxis: {
            type: 'datetime',
            title: {text: "Time"}
        },
        legend: {
            enabled: false
        },
        series: [{data: [], color: 'rgba(233,30,0,0.5)'}, {data: [], color: 'rgba(55,233,41,0.5)'}],
        title : {
            text: "Momentum Trading Strategy" 
        },
        yAxis: {
            title : { text: "Returns"}
        }
    };

    $.getJSON('http://localhost:8080/json/profits_2/' + code + '.json', function (data) {
        options2.series[0].data = data['neg'];
        options2.series[1].data = data['pos'];
        var chart = new Highcharts.Chart(options2);
    });

}

$(document).ready(function() {

    $('#view-group-select').on("change", function() {
        code = $(this).val()
        res = $("#view-group-select option:selected").text().split(' (')[1]
        name = res.substr(0, res.length-1)
        viewGroup(code, name)
    })

    $.get('http://localhost:8080/filenames.txt', function (data) {
        names = data.split('\n')
        for (i=0; i<names.length; i++) {
            $('#view-group-select').append("<option value=" + names[i].split(' (')[0] + ">" + names[i] + "</option>")
        }
    })
    
});
