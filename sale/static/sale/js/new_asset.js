
let dropArea = document.querySelector('.drag-area')
let dragText = dropArea.querySelector('header')
let input = document.querySelector('#id_image')
let remove_btn = document.querySelector('#remove-btn')
let notification = document.querySelectorAll('.wrapper')
let file;

//************** if user selects file from local system *****************
//triggers when user clicks the field
dropArea.addEventListener('click', ()=>{
    input.click()
    input.addEventListener('change', function(){
        file = this.files[0] //getting only the latest file that was uploaded
        showFile()
    })
})
//triggers when user remove the image
remove_btn.addEventListener('click', ()=>{
    dropArea.innerHTML =
    `
        <div class="icon"><i class="fa fa-cloud-upload" aria-hidden="true"></i></div>
        <header>Drag & Drop</header>
        <span>OR</span>
        <header id="click-here">Click here to upload image file</header>
    `
    input.value = ''
    remove_btn.style.display = 'none'
})

//************** if user drag & drop file  *****************
//if user drag file over drop area
dropArea.addEventListener('dragover', (e)=>{
    e.preventDefault()
    dropArea.classList.add('active')
    dragText.textContent = 'Release to Upload File'
})
//if user leave dragged file from drop area
dropArea.addEventListener('dragleave', ()=>{
    dropArea.classList.remove('active')
    dragText.textContent = 'Drag & Drop to Upload File'
})
//if user drop file on drop area
dropArea.addEventListener('drop', (e)=>{
    dropArea.classList.remove('active')
    file = e.dataTransfer.files[0] //getting only the latest file that was uploaded
    dropFile()
    showFile()
})
function dropFile(){
    let dt = new DataTransfer()
    dt.items.add(new File([''], `${file.name}`))
    input.files = dt.files
    if(input.files.length === 0){
        console.log('No file selected')
    }
    else{
        console.log('File type:', file.type)
        console.log(typeof input.files)
        console.log('File is selected')
    }
}
//************** to display image *****************
function showFile(){
    let fileReader = new FileReader();
    fileReader.onload = ()=>{
        let fileURL = fileReader.result //passing user file source in fileURL var
        //adding the img tag inside the dropArea container
        dropArea.innerHTML = `<img src="${fileURL}" alt=""></img>`
    }
    fileReader.readAsDataURL(file) //read the added file
    remove_btn.style.display = 'block'
}
//************** to remove form notification when it is clicked *****************
if(notification){
    setTimeout(refreshNoty, 3000);
    notification.forEach(noty =>{
        noty.addEventListener('click', () =>{
            noty.style.display = 'none'
        })
    })
}

// function to refresh form notification every 4 sec
function refreshNoty(){
     var get_url = window.get_url; //get the get_url variable from html
     $.ajax({
          url: get_url,
          type: 'get',
          success: function(data){
               $('#success-message').load(get_url + ' #success-message')
               $('#failure-message').load(get_url + ' #failure-message')
          },
          complete:function(data){
               setTimeout(refreshNoty, 3000);
          }
     });
}
