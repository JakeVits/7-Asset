
let interest = document.querySelectorAll('.interest')
let yes = 1;
let no = 0;

//set id for different descriptions
for(let i=0;i<interest.length;i++){
    interest[i].id = i
    interest[i].style.color = localStorage.getItem(i) || ''
}
//trigger when it's clicked and change the description to appropriate color
function getInterest(id){
    if(interest[id].style.color == 'white' || interest[id].style.color == ''){
        localStorage.setItem(id, 'yellow')
        interest[id].style.color = 'yellow'
        return
    }
    localStorage.setItem(id, 'white')
    interest[id].style.color = 'white'
}



