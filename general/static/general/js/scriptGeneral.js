
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
    document.querySelector('#id_client-'+index+'-total_ht').value = (data.forfait_price_ht * nb_jours).toFixed(2)
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

        if($("#id_client-"+index+"-forfait").val()==='Forfait 1'){
            $("#id_client-"+index+"-puissance").val(1)
        }else if ($("#id_client-"+index+"-forfait").val() === 'Forfait 2'){
            $("#id_client-"+index+"-puissance").val(19)
        }else if ($("#id_client-"+index+"-forfait").val() === 'Forfait 3'){
            $("#id_client-"+index+"-puissance").val(37)
        }else if ($("#id_client-"+index+"-forfait").val() === 'Forfait 4'){
            $("#id_client-"+index+"-puissance").val(121)
    }else {
            $("#id_client-"+index+"-puissance").val(0)
        }}
    );

    $("#id_client-"+index+"-nb_jours").change(function (){
    let prix_ht = document.querySelector('#prix_HT'+index).value;
    let prix_ttc = document.querySelector('#prix_TTC'+index).value;
    let taxe = document.querySelector('#taxe'+index).value
    let nb_jours = document.querySelector('#id_client-'+index+'-nb_jours').value;
    document.querySelector('#id_client-'+index+'-total_ttc').value = calc_total(prix_ht,taxe, nb_jours );
    document.querySelector('#id_client-'+index+'-total_ht').value = (prix_ht * nb_jours).toFixed(2)
        }
    );
    $("#id_client-"+index+"-puissance").change(function () {
        if($("#id_client-"+index+"-puissance").val()<=18){
            $("#id_client-"+index+"-forfait").val('Forfait 1')
        }else if ($("#id_client-"+index+"-puissance").val() >18 && $("#id_client-"+index+"-puissance").val()<37 ){
            $("#id_client-"+index+"-forfait").val('Forfait 2')
        }else if ($("#id_client-"+index+"-puissance").val() > 36 && $("#id_client-"+index+"-puissance").val()<121 ){
            $("#id_client-"+index+"-forfait").val('Forfait 3')
        }else if ($("#id_client-"+index+"-puissance").val() > 120){
            $("#id_client-"+index+"-forfait").val('Forfait 4')
        }else{
            $("#id_client-"+index+"-forfait").val('---------')
        }
        ajax_forfait(document.querySelector("#id_client-"+index+"-forfait").value,forfaitChangeData, index)
    });

});


function ajax_search(dataToSend, callback){

    $.ajax({
        url:'/ajax_search/client',
        type: 'GET',
        data:{'q':dataToSend},
        success:(data)=>{
            callback(data.html_from_view);

        },
        error :() =>{
            console.log('Il y a une erreur')
    }


    });

};

function resultSearchClients(data) {
    $('.table-responsive').html(data);

}


$('#search_client').keyup(()=>{
    ajax_search(document.querySelector('#search_client').value,resultSearchClients);
})

function ajax_search_commande(dataToSend, callback){

    $.ajax({
        url:'/ajax_search/commande',
        type: 'GET',
        data:{'q':dataToSend},
        success:(data)=>{
            callback(data.html_from_view);

        },
        error :() =>{
            console.log('Il y a une erreur')
    }


    });

};


$('#searchCommande').keyup(()=>{
    ajax_search_commande($('#searchCommande').val(),resultSearchClients);
})

function ajax_payee(dataToSend1, dataToSend2){

    $.ajax({
        url:'/ajax_payee',
        type: 'GET',
        data:{'payee':dataToSend1, 'id_commande':dataToSend2},
        success:(data)=>{
            console.log("Order updated");

        },
        error :() =>{
            console.log('Il y a une erreur')
    }


    });

};
function ajax_payee(dataToSend1, dataToSend2){

    $.ajax({
        url:'/ajax_payee',
        type: 'GET',
        data:{'payee':dataToSend1, 'id_commande':dataToSend2},
        success:(data)=>{
            console.log("Order updated");

        },
        error :(data) =>{
            if (data.payee) {
                $('#checkPayee').attr('checked', 'checked')
            }else{
                $('#checkPayee').removeAttr('checked')
            }
    }


    });

};
function ajax_traitee(dataToSend1, dataToSend2){

    $.ajax({
        url:'/ajax_ach',
        type: 'GET',
        data:{'traitee':dataToSend1, 'id_commande':dataToSend2},
        success:(data)=>{
            console.log("Order updated");

        },
        error :(data) =>{
            if (data.payee) {
                $('#checkAch').attr('checked', 'checked')
            }else{
                $('#checkAch').removeAttr('checked')
            }
    }


    });

};

$('#checkPayee').change(function() {
    let payee;
    let id_commande = $('#commandeID').val()
    if (this.checked) {
        payee = true;
        ajax_payee(payee, id_commande)
    } else {
        let payee = false;
        ajax_payee(payee, id_commande)
    }
});

$('#checkAch').change(function() {
    let traitee;
    let id_commande = $('#commandeID').val()
    if (this.checked) {
        traitee = true;
        ajax_traitee(traitee, id_commande)
    } else {
        let traitee = false;
        ajax_traitee(traitee, id_commande)
    }
});

