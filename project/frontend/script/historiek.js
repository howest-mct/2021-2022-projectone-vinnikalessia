"use strict";

// const lanIP = `${window.location.hostname}:5000`;
// const lanIP = `127.0.0.1:5000`;
const lanIP = `192.168.168.169:5000`;
const socket = io(`http://${lanIP}`, {transports: ["polling", "websocket"] });

let htmlDevices, htmlXWaarde, jsonData1, jsonData2, dataSpel
let htmlJoystick, htmlJoystick1X, htmlJoystick1Y, htmlJoystick1SW, htmlJoystick2X, htmlJoystick2Y, htmlJoystick2SW
let htmlKnop1, htmlKnop2, htmlKeuze, htmlKleur, htmlIP, htmlHistoriek
console.info(lanIP)

const listenToSocket = function(){
  console.info("hello!")
  socket.on('connect', function(){
    console.info('verbonden met socket webserver')
  })
  
  socket.on("B2F_connected", function(payload){
    console.info(payload)
    console.info(`eerste boodschap server: ${payload.message}`)
  })

  socket.on('B2F_games', function(jsonObject){
    console.info("😃")
    console.info(`en winnaar is: ${jsonObject.winnaar}`)
    console.info(jsonObject)
    if (jsonObject.winnaar == 'Rood'){
        jsonData1 ++
        // jsonData1.push(1)
    }
    else if (jsonObject.winnaar == 'Blauw'){
        // jsonData2.push(1)
        jsonData2 ++
    }
    dataSpel = [jsonData1, jsonData2]
    console.info(jsonData1, jsonData2)
    var options = {
        series: [{
        data: [jsonData1, jsonData2]
      }],
        chart: {
        height: 350,
        type: 'bar',
        events: {
          click: function(chart, w, e) {
          }
        }
      },
      colors: ["#FF1654", "#247BA0"],
      plotOptions: {
        bar: {
          columnWidth: '25%',
          distributed: true,
        }
      },
      dataLabels: {
        enabled: true
      },
      legend: {
        show: true
      },
      xaxis: {
        categories: [
          ['Speler 1'],
          ['Speler 2']
        ],
        labels: {
          style: {
            colors: ["#FF1654", "#247BA0"],
            fontSize: '12px'
          }
        }
      }
      };

    var chart = new ApexCharts(document.querySelector(".js-historiek"), options);
    chart.render();
    })
}

const init = function(){
    console.info("DOM geladen")
    htmlHistoriek = document.querySelector('.js-historiek')
    jsonData1 = 0
    jsonData2 = 0
    listenToSocket()
}

document.addEventListener('DOMContentLoaded', init);

