console.log('Can do following changes here in js file')

const searchfun = () =>{
     
    //fetching the text entered in search bar
    let filter = document.getElementById('myInput').value.toUpperCase();
    //console.log(filter)
    // let Table= document.getElementById('myTable');
    // let myTable= Table.getElementsByTagName('tbody');
    // let tr=myTable.getElementsByTagName('tr');

    let tr= document.querySelectorAll( '#myTable  tbody tr ');

    
    for(var i =0 ;i<tr.length;i++)
    {
        let td=tr[i].getElementsByTagName('td')[0];   //To get Title
        let td2=tr[i].getElementsByTagName('td')[1];   //To get Description
        if(td)
        {
            let textValue = td.textContent || td.innerHTML;
            let textValue2=td2.textContent || td2.innerHTML;
       
             if(textValue.toUpperCase().indexOf(filter) > -1 ||   textValue2.toUpperCase().indexOf(filter) > -1 )    // if the character matches
             {
                tr[i].style.display="";
                tr[i].style.backgroundColor="lightyellow";
             }
             else
             tr[i].style.display="none";
    
        }
    
    }
        
}



const addtodo = () =>{
   
    $('form').submit(function (e) {
        var form = this;
        e.preventDefault();
        setTimeout(function () {
            form.submit();
        }, 3000); // in milliseconds
    
        alert('Your Task added successfully');
   
        $("<p>Delay...</p>").appendTo("body");
    });

    //alert('Your Task added successfully');
   
    
// $('form').submit(  function (event) {
//     var formId = this.id,
//     form=this;
//     mySpecialFunction(formId);

//     event.preventDefault();

//     setTimeout(  function() {
//         form.submit();
//     },300)

// });

}   



  function  mySpecialFunction(){
    let box = document.querySelector( '#msg' );
    let node=document.createTextNode('Your Task added successfully');
    // box.innerHTML+='Your Task added successfully';
    box.appendChild(node);
 
    // function func() { 
    //     box.innerHTML=""; 
    //     return true;
    // }
    // setTimeout(func, 1000);
   
   
}




   


 