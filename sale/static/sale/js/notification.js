
let selectedBtn = document.querySelector('.deleteSelectedBtn')
let deleteAllBtn = document.querySelector('.deleteAllBtn')
let deleteBtn = document.querySelector('.deleteBtn')
let cancelBtn = document.querySelector('.cancelBtn')
let modal = document.querySelector('.modal-container')
let notyForm = document.querySelector('.noty-form')
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
    notyForm.submit()
})
function checkBox(){
    let isChecked = false
    for(var i=0;i<checkbox.length;i++){
        if(checkbox[i].checked){
            selectedBtn.classList.add('displayBtn')
            isChecked = true;break;
        }
    }
    if(isChecked==false){
        selectedBtn.classList.remove('displayBtn')
    }
}
