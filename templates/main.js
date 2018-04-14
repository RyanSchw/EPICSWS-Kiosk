/**
 * Project: EPICS IS WS Kiosk Web Application
 * Program name: main.js
 * Author: Ryan Schwartz
 *
 * Purpose:
 */

// Configurable stuff
var TEST_MODE = 1; // 0 is 6 button, 1 is 3 button
var TIMEOUT_MAX = 3; // Max number of timeout errors

// Constants
var rating = 2;
var timeoutRequests = 0;
var startTime = new Date().getTime();
var city = "Weather Station";
var sensor = "temperature";
var sup = {"temperature": "<sup>°F</sup>", "humidity": "%", "pressure": " in", "wind_speed": " mph", "wind_gust": " mph", "rainfall": " in"};
var cities = ["Weather Station", "Sacramento", "Tampa", "Washington"];
var sensors = ["temperature", "rainfall", "wind_speed", "humidity", "pressure"];
var measured = {
    "temperature": "Temperature is a degree of hotness or coldness the can be measured using a thermometer. It's also a measure of how fast the atoms and molecules of a substance are moving. Temperature is measured in degrees on the Fahrenheit, Celsius, and Kelvin scales.",
    "humidity": "Humidity is the amount of water vapor present in the air. Water vapor is the gaseous state of water and invisible to the human eye.",
    "pressure": "Atmospheric pressure, sometimes also called barometric pressure, is the pressure within the atmosphere of Earth (or that of another planet). As elevation increases, there is less overlying atmospheric mass, so that atmospheric pressure decreases with increasing elevation.",
    "wind_speed": "Wind is created when changes in temperatures cause air to move from high to low pressure areas. Low pressure areas are often where warm air is, because when air is warmed by the sun it rises, leaving behind less air, so there are fewer air molecules and therefore less pressure.",
    "rainfall": "Rain is one type of liquid precipitation and is the result of water vapour condensing and precipitating."
};
var sensor_used = {
    "temperature": "Sparkfun SEN-13683 (Combined with humidity sensor)",
    "humidity": "Sparkfun SEN-13683 (Combined with temperature sensor)",
    "pressure": "Sparkfun SEN-09721",
    "wind_speed": "Sparkfun SEN-08942 (Combined with rainfall sensor)",
    "rainfall": "Sparkfun SEN-08942 (Combined with wind sensor)"
};
var works = {
    "temperature": "Thermistors are made of semiconductor material with a resistivity that is especially sensitive to temperature. The resistance of a thermistor decreases with increasing temperature so that when temperature changes, the resistance change is predictable.",
    "humidity": "A capacitive humidity sensor measures relative humidity by placing a thin strip of metal oxide between two electrodes. The metal oxide’s electrical capacity changes with the atmosphere’s relative humidity. Weather, commercial and industries are the major application areas.",
    "pressure": "Pressure is an expression of the force required to stop a fluid from expanding, and is usually stated in terms of force per unit area. A pressure sensor usually acts as a transducer; it generates a signal as a function of the pressure imposed.",
    "wind_speed": "Some of the fan blades have tiny magnets mounted on them and, each time they make a single rotation, they move past a magnetic detector called a reed switch. When a magnet is nearby, the reed switch closes and generates a brief pulse of electric current, before opening again when the magnet goes away.",
    "rainfall": "The tipping bucket rain gauge consists of a funnel that collects and channels the precipitation into a small seesaw-like container. After a pre-set amount of precipitation falls, the lever tips, dumping the collected water and sending an electrical signal."
};

var elem = document.querySelector("#fs");
var survey = [];
var Q1 = UIkit.modal("#modal-group-1");
var Q2 = UIkit.modal("#modal-group-2");
var Q3 = UIkit.modal("#modal-group-3");
var QF = UIkit.modal("#modal-group-4");

$(document).ready(function() {pullData();changePage();});

