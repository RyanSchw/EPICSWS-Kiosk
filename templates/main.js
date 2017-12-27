/**
 * Project: EPICS IS WS Kiosk Web Application
 * Program name: main.js
 * Author: Ryan Schwartz
 *
 * Purpose:
 */


// Page load event
window.addEventListener('load', function(e) {
    // Page load
}, false);

// Variable declarations
var API_KEY = ""
var API_CALLS = 0
var temperature_values = [];

// Email formatted data

// Pull data from weather underground
// @param Date: Formatted as YYYYMMDD
function pullData() {
    console.log(document.getElementById('day1').value);
    day = document.getElementById('day1').value;
    jQuery(document).ready(function($) {
        $.ajax({
            url : "http://api.wunderground.com/api/" + API_KEY + "/history_" + day + "/q/CA/San_Francisco.json",
            dataType : "jsonp",
            async: false,
            success : function(parsed_json) {
                API_CALLS++;
                console.log(parsed_json);
                graphChart(formatTemperature(parsed_json));
            }
        });
    });
}

// @param Parsed JSON
// @return Array of temperature values
function formatTemperature(json) {
    var tempList = [];
    var observationList = json['history']['observations'];
    for (i = 0; i < observationList.length; i++) {
        var t = observationList[i]['tempi'];
        tempList[i] = parseFloat(t);
    }
    return tempList;
}

// TODO: FIX FUNCTIONS
// function validReturn(parsed_json) {
//     if parsed_json['response'] != null {
//         if parsed_json['error'] != null {
//             if parsed_json['type'] != null {
//                 if parsed_json['type'] == "keynotfound" {
//                     // KEY NOT FOUND
//                     jserror("JSON Error: keynotfound");
//                     return;
//                 }
//             }
//             jserror("JSON Error");
//         }
//     }
// }
//
// function jserror(errormsg) {
//     // TODO: Console.log errors with error messages
//     console.error(errormsg);
// }
