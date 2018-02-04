
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
			data: [],
		}]
	},
    options: {
        title: {
            display: true,
            text: '7 Day History'
        },
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    displayFormats: {
                        day: 'MMM D'
                    }
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
			data: [],
		}]
	},
    options: {
        title: {
            display: true,
            text: '30 Day History'
        },
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    displayFormats: {
                        day: 'MMM D'
                    }
                }
            }]
        },
        legend: {
            display: false
        }
    }
});
