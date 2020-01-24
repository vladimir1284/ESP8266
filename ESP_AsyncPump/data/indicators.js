function ge(s) { return document.getElementById(s); }

uTank = {
    min_level: 40,
    canvasID: 'upper_tank',
    capacity: 550,
    labelID: "upper_volume",
    label: "Tanque Elevado",
    yc: 0,
    xc: 0,
    h: 0,
    w: 0,
    min: 0,
    restart: 0,
    height: 0,
    gap: 0,
}
lTank = {
    min_level: 25,
    canvasID: 'lower_tank',
    capacity: 200,
    labelID: "lower_volume",
    label: "Cisterna",
    yc: 0,
    xc: 0,
    h: 0,
    w: 0,
    min: 0,
    restart: 0,
    height: 0,
    gap: 0,
}
myPump = {
    state: 0,
    animationStage: 0,
    canvasID: 'pump',
    labelID: 'pump_state',
    Tmax: 0,
    startDelay: 0,
    ctx: null,
    yc: 0,
    xc: 0,
    h: 0,
    w: 0,
}
mvSensor = {
    state: 0,
    canvasID: 'movement',
    labelID: 'movement_state',
    ctx: null,
    yc: 0,
    xc: 0,
    h: 0,
    w: 0,
    has_luminosity: true,
    luminosity: 30
}
myLight = {
    state: 0,
    canvasID: 'light',
    labelID: 'light_state',
    ctx: null,
    yc: 0,
    xc: 0,
    h: 0,
    w: 0,
}
myDoor = {
    state: 0,
    canvasID: 'door',
    labelID: 'door_state',
    ctx: null,
    yc: 0,
    xc: 0,
    h: 0,
    w: 0,
}

function drawUpperTankTemplate(tank) {
    let canvas = ge(tank.canvasID);
    if (canvas.getContext) {
        const xc = 0.5 * canvas.width;
        const yc = 0.5 * canvas.height;
        let h = 0.8 * canvas.height;
        let w = 0.7 * h;
        if (w > (0.95 * canvas.width)) {
            w = 0.95 * canvas.width;
            h = w / 0.7;
        }
        tank.h = h;
        tank.w = w;
        tank.xc = xc;
        tank.yc = yc;

        let ctx = canvas.getContext('2d');
        ctx.fillStyle = "#000000";
        ctx.strokeRect(xc - w / 2, 0.2 * h, w, h);
        ctx.fillRect(xc - w / 4, 0.1 * h, w / 2, 0.1 * h);
    }
}

function animatePump() {
    const x0 = myPump.xc - 0.32 * myPump.w;
    const w0 = 3 * myPump.w / 40;
    if (myPump.state == 1) {
        if (ge(myPump.labelID).innerHTML = "Apagada") {
            ge(myPump.labelID).innerHTML = "Encendida";
        }
        myPump.ctx.fillStyle = "#0000FF";
        switch (myPump.animationStage) {
            case 0:
                myPump.ctx.clearRect(x0 - 1, myPump.yc
                    - 13 * myPump.h / 40, w0 + 1, 20 * myPump.h / 40);
                myPump.animationStage = 1;
                break;
            case 1:
                myPump.ctx.fillRect(x0, myPump.yc
                    - 3 * myPump.h / 40, w0, 10 * myPump.h / 40);
                myPump.animationStage = 2;
                break;
            case 2:
                myPump.ctx.fillRect(x0, myPump.yc
                    - 13 * myPump.h / 40, w0, 10 * myPump.h / 40);
                myPump.animationStage = 0;
                break;
        }
    } else {
        if (ge(myPump.labelID).innerHTML = "Encendida") {
            ge(myPump.labelID).innerHTML = "Apagada";
        }
        myPump.ctx.clearRect(x0 - 1, myPump.yc
            - 13 * myPump.h / 40, w0 + 1, 20 * myPump.h / 40);
    }
    setTimeout(animatePump, 500);
}

