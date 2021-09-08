
let notification = document.querySelectorAll('.wrapper')

if(notification){
    notification.forEach(noty =>{
        console.log(noty)
        noty.addEventListener('click', () =>{
            noty.style.display = 'none'
        })
    })
}