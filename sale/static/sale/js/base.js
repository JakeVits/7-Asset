
let scroll_btn = document.querySelector('#top-btn')
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
    let main = document.querySelector('.main');
    toggle.classList.toggle('active');
    navigation.classList.toggle('active');
    main.classList.toggle('active');
}
