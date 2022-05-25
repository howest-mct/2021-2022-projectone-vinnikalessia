"use strict";

// #region ***  DOM references                           ***********
let htmlDevice, htmlJoystick
// #endregion

// #region ***  Callback-Visualisation - show___         ***********
const showDevices = function(jsonObject){
  try{
    console.info(jsonObject)
    


  }
  catch (err){
    console.error(err)
  }
}

// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********
// #endregion

// #region ***  Data Access - get___                     ***********
const getDevices = function(){
  const url = 'http://192.168.168.169:5000/api/v1/devices/'
  handleData(url, showDevices)
}
// #endregion

// #region ***  Event Listeners - listenTo___            ***********
// #endregion

// #region ***  Init / DOMContentLoaded                  ***********

// #endregion

const init = function(){
  console.info("😁")
  // htmlJoystick = document.querySelector('.js-joystick')
  // htmlDevice = document.querySelector('.js-devices')

  // if (htmlDevice){
  //   console.info(htmlDevice)
  //   getDevices()
  getDevices()
  
}

// document.addEventListener('DOMContentLoaded', init);
document.addEventListener('DOMContentLoaded', function(){
  console.info('DOM geladen')
  init()
})
