
function addSevenDaysPoint(xVal, yVal) {
    sevenDays.data.labels.push(xVal);
    chartData = sevenDays.data.datasets[0];
    chartData.data.push(yVal);
    sevenDays.update();
}

function addThirtyDaysPoint(xVal, yVal) {
    thirtyDays.data.labels.push(xVal);
    chartData = thirtyDays.data.datasets[0];
    chartData.data.push(yVal);
    thirtyDays.update();
}

function rmDataPoint() {
    // sevenDays.data.datasets[0].data.shift();
    // sevenDays.update();
}

function clearGraph() {
    sevenDays.data.labels = [];
    sevenDays.data.datasets[0].data = [];
    thirtyDays.data.labels = [];
    thirtyDays.data.datasets[0].data = [];
    sevenDays.update();
    thirtyDays.update();
}

// Render chart
var sevenDays = new Chart(document.getElementById('sevenDayChart').getContext('2d'), {
    type: 'line',
    data: {
        labels: [],
		datasets: [{
			fill: false,
            backgroundColor: 'rgba(255, 255, 255, 1)',
            borderColor: 'rgba(255, 255, 255, 1)',
			data: [],
		}]
	},
    options: {
        title: {
            display: true,
            text: '7 Day History',
            fontColor: 'rgba(255, 255, 255, .85)',
            fontSize: 24,
            padding: 16
        },
        scales: {
            xAxes: [{
                // id: 'xAxis1',
                type: 'time',
                distribution: 'series',
                time: {
                    unit: 'hour',
                    // unitStepSize: 0.5,
                    round: 'hour',
                    displayFormats: {
                        // Formatting: http://momentjs.com/docs/#/displaying/format/
                        // Major axis day, minor axis hour
                        hour: 'h:mm A'
                    }
                },
                ticks: {
                    fontColor: 'rgba(255, 255, 255, .85)',
                    fontSize: 18,
                    source: 'auto'
                    // callback: function(label) {
                    //     // console.log(label);
                    //     return '$$' + label;
                    // }
                },
                gridLines: {
                    display: false
                }
            // }, {
            //     id: 'xAxis2',
            //     type: 'category',
            //     ticks: {
            //         callback: function(label) {
            //             return label.format('MMM Do');
            //         },
            //         fontColor: 'rgba(255, 255, 255, .85)',
            //         fontSize: 18
            //     },
            //     gridLines: {
            //         drawOnChartArea: false
            //     }
            }],
            yAxes: [{
                gridLines: {
                    color: 'rgba(255, 255, 255, .85)',
                    zeroLineColor: 'rgba(255, 255, 255, .85)',
                    drawTicks: false,
                    lineWidth: 2
                },
                ticks: {
                    fontColor: 'rgba(255, 255, 255, .85)',
                    padding: 8,
                    fontSize: 18
                }
            }]
        },
        legend: {
            display: false
        }
    }
});

var thirtyDays = new Chart(document.getElementById('thirtyDayChart').getContext('2d'), {
    type: 'line',
    data: {
		datasets: [{
			fill: false,
            backgroundColor: 'rgba(255, 255, 255, 1)',
            borderColor: 'rgba(255, 255, 255, 1)',
			data: [],
		}]
	},
    options: {
        title: {
            display: true,
            text: '30 Day History',
            fontColor: 'rgba(255, 255, 255, 1)',
            fontSize: 24,
            padding: 16
        },
        scales: {
            xAxes: [{
                    type: 'time',
                    distribution: 'linear',
                    bounds: 'data',
                    time: {
                        unit: 'hour',
                        stepSize: 2,
                        round: 'hour',
                        displayFormats: {
                            hour: 'MMM D'
                        }
                    },
                    ticks: {
                        fontColor: 'rgba(255, 255, 255, 1)',
                        fontSize: 18,
                        source: 'auto'
                    },
                    gridLines: {
                        display: false
                    }
                }],
            yAxes: [{
                gridLines: {
                    color: 'rgba(255, 255, 255, 1)',
                    zeroLineColor: 'rgba(255, 255, 255, 1)',
                    drawTicks: false,
                    lineWidth: 2
                },
                ticks: {
                    fontColor: 'rgba(255, 255, 255, 1)',
                    padding: 8,
                    fontSize: 18
                }
            }]
        },
        legend: {
            display: false
        }
    }
});
