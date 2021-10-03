
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
     var url = window.settings_url;
     $.ajax({
          url: url,
          type: 'get',
          success: function(data){
               $("#success-message").load(url + " #success-message"); //must provide one space
               $("#red-message").load(url + " #red-message");
               $("#failure-message").load(url + " #failure-message");
          },
          complete:function(data){
               setTimeout(fetch_data, 3000);
          }
     });
}
$(document).ready(function(){
    setTimeout(fetch_data, 3000);
});