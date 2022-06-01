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