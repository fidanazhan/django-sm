function openLeftSidebar() {
    document.getElementById("nav-bar").style.left = "0";
  }
  
  function closeLeftSidebar() {
    let width = screen.width;
  
    if (width <= 1280){
      document.getElementById("nav-bar").style.left = "-35%";
    }
  
    if (width <= 768)
    {
      document.getElementById("nav-bar").style.left = "-70%";
  
    }
  
    if (width <= 385)
    {
      document.getElementById("nav-bar").style.left = "-100%";
  
    }
  }

  function openContent(event, profile_content_name){
    var i, profile_content, profile_links;
    
    profile_content = document.getElementsByClassName('profile-content');
    for ( i = 0; i < profile_content.length; i++){
      profile_content[i].style.display = 'none';
    }
  
    profile_links = document.getElementsByClassName('profile-links')
    for( i = 0; i < profile_links.length; i++){
      profile_links[i].className = profile_links[i].className.replace(" active", "")
    }
  
    document.getElementById(profile_content_name).style.display = "block";
    event.currentTarget.className += " active"
  }
  
  document.getElementById("defaultOpen").click();
  

function openEllisis(){

    const ellipsis_menu = document.getElementById('ellipsis-box')

    document.onclick = function(event){
        console.log(event.target.id)

        if(event.target.id === 'ellipsis'){
            ellipsis_menu.classList.toggle('active')
            ellipsis_menu.classList.toggle('transition')
        }

        if (event.target.id !== 'ellipsis-box' && event.target.id !== 'ellipsis'){
            ellipsis_menu.classList.remove('active')
            ellipsis_menu.classList.remove('transition')
        }        
    }   
}

