
let closeBtn = document.querySelector('.closeBtn')
let container = document.querySelector('.modal-container')
let deleteBtn = document.querySelectorAll('.delete')

//open the modal when the button is in the modal is clicked
for(var i=0;i<deleteBtn.length;i++){
    deleteBtn[i].addEventListener('click', (e)=>{
        container.classList.add('active')
        console.log('DeleteBtn')
    })
}
//close the modal when the button is in the modal is clicked
closeBtn.addEventListener('click', (e) =>{
    container.classList.remove('active')
})
//close the modal when outside surface of the modal is clicked
window.addEventListener('click', (e) =>{
    if(e.target.id == 'modal_container'){
        container.classList.remove('active')
    }
})