function drawPumpTemplate(pump) {
    let canvas = ge(pump.canvasID);
    if (canvas.getContext) {
        const xc = 0.5 * canvas.width;
        const yc = 0.5 * canvas.height;
        let w = 0.8 * canvas.width;
        let h = w;
        if (h > (0.8 * canvas.height)) {
            h = 0.8 * canvas.height;
            w = h;
        }
        pump.h = h;
        pump.w = w;
        pump.xc = xc;
        pump.yc = yc;
        const pxl = w / 48;
        const x0 = xc - 0.5 * w;
        const y0 = 0.2 * h;

        let ctx = canvas.getContext('2d');
        pump.ctx = ctx;

        ctx.beginPath();
        ctx.translate(x0, y0)
        ctx.moveTo(5 * pxl, 0);
        ctx.lineTo(8 * pxl, 0);
        ctx.lineTo(8 * pxl, 14 * pxl);
        ctx.lineTo(5 * pxl, 15 * pxl);
        ctx.lineTo(5 * pxl, 30 * pxl);
        ctx.lineTo(8 * pxl, 31 * pxl);
        ctx.lineTo(13 * pxl, 31 * pxl);
        ctx.moveTo(16 * pxl, 0);
        ctx.lineTo(13 * pxl, 0);
        ctx.lineTo(13 * pxl, 0);
        ctx.lineTo(13 * pxl, 34 * pxl);
        ctx.lineTo(16 * pxl, 34 * pxl);
        ctx.lineTo(21 * pxl, 28 * pxl);
        ctx.lineTo(24 * pxl, 28 * pxl);
        ctx.lineTo(25 * pxl, 32 * pxl);
        ctx.lineTo(46 * pxl, 32 * pxl);
        ctx.lineTo(47 * pxl, 31 * pxl);
        ctx.lineTo(47 * pxl, 15 * pxl);
        ctx.lineTo(46 * pxl, 14 * pxl);
        ctx.lineTo(25 * pxl, 14 * pxl);
        ctx.lineTo(24 * pxl, 18 * pxl);
        ctx.lineTo(21 * pxl, 18 * pxl);
        ctx.lineTo(16 * pxl, 12 * pxl);
        ctx.lineTo(13 * pxl, 12 * pxl);
        ctx.moveTo(29 * pxl, 14 * pxl);
        ctx.lineTo(29 * pxl, 28 * pxl);
        ctx.moveTo(32 * pxl, 27 * pxl);
        ctx.lineTo(41 * pxl, 27 * pxl);
        ctx.moveTo(32 * pxl, 23 * pxl);
        ctx.lineTo(41 * pxl, 23 * pxl);
        ctx.moveTo(32 * pxl, 19 * pxl);
        ctx.lineTo(41 * pxl, 19 * pxl);
        ctx.moveTo(43 * pxl, 10 * pxl);
        ctx.lineTo(43 * pxl, 8 * pxl);
        ctx.lineTo(31 * pxl, 8 * pxl);
        ctx.lineTo(29 * pxl, 10 * pxl);
        ctx.moveTo(30 * pxl, 35 * pxl);
        ctx.lineTo(26 * pxl, 38 * pxl);
        ctx.lineTo(24 * pxl, 38 * pxl);
        ctx.lineTo(24 * pxl, 40 * pxl);
        ctx.lineTo(46 * pxl, 40 * pxl);
        ctx.lineTo(46 * pxl, 38 * pxl);
        ctx.lineTo(44 * pxl, 38 * pxl);
        ctx.lineTo(40 * pxl, 35 * pxl);
        ctx.strokeRect(0, 20 * pxl, 5 * pxl, 6 * pxl);
        ctx.stroke()
        ctx.translate(-x0, -y0)
    }
}

function updateLightValue(value, light) {
    const pxl = light.w / 48;
    ctx = light.ctx
    xc = light.xc
    yc = light.yc
    if (value) {
        light.state = 1
        ge(light.labelID).innerHTML = "Encendida"
        ctx.fillStyle = "#fafd08"
        ctx.beginPath()
        ctx.translate(xc, yc - 5 * pxl)
        ctx.arc(0, 0, 12 * pxl, 3 * Math.PI / 4, Math.PI / 4)
        ctx.lineTo(6 * pxl, 15.5 * pxl)
        ctx.lineTo(-6 * pxl, 15.5 * pxl)
        ctx.closePath()
        ctx.fill()
        for (i = 0; i < 5; i++) {
            ctx.fillRect(14 * pxl, -pxl, 4 * pxl, 2 * pxl)
            ctx.rotate(- Math.PI / 4)
        }
        ctx.fillStyle = "#000000"
        ctx.rotate(5 * Math.PI / 4)
        ctx.translate(-xc, -yc + 5 * pxl)
    } else {
        light.state = 0
        ge(light.labelID).innerHTML = "Apagada"
        ctx.clearRect(0, 0, 2 * xc, 2 * yc)
        drawLightTemplate(light)
    }

}

