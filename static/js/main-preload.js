
  try{
  navbar = document.getElementById("navbar").offsetHeight;
  sidebar = document.getElementById("sidebar").offsetWidth;
  
  old_main = document.getElementById('main').offsetHeight;
  old_showbox = document.getElementById('showbox').offsetWidth;
  document.getElementById("main").setAttribute('style','height:'+old_main-navbar+'px');
  document.getElementById("showbox").setAttribute('style','width:'+old_showbox-sidebar+'px');  
  // old_bg = document.getElementById("particles-background").offsetWidth;
  // old_fg = document.getElementById("particles-foreground").offsetWidth;
  
  // document.getElementById("particles-background").setAttribute('style','width:'+old_bg-sidebar+'px');
  // document.getElementById("particles-foreground").setAttribute('style','width:'+old_fg-sidebar+'px');

  document.getElementById("main").setAttribute('style','padding-top:'+navbar+'px');
  document.getElementById("showbox").setAttribute('style','padding-left:'+sidebar+'px');
  // document.getElementById("particles-background").setAttribute('style','padding-left:'+sidebar+'px');
  // document.getElementById("particles-foreground").setAttribute('style','padding-left:'+sidebar+'px');  

  document.getElementById('snav').setAttribute('style','visibility:visible');

  console.log('main generated');
  // document.getElementById("showbox").style.paddingTop += 20;
  }catch (error){
    console.log(error)
  }