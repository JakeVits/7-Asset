function getInterest(id){
    let form = document.getElementById(`form${id}`)
    let token = form.getElementsByTagName('input')[0].value
    let interest = form.getElementsByTagName('input')[1].value
    $(form).on('submit', (e)=>{
        e.preventDefault()
        e.stopImmediatePropagation();
        var post_url = window.post_url; //get the post url of django from html
        $.ajax({
            type: 'POST',
            url: post_url,
            headers:{
                'Content-Type': 'application/json',
                "X-CSRFToken": token,
            },
            data: interest,
            dataType: 'json',
            success: function(status){
                if(status.interest === 'interest'){
                    console.log(status.asset + ' asset is interested')
                }
                else{
                    console.log(status.asset + ' asset is not interested')
                }
            },
            error: function(error){
                console.log('Failed to interest this asset!')
            }
        })
    })
}
function refreshData(){
     var total_interest = document.querySelectorAll('.total-interest')
     var interest_status = document.querySelectorAll('.interest-info')
     var get_url = window.get_url; //get the get url of django from html
     $.ajax({
          url: get_url,
          type: 'get',
          success: function(data){
               total_interest.forEach(i =>{
                    $(`#${i.id}`).load(get_url + ` #${i.id}`)
               })
               interest_status.forEach(status =>{
                    $(`#${status.id}`).load(get_url + ` #${status.id}`)
               })
          },
          complete:function(data){
               setTimeout(refreshData, 1000);
          }
     });
}
$(document).ready(function(){
    setTimeout(refreshData,1000);
});
// var myVar;
// function myFunction() {
//   myVar = setTimeout(function(){ alert("Hello"); }, 3000);
// }
// function myStopFunction() {
//   clearTimeout(myVar);
// }
