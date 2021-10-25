

let selectedBtn = document.querySelector('.deleteSelectedBtn')
let deleteAllBtn = document.querySelector('.deleteAllBtn')
let deleteBtn = document.querySelector('.deleteBtn')
let cancelBtn = document.querySelector('.cancelBtn')
let modal = document.querySelector('.modal-container')
let form = document.querySelector('.container-form')
let checkbox = document.querySelectorAll('.checkbox')

//open the modal when delete text is clicked
deleteAllBtn.addEventListener('click', (e)=>{
    modal.classList.add('active')
})
//open the modal when delete text is clicked
selectedBtn.addEventListener('click', (e)=>{
    modal.classList.add('active')
})
//close the modal when outside surface of the modal is clicked
document.addEventListener('click', (e) =>{
    if(e.target.id == 'modal-container'){
        modal.classList.remove('active')
    }
})
//close the modal when cancel button is clicked
cancelBtn.addEventListener('click', (e)=>{
    modal.classList.remove('active')
})
//submit the form when delete button is clicked
deleteBtn.addEventListener('click', (e)=>{
    form.submit()
})
function checkBox(){
    let isChecked = false
    checkbox.forEach((box)=>{
        if(box.checked == true){
            selectedBtn.classList.add('displayBtn')
            isChecked = true
        }
    })
    if(!isChecked){
        selectedBtn.classList.remove('displayBtn')
    }
}



