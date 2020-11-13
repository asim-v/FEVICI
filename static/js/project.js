

function invite(){
  document.getElementById("supermodal").style.backdropFilter = "";
}
function validate(){
  $("#save_button").html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Guardando ...');
}

function cancel(){
  $("#cancel-button").html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Saliendo ...');
  fetch("/")
    .then((data) => {
      console.log(data);
      window.location = data['url'];
    },
      (error) => {
        console.log(error);
        $("#cancel").html("Error.");
      });
}


prioritatias = ["COVID-19","Medio Ambiente","Conservación Ambiental","Salud","Alimentación","Oportunidades Laborales"]
ciencias = ["Ciencia de los Materiales","Ciencias Terrestres y Ambientales","Física y Astronomía","Matemáticas","Energía Química","Energía Física"]
biologias = ["Biología Celular y Molecular","Bioquímica","Química"]
medicas = ["Ciencias Biomédicas y de la Salud","Ciencia Medica Traslacional","Neurociencias"]
humanidades = ["Historia"]
csociales = ["Comportamiento y Ciencia Sociales","Psicología Social","Psicología Clínica"]
biotech = ["Biología Computacional y Bioinformatica","Ciencias Animales","Ciencias de las Plantas"]
ingenierias = ["Ingeniería Ambiental","Ingeniería Biomédica","Robótica y Máquinas Inteligentes","Sistemas de Software","Sistemas Embedidos"]

function createCats(array){
  var id = "subcat";
  var sel = document.getElementById(id);
  while(sel.hasChildNodes()){
    sel.removeChild(sel.firstChild);   
  }
  
  for (index = 0; index < array.length; index++) { 
    var opt = document.createElement('option');
    opt.appendChild( document.createTextNode(array[index]) );
    opt.value = array[index]; 
    sel.appendChild(opt);   
  } 
}

function getIndex(){
  var e = document.getElementById("cat").selectedIndex;
  if (e===1){
    createCats(prioritatias);
  }if (e===2){
    createCats(ciencias);
  }if (e===3){
    createCats(biologias);
  }if (e===4){
    createCats(medicas);
  }if (e===5){
    createCats(humanidades);
  }if (e===6){
    createCats(csociales);
  }if (e===7){
    createCats(biotech);
  }if (e===8){
    createCats(ingenierias);
  }

  console.log(e);
}

function checkMaterials(){
  if (document.getElementById('Materials').checked){
    document.getElementById('invisible').style.display = 'inline';
  }else{
    document.getElementById('invisible').style.display = 'none';
  }
}

function copy() {
  /* Get the text field */
  var copyText = document.getElementById("code");

  /* Select the text field */
  copyText.select();
  copyText.setSelectionRange(0, 99999); /*For mobile devices*/

  /* Copy the text inside the text field */
  document.execCommand("copy");

  /* Alert the copied text */
  element = document.getElementById('copied').classList;
  element.remove('fa-copy');
  element.add('fa-check');

  
}
function validateEmail(email) {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function sendMail(){
  mailto = document.getElementById("invitation").value;
  $("#sendmail").html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Enviando ...');
  if (validateEmail(mailto)){
    fetch("/send_invite/"+mailto)
      .then((data) => {
        console.log(data);
        $("#sendmail").html('Enviado!🔥');
        document.getElementById("sendmail").style.backgroundColor = "#67FBD1 "
        document.getElementById("sendmail").style.color = "#2B2B2B "        
        // window.location = data['url'];
      },
        (error) => {
          console.log(error);
          $("#sendmail").html("Error.");
        }
      );  
  }
  else{
    $("#sendmail").html("Correo no válido");
    document.getElementById("sendmail").style.backgroundColor = "#DF4550 "
    document.getElementById("sendmail").style.color = "#fff "
  }
}