function drawLightTemplate(light) {
    let canvas = ge(light.canvasID);
    if (canvas.getContext) {
        const xc = 0.5 * canvas.width;
        const yc = 0.5 * canvas.height;
        let w = 0.8 * canvas.width;
        let h = w;
        if (h > (0.8 * canvas.height)) {
            h = 0.8 * canvas.height;
            w = h;
        }
        light.h = h;
        light.w = w;
        light.xc = xc;
        light.yc = yc;
        const pxl = w / 48;

        let ctx = canvas.getContext('2d');
        light.ctx = ctx

        ctx.beginPath()
        ctx.translate(xc, yc - 5 * pxl)
        ctx.arc(0, 0, 12 * pxl, 3 * Math.PI / 4, Math.PI / 4)
        ctx.lineTo(6 * pxl, 15.5 * pxl)
        ctx.lineTo(-6 * pxl, 15.5 * pxl)
        ctx.closePath()
        ctx.stroke()
        ctx.beginPath()
        ctx.fillRect(-5 * pxl, 17 * pxl, 10 * pxl, 2 * pxl)
        ctx.fillRect(-5 * pxl, 20 * pxl, 10 * pxl, 2 * pxl)
        ctx.beginPath()
        ctx.arc(0, 18.4 * pxl, 7 * pxl, Math.PI / 4, 3 * Math.PI / 4)
        ctx.fill()
        ctx.translate(-xc, -yc + 5 * pxl)
    }
}

function drawDoorTemplate(door) {
    let canvas = ge(door.canvasID);
    if (canvas.getContext) {
        const xc = 0.5 * canvas.width;
        const yc = 0.5 * canvas.height;
        let w = 0.8 * canvas.width;
        let h = w;
        if (h > (0.8 * canvas.height)) {
            h = 0.8 * canvas.height;
            w = h;
        }
        door.h = h;
        door.w = w;
        door.xc = xc;
        door.yc = yc;
        const pxl = w / 100;

        let ctx = canvas.getContext('2d');
        door.ctx = ctx
        ctx.lineWidth = 2
        ctx.translate(xc / 2, yc / 4)
        if (door.state) {
            ctx.beginPath()
            ctx.moveTo(78 * pxl, 86 * pxl)
            ctx.lineTo(87 * pxl, 86 * pxl)
            ctx.lineTo(87 * pxl, 11 * pxl)
            ctx.lineTo(64 * pxl, 11 * pxl)
            ctx.lineTo(78 * pxl, 18 * pxl)
            ctx.lineTo(78 * pxl, 86 * pxl)
            ctx.lineTo(49 * pxl, 95 * pxl)
            ctx.lineTo(49 * pxl, 5 * pxl)
            ctx.lineTo(64 * pxl, 11 * pxl)
            ctx.moveTo(49 * pxl, 18 * pxl)
            ctx.lineTo(42 * pxl, 18 * pxl)
            ctx.lineTo(42 * pxl, 86 * pxl)
            ctx.lineTo(34 * pxl, 86 * pxl)
            ctx.lineTo(34 * pxl, 40 * pxl)
            ctx.moveTo(34 * pxl, 26 * pxl)
            ctx.lineTo(34 * pxl, 11 * pxl)
            ctx.lineTo(49 * pxl, 11 * pxl)

            ctx.moveTo(56 * pxl, 47 * pxl)
            ctx.lineTo(56 * pxl, 61 * pxl)
        } else {
            ctx.strokeRect(34 * pxl, 11 * pxl, 53 * pxl, 75 * pxl)
            ctx.strokeRect(42 * pxl, 18 * pxl, 36 * pxl, 68 * pxl)
            ctx.clearRect(30 * pxl, 25 * pxl, 5 * pxl, 13 * pxl)
            ctx.moveTo(49 * pxl, 47 * pxl)
            ctx.lineTo(49 * pxl, 57 * pxl)
        }
        ctx.moveTo(37 * pxl, 29 * pxl)
        ctx.lineTo(37 * pxl, 36 * pxl)
        ctx.moveTo(31 * pxl, 29 * pxl)
        ctx.lineTo(31 * pxl, 36 * pxl)
        ctx.stroke()
        ctx.beginPath()
        ctx.arc(34 * pxl, 29 * pxl, 3 * pxl, Math.PI, 2 * Math.PI)
        ctx.arc(34 * pxl, 36 * pxl, 3 * pxl, 0, Math.PI)
        ctx.stroke()
        ctx.beginPath()
        ctx.moveTo(25 * pxl, 49 * pxl)
        ctx.lineTo(18 * pxl, 56 * pxl)
        ctx.moveTo(23 * pxl, 33 * pxl)
        ctx.lineTo(13 * pxl, 33 * pxl)
        ctx.moveTo(25 * pxl, 17 * pxl)
        ctx.lineTo(19 * pxl, 10 * pxl)
        ctx.stroke()

        ctx.translate(-xc / 2, -yc / 4)
    }
}

