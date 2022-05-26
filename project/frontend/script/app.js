"use strict";

const lanIP = `${window.location.hostname}:5000`;
const socket = io(lanIP)
// const socket = io(`http://${lanIP}`);

let htmlDevices, htmlJoystick, htmlXWaarde


const listenToSocket = function(){
  console.info("hello!")
  socket.on('connect', function(){
    console.info('verbonden met socket webserver')
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

