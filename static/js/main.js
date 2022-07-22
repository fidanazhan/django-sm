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