function updateDoorValue(value, door) {
    if (value != door.state) {
        door.state = value
        ctx = door.ctx
        w = door.w
        xc = door.xc
        yc = door.yc
        pxl = w / 100
        ctx.clearRect(xc / 3, yc / 5, 150 * pxl, 110 * pxl)
        switch (value) {
            case 0:
                ge(door.labelID).innerHTML = "Cerrada"
                drawDoorTemplate(door)
                break
            case 1:
                ge(door.labelID).innerHTML = "Abierta"
                drawDoorTemplate(door)
                break
            default:
                ge(door.labelID).innerHTML = "Error"
                drawDoorTemplate(door)
                ctx.strokeStyle = "#ff0000"
                ctx.strokeRect(xc / 2, yc / 4, xc, 1.6 * yc)
                ctx.strokeStyle = "#000000"
                break
        }
    }
}

function drawMovementTemplate(mv) {
    let canvas = ge(mv.canvasID);
    if (canvas.getContext) {
        const xc = 0.5 * canvas.width;
        const yc = 0.5 * canvas.height;
        let w = 0.8 * canvas.width;
        let h = w;
        if (h > (0.8 * canvas.height)) {
            h = 0.8 * canvas.height;
            w = h;
        }
        mv.h = h;
        mv.w = w;
        mv.xc = xc;
        mv.yc = yc;
        const pxl = w / 48;

        let ctx = canvas.getContext('2d');
        mv.ctx = ctx
        // Luminosity sensor
        if (mv.has_luminosity) {
            ctx.beginPath()
            ctx.lineWidth = 4
            ctx.arc(90 * pxl, 20 * pxl, 6 * pxl, 0, 2 * Math.PI)
            ctx.stroke()

            ctx.beginPath()
            ctx.translate(90 * pxl, 20 * pxl)
            for (i = 0; i < 8; i++) {
                ctx.fillRect(8 * pxl, -pxl, 4 * pxl, 2 * pxl)
                ctx.rotate(Math.PI / 4)
            }
            ctx.translate(-90 * pxl, -20 * pxl)

            // indicator bar
            updateLuminosityValue(mv.luminosity, mv)
        } else {
            ctx.translate(2 * w / 3, 0);
        }

        // Movement Sensor
        ctx.beginPath();
        ctx.moveTo(30 * pxl, 50 * pxl);
        ctx.lineTo(30 * pxl, 42 * pxl);
        ctx.lineTo(37 * pxl, 37 * pxl);
        ctx.lineTo(34 * pxl, 26 * pxl);
        ctx.lineTo(41 * pxl, 26 * pxl);
        ctx.lineTo(45 * pxl, 27 * pxl);
        ctx.lineTo(49 * pxl, 31 * pxl);
        ctx.lineTo(48 * pxl, 33 * pxl);
        ctx.lineTo(44 * pxl, 29 * pxl);
        ctx.lineTo(41 * pxl, 28 * pxl);
        ctx.lineTo(42 * pxl, 38 * pxl);
        ctx.lineTo(34 * pxl, 43 * pxl);
        ctx.lineTo(32 * pxl, 49 * pxl);
        ctx.closePath()
        ctx.fill()

        ctx.beginPath();
        ctx.arc(35 * pxl, 21 * pxl, 3 * pxl, 0, 2 * Math.PI)
        ctx.fill()

        ctx.fillRect(29 * pxl, 31 * pxl, 6 * pxl, 2 * pxl)

        ctx.beginPath();
        ctx.moveTo(41 * pxl, 40 * pxl)
        ctx.lineTo(43 * pxl, 39 * pxl)
        ctx.lineTo(49 * pxl, 48 * pxl)
        ctx.lineTo(49 * pxl, 49 * pxl)
        ctx.lineTo(47 * pxl, 49 * pxl)
        ctx.closePath()
        ctx.fill()

        ctx.beginPath();
        ctx.arc(18 * pxl, 11 * pxl, 3 * pxl, 0, Math.PI)
        ctx.fill()

        ctx.lineWidth = 3
        for (i = 0; i < 4; i++) {
            ctx.beginPath()
            ctx.arc(18 * pxl, 11 * pxl, (6 + 4 * i) * pxl, Math.PI / 12, 7 * Math.PI / 12)
            ctx.stroke()
        }

        if (!mv.has_luminosity) {
            ctx.translate(-2 * w / 3, 0);
        }
    }
}

