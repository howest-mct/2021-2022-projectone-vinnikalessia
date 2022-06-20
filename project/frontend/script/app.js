"use strict";

// const lanIP = `${window.location.hostname}:5000`;
// const lanIP = `127.0.0.1:5000`;
const lanIP = `192.168.168.169:5000`;
const socket = io(`http://${lanIP}`, {transports: ["polling", "websocket"] });

let htmlDevices, htmlXWaarde
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

  //////////////////////////////___JOYSTICKS___//////////////////////////////
  ////////////___joy 1___////////////
  socket.on('B2F_value_joy_1_sw', function(jsonObject){
    console.info(jsonObject)
    let htmlString = ""
    htmlString += `
    <div class="c-waarde">
    hoeveel keer er op de knop is gedrukt: ${jsonObject.teller}
    </div>`
    htmlJoystick1SW.innerHTML = htmlString
    })

  socket.on('B2F_value_joy_1_x', function(jsonObject){
    console.info(jsonObject)
    let htmlString = ""
    htmlString += `
    <div class="c-waarde">
    waarden x-as: ${jsonObject.joy_1_x}
    </div>`
    htmlJoystick1X.innerHTML = htmlString
    })

  socket.on('B2F_value_joy_1_y', function(jsonObject){
    console.info(jsonObject)
    let htmlString = ""
    htmlString += `
    <div class="c-waarde">
    waarden y-as: ${jsonObject.joy_1_y}
    </div>`
    htmlJoystick1Y.innerHTML = htmlString
  })
  
  ////////////___joy 2___////////////
  socket.on('B2F_value_joy_2_x', function(jsonObject){
    console.info(jsonObject)
    let htmlString = ""
    htmlString += `
    <div class="c-waarde">
    waarden x-as: ${jsonObject.joy_2_x}
    </div>`
    htmlJoystick2X.innerHTML = htmlString
  })

  socket.on('B2F_value_joy_2_y', function(jsonObject){
    console.info(jsonObject)
    let htmlString = ""
    htmlString += `
    <div class="c-waarde">
    waarden y-as: ${jsonObject.joy_2_y}
    </div>`
    htmlJoystick2Y.innerHTML = htmlString
  })

  socket.on('B2F_value_joy_2_sw', function(jsonObject){
    console.info(jsonObject)
    let htmlString = ""
    htmlString += `
    <div class="c-waarde">
    hoeveel keer er op de knop is gedrukt: ${jsonObject.teller}
    </div>`
    htmlJoystick2SW.innerHTML = htmlString
    })
  
  ////////////___knoppen___////////////
  socket.on('B2F_value_knopup1', function(jsonObject){
    console.info("up")
    console.info(jsonObject)
    let htmlString = ""
    htmlString += `
    <div class="c-waarde js-knop1">
    1 verdieping naar boven
    </div>`
    htmlKnop1.innerHTML = htmlString
  })
  
  socket.on('B2F_value_knopdown1', function(jsonObject){
    console.info("down")
    console.info(jsonObject)
    let htmlString = ""
    htmlString += `<div class="c-waarde js-knop1">
    1 verdieping naar beneden
    </div>`
    htmlKnop1.innerHTML = htmlString
  })
  
  socket.on('B2F_value_knopup2', function(jsonObject){
    console.info("up")
    console.info(jsonObject)
    let htmlString = ""
    htmlString += `
    <div class="c-waarde js-knop2">
    1 verdieping naar boven
    </div>`
    htmlKnop2.innerHTML = htmlString
  })

  socket.on('B2F_value_knopdown2', function(jsonObject){
    console.info("down")
    console.info(jsonObject)
    let htmlString = ""
    htmlString += `<div class="c-waarde js-knop2">
    1 verdieping naar beneden
    </div>`
    htmlKnop2.innerHTML = htmlString
  })

  ////////////___oled___////////////
  socket.on('B2F_choice_oled', function(jsonObject){
    console.info(jsonObject)
    let htmlString = ''
    if (jsonObject.keuze == 0){
      htmlString = `<div class="o-layout__item js-keuze">
      We spelen tot 1
      </div>`
    }
    else if (jsonObject.keuze == 1){
      htmlString = `<div class="o-layout__item js-keuze">
      We spelen tot 3
      </div>`
    }
    else if (jsonObject.keuze == 2){
      htmlString = `<div class="o-layout__item js-keuze">
      We spelen tot 5
      </div>`
    }
    else if (jsonObject.keuze == 3){
      htmlString = `<div class="o-layout__item js-keuze">
      We spelen tot 9
      </div>`
    }
    htmlKeuze.innerHTML = htmlString
  })

  socket.on('B2F_player', function(jsonObject){
    console.info(jsonObject)
    let htmlString = ''
    htmlString =`<div class="o-layout__item js-beurtkleur">
    <p>het is aan: ${jsonObject.speler}</p>
    </div>`
    htmlKleur.innerHTML = htmlString
  })

  socket.on('B2F_show_ip', function(jsonObject){
    console.info(jsonObject)
    let htmlString = ''
    htmlString =`<div class="o-layout__item js-ip">
    <p>
        IP-adres: ${jsonObject.ip_adres}
    </p>
    </div>`
    htmlIP.innerHTML = htmlString
  })
}

const init = function(){
  console.info("DOM geladen")
  htmlDevices = document.querySelector('.js-devices')
  // htmlJoystick = document.querySelector('.js-joystick') // wrsch niet nodig
  htmlJoystick1X = document.querySelector('.js-joystick1X')
  htmlJoystick1Y = document.querySelector('.js-joystick1Y')
  htmlJoystick1SW = document.querySelector('.js-joystick1SW')

  htmlJoystick2X = document.querySelector('.js-joystick2X')
  htmlJoystick2Y = document.querySelector('.js-joystick2Y')
  htmlJoystick2SW = document.querySelector('.js-joystick2SW')

  htmlKnop1 = document.querySelector('.js-knop1')
  htmlKnop2 = document.querySelector('.js-knop2')

  htmlKeuze = document.querySelector('.js-keuze')
  htmlKleur = document.querySelector('.js-beurtkleur')
  htmlIP = document.querySelector('.js-ip')


  listenToSocket()
}

document.addEventListener('DOMContentLoaded', init);

