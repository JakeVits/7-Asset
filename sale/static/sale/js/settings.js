
let password_form = document.querySelector('.password-form')
let password_update = document.querySelectorAll('.password-update')

let email_form = document.querySelector('.email-form')
let email_update = document.querySelectorAll('.email-update')

let username_form = document.querySelector('.username-form')
let username_update = document.querySelectorAll('.username-update')


email_update.forEach(e => {
    e.addEventListener('click', () => {
        password_form.classList.add('hide')
        email_form.classList.add('show')
        username_form.classList.remove('show')
    })
})
password_update.forEach(e => {
    e.addEventListener('click', () => {
        password_form.classList.remove('hide')
        email_form.classList.remove('show')
        username_form.classList.remove('show')
    })
})
username_update.forEach(e => {
    e.addEventListener('click', () => {
        password_form.classList.add('hide')
        email_form.classList.remove('show')
        username_form.classList.add('show')
    })
})

// function to refresh particular elements in web browser
function fetch_data(){
     var url = window.USER_FOLLOW_URL;
     $.ajax({
          url: url,
          type: 'get',
          success: function(data){
               $("#success").load(url + " #success"); //must provide one space
               $("#fail").load(url + " #fail");
          },
          complete:function(data){
               setTimeout(fetch_data,3000);
          }
     });
}
$(document).ready(function(){
    setTimeout(fetch_data,4000);
});