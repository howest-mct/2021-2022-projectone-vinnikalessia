"use strict";

const lanIP = `${window.location.hostname}:5000`;
console.info(lanIP)
const socket = io(lanIP)

// #region ***  DOM references                           ***********
let htmlDevices, htmlJoystick, htmlWaarden
// #endregion

// #region ***  Callback-Visualisation - show___         ***********

// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********
// #endregion

// #region ***  Data Access - get___                     ***********
// #endregion

// #region ***  Event Listeners - listenTo___            ***********
const listenToSocket = function(){
  socket.on('connect', function(){
    console.info('verbonden met socket webserver')
  })
  socket.on('B2F_joy_value', function(jsonObject){
    // console.info("joystick: ", jsonObject.joystick)
  })
}
// #endregion

// #region ***  Init / DOMContentLoaded                  ***********
const init = function(){
  console.info("DOM loaded")
  htmlDevices = document.querySelector('.js-devices')
  htmlJoystick = document.querySelector('.js-joystick')
  htmlWaarden = document.querySelector('.js-waarden')

  listenToSocket()

}
// #endregion


// document.addEventListener('DOMContentLoaded', init);
document.addEventListener('DOMContentLoaded', init)
