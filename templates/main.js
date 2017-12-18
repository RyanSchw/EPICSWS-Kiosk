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

// Email formatted data

// Pull data from weather underground
func pullData() {
    jQuery(document).ready(function($) {
        $.ajax({
        url : "http://api.wunderground.com/api/" + API_KEY + "/geolookup/conditions/q/CA/San_Francisco.json",
        dataType : "jsonp",
        success : function(parsed_json) {
          var location = parsed_json['current_observation']['display_location']['full'];
          var measurements = parsed_json['current_observation'];
          var weather = measurements['weather']; // String, Overview of weather
          var temp_f = measurements['temp_f']; // Integer, Measured temperature in degrees F
          var humidity = measurements['relative_humidity']; // String, xx%, Relative humidity (%)
          var wind_dir = measurements['wind_dir']; // String, Wind direction (South, North, etc.)
          var wind_degrees = measurements['wind_degrees']; // Integer, Wind direction (0 degrees is North)
          var wind_mph = measurements['wind_mph']; // Integer, Wind speed in miles per hour
          var pressure_in = measurements['pressure_in']; // String, Barometric pressure in inch pounds?


        }
        });
    });
}
