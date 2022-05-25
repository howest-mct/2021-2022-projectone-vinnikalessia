"use strict";

// #region ***  DOM references                           ***********
let htmlDevice, htmlJoystick
// #endregion

// #region ***  Callback-Visualisation - show___         ***********
const showDevices = function(jsonObject){
  try{
    console.info(jsonObject)
    let htmlstring = '';
    for(const device of jsonObject.devices){
      htmlstring += `<div class="o-layout__item u-1-of-2-bp3 js-${device.devicenaam}">
      <h2>${device.devicenaam}:</h2>
      <div class="c-waarde">
          waarden x-as: 123
      </div>
      <div class="c-waarde">
          waarden y-as: 321
      </div>
      <div class="c-waarde">
          hoeveel keer er op de knop is gedrukt: 2
      </div>
  </div>`;
    }
    htmlDevice.innerHTML = htmlstring
    // getWaarden()
  }
  catch (err){
    console.error(err)
  }
}

// const showWaarden = function(jsonObject){
//   try{
//     console.info(jsonObject)

//   }
//   catch(err){
//     console.info(err)
//   }
// }

// #endregion

// #region ***  Callback-No Visualisation - callback___  ***********
// #endregion

// #region ***  Data Access - get___                     ***********
const getDevices = function(){
  const url = 'http://192.168.168.169:5000/api/v1/devices/'
  handleData(url, showDevices)
}

// const getWaarden = function(){
//   const url = 'http://192.168.168.169:5000/api/v1/waarden/'
//   handleData(url, showWaarden)
// }
// #endregion

// #region ***  Event Listeners - listenTo___            ***********
// #endregion

// #region ***  Init / DOMContentLoaded                  ***********

// #endregion

const init = function(){
  console.info("😁")
  // htmlJoystick = document.querySelector('.js-joystick')
  htmlDevice = document.querySelector('.js-devices')

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