// Handles any ajax errors from below, just to make sure requests aren't being made when the service is broken
function errorHandler(message) {
    if (++timeoutRequests > TIMEOUT_MAX) {
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

function enterFullscreen() {
    if (elem.webkitRequestFullScreen) {
        elem.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);
    } else {
        elem.mozRequestFullScreen();
    }
}

function changeCity(newCity) {
    document.getElementById(city).classList.remove("active-city");
    city = newCity
    document.getElementById(city).classList.add("active-city");
    addLog(newCity);
    changePage();
}

function changeSensor(newSensor) {
    document.getElementById(sensor).classList.remove("active-sensor");
    document.getElementById(sensor).classList.add("nonactive-sensor");
    sensor = newSensor
    document.getElementById(sensor).classList.add("active-sensor");
    document.getElementById(sensor).classList.remove("nonactive-sensor");
    addLog(newSensor);
    changePage();
}

function addLog(type) {
    $.ajax({
        type: 'POST',
        url: '/request/submit',
        data: {"time": moment().unix(), "button": type}
    });
}

function changePage() {
    clearGraph();
    console.log(city);
    data = JSON.parse(localStorage.getItem("data"))[city][sensor];
    if (data.length > 1) {
        // Reverse the loading so that the newest values are loaded last
        for (i = data.length - 1; i >= 0; i--) {
            var t = new moment(data[i]['time']);
            if (t.subtract(7, 'days')) {
                addThirtyDaysPoint(t, data[i][sensor]);
            }
            addSevenDaysPoint(t, data[i][sensor]);
        }

        // Update "Current xxx"
        // https://stackoverflow.com/questions/4878756/how-to-capitalize-first-letter-of-each-word-like-a-2-word-city
        document.getElementById('current_title').innerHTML = "Current " + sensor.replace(/_/g, " ").replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
        var lastTime = data[data.length - 1][sensor];
        document.getElementById('current_data').innerHTML = lastTime + sup[sensor];
        var prevTime = data[data.length - 2][sensor];
        if (lastTime - prevTime < 0) {
            document.getElementById('data_description').innerHTML = (((lastTime - prevTime) / (prevTime || 1) * 100).toFixed(5)).toString().substring(0, 5) + "% change in the past 15 minutes."
        } else {
            document.getElementById('data_description').innerHTML = (((lastTime - prevTime) / (prevTime || 1) * 100).toFixed(5)).toString().substring(0, 4) + "% change in the past 15 minutes."
        }

        // Update descriptions
        document.getElementById("Measured").innerHTML = measured[sensor];
        document.getElementById("Sensor").innerHTML = sensor_used[sensor];
        document.getElementById("Works").innerHTML = works[sensor];
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

function takeSurvey() {
    // Pop up with survey instructions, include CANCEL button (same as takeSurvey button)
    if (Q1.isToggled() || Q2.isToggled() || Q3.isToggled()) {
        Q1.hide();
        Q2.hide();
        Q3.hide();
        QF.hide();
        survey = [];
    } else {
        Q1.show();
        Q2.hide();
        Q3.hide();
        QF.hide();
    }
}

function nextQuestion() {
    if (Q1.isToggled()) {
        Q1.hide();
        Q2.show();
        Q3.hide();
        QF.hide();
        survey[survey.length < 0 ? 0 : survey.length] = rating + 1;
    } else if (Q2.isToggled()) {
        Q1.hide();
        Q2.hide();
        Q3.show();
        QF.hide();
        survey[survey.length < 0 ? 0 : survey.length] = rating + 1;
    } else if (Q3.isToggled()) {
        survey[survey.length < 0 ? 0 : survey.length] = rating + 1;
        submitSurvey();
        Q1.hide();
        Q2.hide();
        Q3.hide();
        QF.show();
    } else if (QF.isToggled()) {
        Q1.hide();
        Q2.hide();
        Q3.hide();
        QF.hide();
    } else {
        takeSurvey();
    }
}

function submitSurvey() {
    if (survey != null) {
        $.ajax({
            type: 'POST',
            url: '/request/survey',
            data: {"Q1": survey[0] || 0, "Q2": survey[1] || 0, "Q3": survey[2] || 0}
        });
    }
}

document.addEventListener('keydown', function(event) {
    if (TEST_MODE) {
        // TEST MODE 1, 3 button layout
        if (event.keyCode == 74) {
            // j, moves sensor to the left
            if (Q1.isToggled() || Q2.isToggled() || Q3.isToggled()) {
                rating = (((rating - 1) % 5) + 5) % 5;
                document.getElementById("rating1").innerHTML = rating + 1;
                document.getElementById("rating2").innerHTML = rating + 1;
                document.getElementById("rating3").innerHTML = rating + 1;
            } else if (QF.isToggled()) {
                nextQuestion();
            } else {
                changeSensor(sensors[(((sensors.indexOf(sensor) - 1) % sensors.length) + sensors.length) % sensors.length]);
            }
        }
        else if (event.keyCode == 75) {
            // k, resets to home
            nextQuestion();
        }
        else if (event.keyCode == 76) {
            // l, moves sensor to the right
            if (Q1.isToggled() || Q2.isToggled() || Q3.isToggled()) {
                rating = (rating + 1) % 5;
                document.getElementById("rating1").innerHTML = rating + 1;
                document.getElementById("rating2").innerHTML = rating + 1;
                document.getElementById("rating3").innerHTML = rating + 1;
            } else if (QF.isToggled()) {
                nextQuestion();
            } else {
                changeSensor(sensors[(sensors.indexOf(sensor) + 1) % sensors.length]);
            }
        }
    // } else {
    //     // TEST MODE 0, 6 button layout
    //     if (event.keyCode == 85) {
    //       // u, temperature
    //       if (Q1.isToggled() || Q2.isToggled() || Q3.isToggled()) {
    //           survey[survey.length < 0 ? 0 : survey.length] = 1;
    //           nextQuestion();
    //       } else if (QF.isToggled()) {
    //           nextQuestion();
    //       } else {
    //           changeSensor("temperature");
    //       }
    //     }
    //     else if (event.keyCode == 73) {
    //       // i, humidity
    //       if (Q1.isToggled() || Q2.isToggled() || Q3.isToggled()) {
    //           survey[survey.length < 0 ? 0 : survey.length] = 2;
    //           nextQuestion();
    //       } else if (QF.isToggled()) {
    //           nextQuestion();
    //       } else {
    //           changeSensor("humidity");
    //       }
    //     }
    //     else if (event.keyCode == 79) {
    //       // o, pressure
    //       if (Q1.isToggled() || Q2.isToggled() || Q3.isToggled()) {
    //           survey[survey.length < 0 ? 0 : survey.length] = 3;
    //           nextQuestion();
    //       } else if (QF.isToggled()) {
    //           nextQuestion();
    //       } else {
    //           changeSensor("pressure");
    //       }
    //     }
    //     else if (event.keyCode == 74) {
    //       // j, rainfall
    //       if (Q1.isToggled() || Q2.isToggled() || Q3.isToggled()) {
    //           survey[survey.length < 0 ? 0 : survey.length] = 4;
    //           nextQuestion();
    //       } else if (QF.isToggled()) {
    //           nextQuestion();
    //       } else {
    //           changeSensor("rainfall");
    //       }
    //     }
    //     else if (event.keyCode == 75) {
    //       // k, wind speed
    //       if (Q1.isToggled() || Q2.isToggled() || Q3.isToggled()) {
    //           survey[survey.length < 0 ? 0 : survey.length] = 5;
    //           nextQuestion();
    //       } else if (QF.isToggled()) {
    //           nextQuestion();
    //       } else {
    //           changeSensor("wind_speed");
    //       }
    //     }
    //     else if (event.keyCode == 76) {
    //       // l, SURVEY
    //       takeSurvey();
    //     }
    }

    if (event.keyCode == 81) {
        // q, city up
        if (Q1.isToggled() || Q2.isToggled() || Q3.isToggled()) {
            takeSurvey();
        } else {
            changeCity(cities[(((cities.indexOf(city) - 1) % cities.length) + cities.length) % cities.length]);
        }
    } else if (event.keyCode == 65) {
        // a, city down
        if (Q1.isToggled() || Q2.isToggled() || Q3.isToggled()) {
            takeSurvey();
        } else {
            changeCity(cities[(cities.indexOf(city) + 1) % cities.length]);
        }
    }
});
