"use strict";

// const lanIP = `${window.location.hostname}:5000`;
// const lanIP = `127.0.0.1:5000`;
const lanIP = `192.168.168.169:5000`;
const socket = io(`http://${lanIP}`, {transports: ["polling", "websocket"] });

let htmlDevices, htmlXWaarde
let htmlJoystick, htmlJoystick1X, htmlJoystick1Y, htmlJoystick1SW, htmlJoystick2X, htmlJoystick2Y, htmlJoystick2SW
console.info(lanIP)


const listenToSocket = function(){
  console.info("hello!")
  socket.on('connect', function(){
    console.info('verbonden met socket webserver')
  })
  
  socket.on("B2F_connected", function(payload){
    console.info(payload)
    console.info(`eerste boodschap server: ${payload.message}`)
    // tot hier lukt alles
  })
  

  // socket.on('B2F_value_joy', function(jsonObject){
  //     console.info(jsonObject)
  //     // ${jsonObject.waarden.waarde}
  //     let htmlString = ""
  //     htmlString += `<div class="c-waarde js-xwaarde">
  //     waarden x-as: 0
  //     </div>
  //     <div class="c-waarde">
  //     waarden y-as: 321
  //     </div>
  //     <div class="c-waarde">
  //     hoeveel keer er op de knop is gedrukt: ${jsonObject.teller}
  //     </div>`
  //     htmlJoystick.innerHTML = htmlString
  //     // tot hier werkt het
  //     })

  //////////////////////////////___TEST___//////////////////////////////
  // joy 1
  socket.on('B2F_value_joy_1_sw', function(jsonObject){
    console.info(jsonObject)
    // ${jsonObject.waarden.waarde}
    let htmlString = ""
    htmlString += `
    <div class="c-waarde">
    hoeveel keer er op de knop is gedrukt: ${jsonObject.teller}
    </div>`
    htmlJoystick.innerHTML = htmlString
    })

  socket.on('B2F_value_joy_1_x', function(jsonObject){
    console.info(jsonObject, jsonObject.joy_1_x)
    // ${jsonObject.waarden.waarde}
    let htmlString = ""
    htmlString += `
    <div class="c-waarde">
    Joystick 1 X: ${jsonObject.joy_1_x}
    </div>`
    htmlJoystick1X.innerHTML = htmlString
    })

  socket.on('B2F_value_joy_1_y', function(jsonObject){
    console.info(jsonObject)
    // ${jsonObject.waarden.waarde}
    let htmlString = ""
    htmlString += `
    <div class="c-waarde">
    hoeveel keer er op de knop is gedrukt: ${jsonObject.teller}
    </div>`
    htmlJoystick.innerHTML = htmlString
    })

  //////////////////////////////___joy 2___//////////////////////////////
  socket.on('B2F_value_joy_2_sw', function(jsonObject){
    console.info(jsonObject)
    // ${jsonObject.waarden.waarde}
    let htmlString = ""
    htmlString += `
    <div class="c-waarde">
    hoeveel keer er op de knop is gedrukt: ${jsonObject.teller}
    </div>`
    htmlJoystick.innerHTML = htmlString
    })


  socket.on('B2F_value_joy_2_x', function(jsonObject){
    console.info(jsonObject)
    // ${jsonObject.waarden.waarde}
    let htmlString = ""
    htmlString += `
    <div class="c-waarde">
    hoeveel keer er op de knop is gedrukt: ${jsonObject.teller}
    </div>`
    htmlJoystick.innerHTML = htmlString
    })

  socket.on('B2F_value_joy_2_y', function(jsonObject){
    console.info(jsonObject)
    // ${jsonObject.waarden.waarde}
    let htmlString = ""
    htmlString += `
    <div class="c-waarde">
    hoeveel keer er op de knop is gedrukt: ${jsonObject.teller}
    </div>`
    htmlJoystick.innerHTML = htmlString
    })
}

const init = function(){
  console.info("DOM geladen")
  htmlDevices = document.querySelector('.js-devices')
  htmlJoystick = document.querySelector('.js-joystick')
  htmlJoystick1X = document.querySelector('.js-joystick1X')
  htmlJoystick1Y = document.querySelector('.js-joystick1Y')
  htmlJoystick1SW = document.querySelector('.js-joystick1SW')

  htmlJoystick2X = document.querySelector('.js-joystick2X')
  htmlJoystick2Y = document.querySelector('.js-joystick2Y')
  htmlJoystick2SW = document.querySelector('.js-joystick2SW')

  listenToSocket()
}

document.addEventListener('DOMContentLoaded', init);

