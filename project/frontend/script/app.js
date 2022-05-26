"use strict";

// #region ***  DOM references                           ***********
// const lanIP = `${window.location.hostname}:5000`;
// const lanIP = `172.0.0.1:5000`;
const lanIP = `192.168.168.169:5000`;
console.info(lanIP)
const socket = io(lanIP)
// const socketio = io(`http://${lanIP}`);
// const socketio = io(`http://192.168.168.169:5000`);
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