function updateLuminosityValue(value, mv) {
    if (value < 0) {
        value = 0
    }
    if (value > 100) {
        value = 100
    }
    mv.luminosity = value
    value = Math.round(value / 10)
    ctx = mv.ctx
    w = mv.w
    pxl = w / 48
    ctx.beginPath()
    ctx.translate(71 * pxl, 45 * pxl)
    ctx.clearRect(-pxl, -pxl, 45 * pxl, 5 * pxl)
    for (i = 0; i < 10; i++) {
        if (value > i) {
            ctx.fillStyle = "#000000"
        } else {
            ctx.fillStyle = "#ababab"
        }
        ctx.fillRect(i * 4 * pxl, 0, 2 * pxl, 3 * pxl)
    }
    ctx.fillStyle = "#000000"
    ctx.translate(-71 * pxl, -45 * pxl)
}

function updateMovementValue(value, mv) {
    ctx = mv.ctx
    w = mv.w
    pxl = w / 48
    if (!mv.has_luminosity) {
        ctx.translate(2 * w / 3, 0);
    }
    if (value) {
        ctx.strokeStyle = "#ff0000"
        ctx.strokeRect(10 * pxl, 5 * pxl, 45 * pxl, 50 * pxl)
        ctx.strokeStyle = "#000000"
        if (!mv.has_luminosity) {
            ctx.translate(-2 * w / 3, 0);
        }
    }
    else {
        ctx.clearRect(9 * pxl, 4 * pxl, 47 * pxl, 52 * pxl)
        if (!mv.has_luminosity) {
            ctx.translate(-2 * w / 3, 0);
        }
        drawMovementTemplate(mv)

    }
}

function drawLowerTankTemplate(tank) {
    let canvas = ge(tank.canvasID);
    if (canvas.getContext) {
        const xc = 0.5 * canvas.width;
        const yc = 0.5 * canvas.height;
        let w = 0.8 * canvas.width;
        let h = 0.6 * w;
        if (h > (0.8 * canvas.height)) {
            h = 0.8 * canvas.height;
            w = h / 0.6;
        }
        tank.h = h;
        tank.w = w;
        tank.xc = xc;
        tank.yc = yc;

        let ctx = canvas.getContext('2d');
        ctx.beginPath();
        ctx.moveTo(xc - w / 2, 0.2 * h);
        ctx.lineTo(xc - w / 2, 1.2 * h);
        ctx.lineTo(xc + w / 2, 1.2 * h);
        ctx.lineTo(xc + w / 2, 0.2 * h);
        ctx.stroke();
    }
}

