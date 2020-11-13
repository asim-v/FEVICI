
  /*
   Create a new chat  
  */
  function create_new_note() {
    $("#btn-create-new-chat").html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Creando ...');
    fetch("/new-chat/create")
      .then((data) => {
        console.log(data);
        $("#btn-create-new-chat").html("Listo!");
        window.location = data['url'];
      },
        (error) => {
          console.log(error);
          $("#btn-create-new-chat").html("Hubo un error.");
        });
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
  // <i class="fas fa-arrow-left" aria-hidden="True"></i>
  function collapse_sidebar(){
    var sidebar = document.getElementById('sidebar');
    var button = document.getElementById('collapse-left')
    var box = document.getElementById('showbox');

    sidebar.classList.add('hidden');
    box.setAttribute('style','padding-left:0px');
    button.setAttribute('onclick','open_sidebar()');
    button.innerHTML = '<i class="fas fa-arrow-right" aria-hidden="True"></i>';
    // button.setAttribute()
    
  }
  function open_sidebar(){
    var sidebar = document.getElementById('sidebar');
    var sidebar_lenght = document.getElementById('sidebar').offsetWidth;
    var button = document.getElementById('collapse-left')
    var box = document.getElementById('showbox');

    sidebar.classList.remove('hidden');
    box.setAttribute('style','padding-left:70px');
    button.setAttribute('onclick','collapse_sidebar()');
    button.innerHTML = '<i class="fas fa-arrow-left" aria-hidden="True"></i>';
    console.log(sidebar_lenght.toString());
  }