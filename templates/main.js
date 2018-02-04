/**
 * Project: EPICS IS WS Kiosk Web Application
 * Program name: main.js
 * Author: Ryan Schwartz
 *
 * Purpose:
 */

var timeoutRequests = 0;
var startTime = new Date().getTime();
var refreshRate = 900000; // Milliseconds, 15 minutes
var city = "Weather Station";
var sensor = "temperature";
var sup = {"temperature": "<sup>°F</sup>", "humidity": "%", "pressure": " in", "wind_speed": " mph", "wind_gust": " mph", "rainfall": " in"};

$(document).ready(function() {pullData();});

/////////////////////////////////////////////////////////
///                                                   ///
///               Main function (timer)               ///
///                                                   ///
/////////////////////////////////////////////////////////
function timer() {
    if (timeoutRequests > 3) {return;} // Stop updating if error handler sends service request email
    var now = new Date().getTime();
    pullData();
    setTimeout(timer, refreshRate - ((new Date().getTime() - startTime) % refreshRate));
};

// TODO: Enable ajax timer
// timer();

// Handles any ajax errors from below, just to make sure requests aren't being made when the service is broken
function errorHandler(message) {
    if (++timeoutRequests > 3) {
        // Something is wrong, have server send email request for help
        console.log("Error Found");
        console.log(message);
        $.ajax({
            type: 'POST',
            url: '/request/error',
            data: {"message": message},
            success: function(response) {
                console.log("Help requested: " + response);
            }
        });
    }
}

function changeCity(newCity) {
    city = newCity
    // All transition stuff
    changePage();
}

function changeSensor(newSensor) {
    sensor = newSensor
    changePage()
}

function changePage() {
    clearGraph();
    data = JSON.parse(localStorage.getItem("data"));
    data = data[city][sensor];
    if (data.length > 1) {
        // Reverse the loading so that the newest values are loaded last
        for (i = data.length - 1; i >= 0; i--) {
            var t = new moment(data[i]['time']);
            if (t.subtract(7, 'days')) {
                addThirtyDaysPoint(t, data[i][sensor]);
            }
            addSevenDaysPoint(t, data[i][sensor]);
        }
        // https://stackoverflow.com/questions/4878756/how-to-capitalize-first-letter-of-each-word-like-a-2-word-city
        document.getElementById('current_title').innerHTML = "Current " + sensor.replace(/_/g, " ").replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
        var lastTime = data[data.length - 1][sensor];
        document.getElementById('current_data').innerHTML = lastTime + sup[sensor];
        var prevTime = data[data.length - 2][sensor];
        document.getElementById('data_description').innerHTML = "%.2f" % lastTime / prevTime + "% change in the past 15 minutes."
    }
}

function pullData() {
    $.ajax({
        type: 'GET',
        url: "/request/data",
        dataType: "json",
        timeout: 10000,
        success: function(response) {
            timeoutRequests = 0;

            // Store response if available
            if (typeof(Storage) !== "undefined") {
                //TODO: Remove all values that are less than 0 or None
                localStorage.setItem("data", JSON.stringify(response));
            }
        },
        error: function(xmlhttprequest, textstatus, message) {
            if (textstatus === "timeout") {
                errorHandler(message);
            } else {
                // Something else went wrong, but we'll just override the number of requests to send a POST request
                timeoutRequests = 3;
                errorHandler("AJAX Call Error; Error Code: " + xmlhttprequest.status + ", Message: " + message);
            }
        }
    });
}