function updateTankValue(value, tank) {
    if (value >= 0 && value <= 100) {
        let texto = value * tank.capacity / 100 + " lts";
        ge(tank.labelID).innerHTML = texto;

        let canvas = ge(tank.canvasID);
        if (canvas.getContext) {
            let ctx = canvas.getContext('2d');
            if (value > tank.min_level) {
                ctx.fillStyle = "#0000FF";
            } else {
                ctx.fillStyle = "#FF0000";
            }

            ctx.clearRect(tank.xc - tank.w / 2 + 1, 0.2 * tank.h + 1, tank.w - 2,
                tank.h - 2);
            ctx.fillRect(tank.xc - tank.w / 2 + 1,
                (1 - value / 100) * (tank.h - 2) + 0.2 * tank.h + 1,
                tank.w - 2, (value / 100) * (tank.h - 2));
        }
    } else {
        ge(tank.labelID).innerHTML = "Valor incorrecto!!";
    }
}

function configure_upperTank() {
    configuredTank = uTank;
    configureTank();
}

function configure_lowerTank() {
    configuredTank = lTank;
    configureTank();
}

function configureTank() {
    w3_close();
    ge("tank_config").style.display = "block";
    ge("config_tank_label").innerHTML = configuredTank.label;
    // Capacity
    ge("inputCapacity").value = configuredTank.capacity + "lts";
    // Height
    ge("inputHeight").value = configuredTank.height + "cm";
    // Gap
    ge("inputGap").value = configuredTank.gap + "cm";
    // Restart
    ge("slideRestart").value = configuredTank.restart;
    ge("labelRestart").innerHTML = "Reinicio: " + configuredTank.restart + "%";
    // Min
    ge("slideMin").value = configuredTank.min;
    ge("labelMin").innerHTML = "Mínimo: " + configuredTank.min + "%";
}

function setTankGap() {
    value = parseInt(ge("inputGap").value);
    if (value >= 10 && value <= 300) {
        ge("inputGap").value = value + "cm";
        configuredTank.gap = value;
    }
}

function setTankHeight() {
    value = parseInt(ge("inputHeight").value);
    if (value >= 20 && value <= 300) {
        ge("inputHeight").value = value + "cm";
        configuredTank.height = value;
    }
}

function setTankCapacity() {
    value = parseInt(ge("inputCapacity").value);
    if (value >= 0 && value <= 100000) {
        ge("inputCapacity").value = value + "lts";
        configuredTank.capacity = value;
    }
}

function setTankRestart() {
    configuredTank.restart = parseInt(ge("slideRestart").value);
    ge("labelRestart").innerHTML = "Reinicio: " + configuredTank.restart + "%";
}

function setTankMin() {
    configuredTank.min = parseInt(ge("slideMin").value);
    ge("labelMin").innerHTML = "Mínimo: " + configuredTank.min + "%";
}

function configure_pump() {
    w3_close();
    ge("pump_config").style.display = "block";
    ge("config_pump_label").innerHTML = "Bomba";

    // Maximum running time
    ge("inputTmax").value = myPump.Tmax + "min";
    // Start capacitor connceted dely
    ge("slideStart").value = myPump.startDelay;
    ge("labelStart").innerHTML = "Arranque: " + myPump.startDelay + "s";
}

function setPumpTmax() {
    value = parseInt(ge("inputTmax").value);
    if (value >= 0 && value <= 120) {
        ge("inputTmax").value = value + "min";
        myPump.Tmax = value;
    }
}

function setPumpStart() {
    myPump.startDelay = parseInt(ge("slideStart").value);
    ge("labelStart").innerHTML = "Arranque: " + myPump.startDelay + "s";
}

function startPump() {

}

function stopPump() {

}

function ackPump() {

}

function savePumpConfigs() {
    w3_close();
    //TODO actually save configurations
}

function saveTankConfigs() {
    w3_close();
    //TODO actually save configurations
}

function initPage() {
    startSocket()
    startEvents()
    resetIndicators()
}

function getSetups() {
    ws.send(JSON.stringify({ cmd: 'get', slave: 1, type: 'setup' }))
    setTimeout(updateValues, 2000)
}

