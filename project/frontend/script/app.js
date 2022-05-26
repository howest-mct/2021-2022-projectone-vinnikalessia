"use strict";

// const lanIP = `${window.location.hostname}:5000`;
const lanIP = `192.168.168.169:5000`;
console.info(lanIP)
const socket = io(`http://${lanIP}`);

let htmlDevices, htmlJoystick, htmlXWaarde


const listenToSocket = function(){
  console.info("hello!")
  socket.on('connect', function(){
    console.info('verbonden met socket webserver')
  })

  socket.on('B2F_value_joy_1', function(jsonObject){
    console.info("live joystick: ", jsonObject.x_waarde)
    value_x = jsonObject.x_waarde
    let htmlstring = `${value_x}`
    htmlXWaarde.innerhtml = htmlstring
    console.info(value_x)
  })
}

const init = function(){
  console.info("DOM geladen")
  htmlDevices = document.querySelector('.js-devices')
  htmlJoystick = document.querySelector('.js-joystick')
  htmlXWaarde = document.querySelector('.js-xwaarde')

  listenToSocket()
}

document.addEventListener('DOMContentLoaded', init());

