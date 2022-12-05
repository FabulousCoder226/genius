let body = document.querySelector('body')
let jonah = document.querySelector('.jonah')
let icon = document.querySelector('.bi-moon-fill')

jonah.addEventListener('click', ()=>{
    body.classList.toggle('dark')
    if(body.classList.contains('dark')){
        icon.classList.replace('bi-moon-fill', 'bi-brightness-high-fill')
    }
    else{
        icon.classList.replace('bi-brightness-high-fill', 'bi-moon-fill')
    }
})