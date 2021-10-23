
let openModalBtn = document.querySelector('.camera')
let container = document.querySelector('.modal-container')
let cancelBtn = document.querySelector('.cancelBtn')
let pp = document.querySelector('.profile-image-field')

console.log(pp)

//close the modal when cancel button is clicked
cancelBtn.addEventListener('click', (e) =>{
    e.preventDefault()
    container.classList.remove('active')
})
//open the modal when camera icon is clicked
openModalBtn.addEventListener('click', (e) =>{
    console.log('It reaches')
    container.classList.add('active')
})
//close the modal when outside surface of the modal is clicked
document.addEventListener('click', (e) =>{
    if(e.target.id == 'modal-container'){
        container.classList.remove('active')
        console.log(e.target.id)
    }
})