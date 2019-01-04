var status = 0; // to keep track wheter the testing is on or off
var d = document.getElementById("sel_interval"); 
interval = 2;
s = 0; //requests sent

r = 0; //responsed recieved
var Sensor;
uri = 'http://api.openweathermap.org/data/2.5/weather?appid=f6182a9874fa6e1a215f5a7489f8b3eb&q=Mumbai'; //default uri
testinterval = null;

//For starting and stopping the Test Process
function startTesting() {
  if (status == 1) {
    stopTesting();
    return;
  }
  else {
    document.getElementById("testbut").innerText = "Stop Testing";
    status = 1;
    e = document.getElementById("sel_sensor");
    uri = e.options[e.selectedIndex].value;
    Sensor = e.options[e.selectedIndex].innerText;
    testing();
    interval = parseInt(document.getElementById("sel_interval").value) * 1000 * 60;
    testinterval = setInterval(function () {
      console.log(interval);
      testing();
      cnt++;
    }, interval);
  }

}


function stopTesting() {
  console.log("In stop testing");
  status = 0;
  document.getElementById("testbut").innerText = "Start Testing";
  clearInterval(testinterval);
}

//Sends the requests continously after every interval selected by the user.
function testing() {
  s++;
  document.getElementById("s").innerHTML = s;
  var myData = {};

  console.log(uri);
  $.ajax({
    url: uri,
    dataType: "json",
    async: false,
    success: function (data) {
      myData['sensor'] = Sensor; // the sensor selected
      myData['temperature'] = (data['main']['temp']) - 273.15; //This must be refined
      myData['city'] = 'Mumbai';  //must be generalized
      //myData['value'] = 27; 
      myData['timestamp'] = js_yyyy_mm_dd_hh_mm_ss();
      console.log(js_yyyy_mm_dd_hh_mm_ss());
      tableData(myData);
      r = r + 1;
      console.log(myData);
      document.getElementById("r").innerHTML = r;
      // make a call to local API to handle AWS part
      $.ajax({
        type: 'POST',
        dataType: 'json',
        async: false,
        csrfmiddlewaretoken: "{{ csrf_token }}",
        contentType: 'application/json; charset=utf-8',
        url: 'http://localhost:8000/api/pushData/',
        data: JSON.stringify(myData),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        beforeSend: function (xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", '{{ csrf_token }}');
        },
        success: function (result) {

          console.log('yayy' + result);
        }
      });
    }

  });
  console.log(myData);



}

//function used to add rows of responsed recived.
function tableData(data) {

  var markup = "<tr><td>" + data['sensor'] + "</td><td>" + data['temperature'] + "</td><td>" + data['city'] + "</td><td>" +
    data['timestamp'] + "</td></tr>";
  $('table tbody').append(markup);
}
var cnt = 0;

//AJAX Requirement for posting data to rest API 
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

$.ajaxSetup({
  beforeSend: function (xhr, settings) {
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
      // Only send the token to relative URLs i.e. locally.
      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
  }
});

//to get the timestamp in required format.
function js_yyyy_mm_dd_hh_mm_ss() {
  now = new Date();
  year = "" + now.getFullYear();
  month = "" + (now.getMonth() + 1); if (month.length == 1) { month = "0" + month; }
  day = "" + now.getDate(); if (day.length == 1) { day = "0" + day; }
  hour = "" + now.getHours(); if (hour.length == 1) { hour = "0" + hour; }
  minute = "" + now.getMinutes(); if (minute.length == 1) { minute = "0" + minute; }
  second = "" + now.getSeconds(); if (second.length == 1) { second = "0" + second; }
  return year + "-" + month + "-" + day + "-  " + hour + ":" + minute + ":" + second;
}
