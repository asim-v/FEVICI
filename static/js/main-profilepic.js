
  function dropdownClick(target, other) {
    if(document.querySelectorAll(other)[0].classList.contains('active')){
      document.querySelectorAll(other)[0].classList.remove('active');
    }
    document.querySelectorAll(target)[0].classList.toggle('active');
  }
  try{
    document.querySelector(".profileddtrigger").addEventListener("click", function() {
      dropdownClick('.profiledd', '.mobilemenudd');
    });
    document.querySelector(".ddtriggermobile").addEventListener("click", function() {
      dropdownClick('.mobilemenudd', '.profiledd');
    });
  }catch(error){
    console.log(error)
  }