var myData = {}; //object which will be used for getting data

//This funtion makes api call to get data, displays different buttons based on requirenment and displays the data in the table.
function displayData() {
  var uri = "http://localhost:8000/api/makeTable/temp";

  $.ajax({
    url: uri,
    dataType: "json",
    async: false,
    success: function (data) {
      console.log(data)
      myData = data;
    }
  });

  console.log(myData);
  createButtons();
  CreateTableFromJSON(JSON.parse(myData["Items"]));
}
var columns = [] 

// creation of buttons
function createButtons() {
  var max = document.createElement("button");
  var min = document.createElement("button");
  var chart = document.createElement("button");
  var t = document.createTextNode("Get Max Value");
  max.className = "btn btn-primary col-2 mr-2";
  min.className = "btn btn-primary col-2 mr-2";
  chart.className = "btn btn-primary col-2";
  max.appendChild(t);
  t = document.createTextNode("Get Min Value");
  min.appendChild(t);
  t = document.createTextNode("Get Graph");
  chart.appendChild(t);
  max.onclick = function () {
    getMaxValue();
  };
  min.onclick = function () {
    getMinValue();
  };
  chart.onclick = function () {
    drawGraph();
  };
  var div = document.getElementById("buttons");
  div.appendChild(max);
  div.appendChild(min);
  div.appendChild(chart);
}

//For getting max value in recieved data
function getMaxValue() {
  var div = document.getElementById("results");
  div.innerHTML = "<p> the maximum value is  " + myData['Max'] + " degree celsius  </p>";
}

//For getting min value in recieved data
function getMinValue() {
  var div = document.getElementById("results");
  div.innerHTML = "<p> the minimum value is  " + myData['Min'] + " degree celsius  </p>";
}

//It draws a graph of value of sensor against timestamp
function drawGraph() {
  var data = {
    x: myData['timestamp'],
    y: myData['temperature'],
    type: 'scatter'
  };
  console.log(data);

  Plotly.newPlot('graph', [data]);

}

// This function interpretes the json data to organize in the data in from of table.
function CreateTableFromJSON(myData) {
  console.log("Started");

  var myBooks = myData;
  var col = [];
  for (var i = 0; i < myBooks.length; i++) {
    for (var key in myBooks[i]) {
      if (col.indexOf(key) === -1) {
        col.push(key);
      }
    }
  }
  columns = col;
  // CREATE DYNAMIC TABLE.
  var table = document.createElement("table");
  table.className = "table table-striped";

  // CREATE HTML TABLE HEADER ROW USING THE EXTRACTED HEADERS ABOVE.

  var tr = table.insertRow(-1);                   // TABLE ROW.

  for (var i = 0; i < col.length; i++) {
    var th = document.createElement("th");      // TABLE HEADER.
    th.innerHTML = col[i];
    tr.appendChild(th);
  }

  // ADD JSON DATA TO THE TABLE AS ROWS.
  for (var i = 0; i < myBooks.length; i++) {

    tr = table.insertRow(-1);

    for (var j = 0; j < col.length; j++) {
      var tabCell = tr.insertCell(-1);
      tabCell.innerHTML = myBooks[i][col[j]];
    }
  }

  // FINALLY ADD THE NEWLY CREATED TABLE WITH JSON DATA TO A CONTAINER.
  var divContainer = document.getElementById("showData");
  divContainer.innerHTML = "";
  divContainer.appendChild(table);
  console.log("Ended");

}
function getAxis() {
  var myDiv = document.getElementById("data");

  document.write("Select the y-axis feature");
  var selectList = document.createElement("select");
  selectList.id = "mySelecty";
  myDiv.appendChild(selectList);

  for (var i = 0; i < array.length; i++) {
    if (typeof myData[columns[i]] == "number") {
      var option = document.createElement("option");
      option.value = array[i];
      option.text = array[i];
      selectList.appendChild(option);

    }
  }
  document.write("Select the x-axis feature");
  var selectList = document.createElement("select");
  selectList.id = "mySelectx";
  myDiv.appendChild(selectList);

  for (var i = 0; i < array.length; i++) {
    var option = document.createElement("option");
    option.value = array[i];
    option.text = array[i];
    selectList.appendChild(option);
  }

}
