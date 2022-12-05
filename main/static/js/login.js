let input = document.querySelector('.input') 
let show = document.querySelector('.show') 

show.addEventListener('click', ()=>{
    show.classList.toggle('hide')
    if(input.type === 'password'){
        input.type = 'text';
    }
    else{
        input.type = 'password';
    }
})