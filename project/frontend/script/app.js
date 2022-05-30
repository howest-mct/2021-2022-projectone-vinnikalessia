"use strict";

// const lanIP = `${window.location.hostname}:5000`;
// const lanIP = `127.0.0.1:5000`;
const lanIP = `192.168.168.169:5000`;
const socket = io(`http://${lanIP}`);

let htmlDevices, htmlJoystick, htmlXWaarde
console.info(lanIP)

const callbackJoyX = function(){
  handleData(`http://127.0.0.1:5000/api/v1/waarden`, showWaarden)
}

const showWaarden = function(jsonObject){
  console.info(jsonObject)
  let htmlString = ''
  for(const waarde of jsonObject){
    htmlString += `<div class="c-waarde js-xwaarde">
        waarden x-as: ${waarde}
    </div>`
  }
  htmlXWaarde.innerHTML += htmlString
  print("gedaan!!!")
}

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
  
  socket.on('B2F_value_joy_1', function(jsonObject){
    console.info("hallo?")
    console.info(jsonObject)
  })
}

const init = function(){
  console.info("DOM geladen")
  htmlDevices = document.querySelector('.js-devices')
  htmlJoystick = document.querySelector('.js-joystick')
  htmlXWaarde = document.querySelector('.js-xwaarde')

  listenToSocket()
}

document.addEventListener('DOMContentLoaded', init);

