
let scroll_btn = document.querySelector('#top-btn')
let user_image = document.querySelector('.user-image')
let pp_menu = document.querySelector('.pp-menu')
window.onscroll = () => scrollUp()

//triggers when user scrolls down
function scrollUp(){
    if (document.body.scrollTop > 0 || document.documentElement.scrollTop > 0) {
        scroll_btn.style.display = "block";
        return
    }
    scroll_btn.style.display = "none";
}
//to scroll up to the top
function scrollBtn(){
    document.body.scrollTop = 0
    document.documentElement.scrollTop = 0
}
//to trigger navigation bar
function toggleMenu(){
    let toggle = document.querySelector('.toggle');
    let navigation = document.querySelector('.navigation');
    let container = document.querySelector('.base-container');
    toggle.classList.toggle('active');
    navigation.classList.toggle('active');
    container.classList.toggle('active');
}
//to open profile menu
user_image.addEventListener('click', (e)=>{
    pp_menu.classList.toggle('open-pp-menu')
})


