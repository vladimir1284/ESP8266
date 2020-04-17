horas = 0
minutos = 0
dots=true
calentando = true
temperature  = 30

function ge(s) { return document.getElementById(s) }

function sprintf(str) {
    var args = arguments, i = 1;

    return str.replace(/%(s|d|0\d+d)/g, function (x, type) {
        var value = args[i++];
        switch (type) {
        case 's': return value;
        case 'd': return parseInt(value, 10);
        default:
            value = String(parseInt(value, 10));
            var n = Number(type.slice(1, -1));
            return '0'.repeat(n).slice(value.length) + value;
        }
    });
}

function initPage() {
  initState()
  var intervalTimer = setInterval(updateTimer, 500);
  var intervalValues = setInterval(get_values, 3000);
}

function get_values() {
    fetch("get_values").then(function (response) {
      let contentType = response.headers.get("content-type");
      if (contentType && contentType.indexOf("application/json") !== -1) {
        return response.json().then(function (json) {
          temperature  = json.temperature
          ge("thermometer").setAttribute('data-value', json.temperature)
          updatePower(json.lowerPower,json.upperPower)
          horas = Math.floor(json.timer / 3600000)
          minutos = Math.round((json.timer / 60000) % 60)
          if(json.inAuto){              
            if(json.ready){
                updateStatus("Listo")
              } else {
                updateStatus("Calentando")
              }
          }
          if (!json.on) {
            updateStatus("Apagado")
            ge("auto").checked = false
            ge("manual").checked = false
          }
          });
      } else {
        console.log("Oops, we haven't got JSON!");
      }
    })
  .catch(function(error) {
    ge("thermometer").setAttribute('data-value', 0)
    console.log('Hubo un problema con la petición Fetch:' + error.message);
  });
}
        
function set_timer(val) {
  fetch("set_timer?minutes=" + String(val))
}

function upperInputEventHandler(slider){
  ge("upperLabel").innerHTML="Superior "+slider.value+"%"
}

function upperChangeEventHandler(slider){
  if (ge("manual").checked){
    fetch("set_manual?lower="+ge("lower").value+"&upper="+ge("upper").value)
  }  
}

function lowerInputEventHandler(slider){
  ge("lowerLabel").innerHTML="Inferior "+slider.value+"%"
}

function lowerChangeEventHandler(slider){
  if (ge("manual").checked){
    fetch("set_manual?lower="+ge("lower").value+"&upper="+ge("upper").value)
  }  
}

function setpointInputEventHandler(slider){
  ge("setpointLabel").innerHTML="Temperatura "+slider.value+"°C "
}

function setpointChangeEventHandler(slider){
  if (ge("auto").checked){
    fetch("set_auto?temp="+slider.value)
  }
}

function updateTimer(){
  if (minutos+horas > 0){
    let str = ""
    if (dots){
      str = sprintf('%02d %02d', horas, minutos)
      dots = false
    } else {
      str = sprintf('%02d:%02d', horas, minutos)
      dots = true
    }
    ge("remaining").innerHTML=str
  } else {
    ge("remaining").innerHTML="00:00"
  }
}

function auto(checkBox){
  if (checkBox.checked){
    ge("manual").checked = false
    value = ge("setpoint").value
    fetch("set_auto?temp="+value)
  } else {
    updateStatus("Apagado")
    fetch("turn_off")
  }    
}

function manual(checkBox){
  if (checkBox.checked){    
    ge("auto").checked = false
    updateStatus("Apagado")
    fetch("set_manual?lower="+ge("lower").value+"&upper="+ge("upper").value)
  } else {
    fetch("turn_off")
  }    
}

function sendTimer(){
  let v = parseInt(ge("timer").value)
  horas = Math.floor(v/60)
  minutos = v%60
  set_timer(v)
}

function updatePower(lower, upper){
  let Plower = Math.round(lower*10)
  let Pupper = Math.round(upper*13)
  let Ptotal = Plower + Pupper
  ge("Pupper").innerHTML = Pupper+"W"
  ge("Plower").innerHTML = Plower+"W"
  ge("Ptotal").innerHTML = Ptotal+"W"
}

function updateStatus(status){
  if (status == "Apagado"){
    let label = ge("state")
    label.innerHTML="Apagado"
    label.classList.remove("w3-red")
    label.classList.remove("w3-teal")
    label.classList.add("w3-grey")
    calentando = false
  }
  if (status == "Calentando"){
    let label = ge("state")
    label.innerHTML="Calentando"
    label.classList.remove("w3-grey")
    label.classList.add("w3-red")
    calentando = true
  }
  if (status == "Listo"){
    let label = ge("state")
    label.innerHTML="Listo"
    label.classList.remove("w3-red")
    label.classList.remove("w3-grey")
    label.classList.add("w3-teal")
    calentando = false
  } 
}

function initState(){  
  fetch("get_values").then(function (response) {
    let contentType = response.headers.get("content-type");
    if (contentType && contentType.indexOf("application/json") !== -1) {
      return response.json().then(function (json) {
        temperature  = json.temperature
        if (json.on){
          if (json.inAuto){
            setpoint = Math.round(json.error+temperature)
            ge("auto").checked = true
            if(json.ready){
              updateStatus("Listo")
            } else {
              updateStatus("Calentando")
            }
            ge("setpoint").value = setpoint
            ge("setpointLabel").innerHTML="Temperatura "+setpoint+"°C "
          } else {
            ge("manual").checked = true
            ge("lower").value = json.lowerPower
            ge("lowerLabel").innerHTML="Inferior "+json.lowerPower+"%"
            ge("upper").value = json.upperPower
            ge("upperLabel").innerHTML="Superior "+json.upperPower+"%"
          }
        } else {
          ge("auto").checked = false
          ge("manual").checked = false
          updateStatus("Apagado")
        }
        });
    } else {
      console.log("Oops, we haven't got JSON!");
    }
  });
}

// TODO poner a 0 la temperatura cuando falle la conexión
