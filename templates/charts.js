
function addSevenDaysPoint(xVal, yVal) {
    chartData = sevenDays.data.datasets[0];
    chartData.data.push({x: xVal, y: yVal});
    sevenDays.update();
}

function addThirtyDaysPoint(xVal, yVal) {
    chartData = thirtyDays.data.datasets[0];
    chartData.data.push({x: xVal, y: yVal});
    thirtyDays.update();
}

function rmDataPoint() {
    sevenDays.data.datasets[0].data.shift();
    sevenDays.update();
}

function clearGraph() {
    sevenDays.data.datasets[0].data = [];
    thirtyDays.data.datasets[0].data = [];
    sevenDays.update();
    thirtyDays.update();
}

// Render chart
var sevenDays = new Chart(document.getElementById('sevenDayChart').getContext('2d'), {
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
            text: '7 Day History',
            fontColor: 'rgba(255, 255, 255, .85)',
            fontSize: 24,
            padding: 16
        },
        scales: {
            xAxes: [{
                type: 'time',
                distribution: 'linear',
                time: {
                    unit: 'hour',
                    displayFormats: {
                        // Formatting: http://momentjs.com/docs/#/displaying/format/
                        hour: 'M/D, hh:mm A'
                    }
                },
                ticks: {
                    fontColor: 'rgba(255, 255, 255, .85)',
                    fontSize: 18
                },
                gridLines: {
                    display: false
                }
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
                time: {
                    unit: 'hour',
                    displayFormats: {
                        // Formatting: http://momentjs.com/docs/#/displaying/format/
                        hour: 'M/D, hh:mm A'
                    }
                },
                ticks: {
                    fontColor: 'rgba(255, 255, 255, 1)',
                    fontSize: 18
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