function updateValues() {
    ws.send(JSON.stringify({ cmd: 'get', slave: 1, type: 'variables' }))
    setTimeout(updateValues, 2000)
}


function resetIndicators() {
    updateTankValue(0, uTank)
    updateTankValue(0, lTank)
    drawLowerTankTemplate(lTank)
    drawUpperTankTemplate(uTank)
    drawPumpTemplate(myPump)
    drawMovementTemplate(mvSensor)
    drawLightTemplate(myLight)
    drawDoorTemplate(myDoor)
    animatePump()
}
// Script to open and close sidebar
function w3_open() {
    ge("mySidebar").style.display = "block";
    ge("myOverlay").style.display = "block";
}

function w3_close() {
    ge("mySidebar").style.display = "none";
    ge("myOverlay").style.display = "none";
    ge("menu_upperTank").style.display = "none";
    ge("menu_lowerTank").style.display = "none";
    ge("menu_pump").style.display = "none";
    ge("tank_config").style.display = "none";
    ge("pump_config").style.display = "none";
}

// Menu Upper Tank
function menu_upperTank() {
    ge("menu_upperTank").style.display = "block";
}
// Menu Lower Tank
function menu_lowerTank() {
    ge("menu_lowerTank").style.display = "block";
}
// Menu Pump
function menu_pump() {
    ge("menu_pump").style.display = "block";
}
window.onresize = resetIndicators;
var ws = null;

function startSocket() {
    ws = new WebSocket('ws://' + document.location.host + '/ws', ['arduino']);
    ws.binaryType = "arraybuffer";
    ws.onopen = function (e) {
        addMessage("Connected");
        // Initiate communication
        getSetups()
        updateValues()
    };
    ws.onclose = function (e) {
        addMessage("Disconnected");
    };
    ws.onerror = function (e) {
        console.log("ws error", e);
        addMessage("Error");
    };
    ws.onmessage = function (e) {
        var msg = "";
        if (e.data instanceof ArrayBuffer) {
            msg = "BIN:";
            var bytes = new Uint8Array(e.data);
            for (var i = 0; i < bytes.length; i++) {
                msg += String.fromCharCode(bytes[i]);
            }
        } else {
            msg = "TXT:" + e.data;
            processMsg(e.data)
        }
        addMessage(msg);
    };
}


function processMsg(data) {
    response = JSON.parse(data)
    if (response["type"] == "setup") {
        configTank(uTank,
            response["UT_MIN"],
            500,
            25,
            response["UT_RESTART"],
            response["UT_GAP"],
            response["UT_HEIGTH"]
        )
        configTank(lTank,
            response["LT_MIN"],
            200,
            25,
            response["LT_RESTART"],
            response["LT_GAP"],
            response["LT_HEIGTH"]
        )
        pump.Tmax = 5
        pump.startDelay = 3
    }
    if (response["type"] == "variables") {
        updateTankValue(response["UT_LEVEL"], uTank)
        updateTankValue(response["LT_LEVEL"], lTank)
        pump.state = response["PC_STATE"]
    }
}

function configTank(tank, min_level, capacity, min, restart, gap, height) {
    tank.min_level = min_level
    tank.capacity = capacity
    tank.min = min
    tank.restart = restart
    tank.height = height
    tank.gap = gap
}

function startEvents() {
    var es = new EventSource('/events');
    es.onopen = function (e) {
        addMessage("Events Opened");
    };
    es.onerror = function (e) {
        if (e.target.readyState != EventSource.OPEN) {
            addMessage("Events Closed");
        }
    };
    es.onmessage = function (e) {
        addMessage("Event: " + e.data);
    };
    es.addEventListener('ota', function (e) {
        addMessage("Event[ota]: " + e.data);
    }, false);
}

function addMessage(m) {
    ge("msgBar").innerHTML = m;
}

function sfDelete(f) {
    ws.send(JSON.stringify({ cmd: 'fs', operation: 'remove', filename: f }))
}

function sfRename(fi, fo) {
    ws.send(JSON.stringify({ cmd: 'fs', operation: 'rename', ifile: fi, ofile: fo }))
}