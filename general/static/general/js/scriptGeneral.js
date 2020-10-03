
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



function calc_total(price, taxe, nb_jours){
    let total = Math.round((price *(1+taxe/100) )* nb_jours);
    total = total.toFixed(2)
    return total

}

function forfaitChangeData(data, index) {
    document.querySelector('#prix_HT'+index).value = data.forfait_price_ht;
    document.querySelector('#prix_TTC'+index).value = data.forfait_price_ttc;
    document.querySelector('#taxe'+index).value = data.forfait_taxe;
    let nb_jours = document.querySelector('#id_client-'+index+'-nb_jours').value;
    document.querySelector('#id_client-'+index+'-total_ttc').value = calc_total(data.forfait_price_ht,data.forfait_taxe, nb_jours )
};

function ajax_forfait(dataToSend, callback, index){

    $.ajax({
        url:'/ajax_forfait',
        type: 'GET',
        data:{'forfait_name':dataToSend},
        success:(data)=>{
            callback(data, index);

        },
        error :() =>{
            console.log('Il y a une erreur')
    }


    });

};


$( "div[id^='commande_client']" ).each(function( index ) {
    if(document.querySelector('#id_client-'+index+'-forfait').value){
        ajax_forfait(document.querySelector("#id_client-"+index+"-forfait").value,forfaitChangeData, index);
    }
  $("#id_client-"+index+"-forfait").change(function (){
        ajax_forfait(document.querySelector("#id_client-"+index+"-forfait").value,forfaitChangeData, index)
        }
    );

    $("#id_client-"+index+"-nb_jours").change(function (){
    let prix_ht = document.querySelector('#prix_HT'+index).value;
    let prix_ttc = document.querySelector('#prix_TTC'+index).value;
    let taxe = document.querySelector('#taxe'+index).value
    let nb_jours = document.querySelector('#id_client-'+index+'-nb_jours').value;
    document.querySelector('#id_client-'+index+'-total_ttc').value = calc_total(prix_ht,taxe, nb_jours )
        }
    );

});