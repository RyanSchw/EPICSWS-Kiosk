
// Currently imports Chart.js from Cloudflare

function graphChart(tempValues) {
    chartData = myChart.data.datasets;
    chartData.push({});
    chartData[numberOfDataPoints].data        = tempValues;
    chartData[numberOfDataPoints].label       = 'Day ' + numberOfDataPoints;
    chartData[numberOfDataPoints].borderColor = '#' + Math.random().toString(16).slice(2, 8).toUpperCase().slice(-6);
    chartData[numberOfDataPoints].fill        = false;
    myChart.update();
}

function formattedLabels() {
    var tab = [];
    for (i = 0; i < 25; i++) {
        tab[i] = i;
    }
    return tab;
}

// Render chart
var ctx = document.getElementById('tempChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: formattedLabels(),
        datasets: []
    },
    options: {
        title: {
            display: true,
            text: 'Day History'
        }
    }
});
