
/*This feature allows you to hide/show order forms and change the button based on the state of the block. */
$(document).ready(function(){

  $("#buttonCollapse").click(function() {
      if ($("#CommandesCollapse").hasClass('show')){
           $("#CommandesCollapse").removeClass('show')
            $("#CommandesCollapse").addClass('hidden')
           $("#CommandesCollapse").slideToggle();
           $("#buttonCollapse").html("<i class=\"fas fa-plus\"></i>")

      }else{
          $("#CommandesCollapse").removeClass('hidden')
          $("#CommandesCollapse").addClass('show')
           $("#CommandesCollapse").slideToggle();
          $("#buttonCollapse").html("<i class=\"fas fa-minus\"></i>")
      };




  })});



document.querySelector('#buttonCreate').addEventListener('click',(e)=>{
    e.preventDefault();
    alert('TEST');
    console.log($('#form_create').serializeArray());
})
document.querySelector('#form_create').addEventListener('submit',(e)=>{
    e.preventDefault();
    alert('TEST');
    console.log($('#form_create').serializeArray());
})