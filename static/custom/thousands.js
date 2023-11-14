$(document).ready(function (){
        const pr = document.querySelectorAll('.pr')
        for (let index = 0; index < pr.length; index++) {
            
              num = pr[index].innerHTML
          var num_parts = num.toString().split(".");
          num_parts[0] = num_parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
          pr[index].innerHTML = num_parts.join(".");
        }
});

function getThousands(number){
        let resault
        var num_parts = number.toString().split(".");
        num_parts[0] = num_parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        resault = num_parts.join(".");
        return resault;
}
