function ajax_infos_clients(dataToSend, callback){

    $.ajax({
        url:'/ajax_infos_client',
        type: 'GET',
        data:{'id':dataToSend},
        success:(data)=>{
            callback(data);

        },
        error :() =>{
            console.log('Il y a une erreur')
    }


    });

};

function loadInfosClient(data) {
    $('#nom').val(data.nom);
    $('#prenom').val(data.prenom);
    $('#manege').val(data.manege);
    $('#adresse').val(data.adresse);
    $('#telephone').val(data.telephone);
    $('#email').val(data.email);

};

$(document).ready(function() {
    ajax_infos_clients($('#id_client').val(),loadInfosClient)
})

$('#id_client').change(function() {
    ajax_infos_clients($('#id_client').val(),loadInfosClient)
})


function forfaitChangeData(data) {
    $('#forfaitHelp').html(data.forfait_description);
    document.querySelector('#prix_ht').value = data.forfait_price_ht;
    document.querySelector('#prix_ttc').value = data.forfait_price_ttc;
    document.querySelector('#taxe').value = data.forfait_taxe;
    let nb_jours = document.querySelector('#id_nb_jours').value;
    document.querySelector('#id_total_ht').value = (data.forfait_price_ht * nb_jours).toFixed(2)
    document.querySelector('#id_total_ttc').value = calc_total(data.forfait_price_ht,data.forfait_taxe, nb_jours )

};

function ajax_forfait(dataToSend, callback){

    $.ajax({
        url:'/ajax_forfait',
        type: 'GET',
        data:{'forfait_name':dataToSend},
        success:(data)=>{
            callback(data);

        },
        error :() =>{
            console.log('Il y a une erreur')
    }


    });

};


if(document.querySelector('#id_forfait').value){
        ajax_forfait(document.querySelector("#id_forfait").value,forfaitChangeData);
    }

$('#id_forfait').change(function(){
     ajax_forfait(document.querySelector("#id_forfait").value,forfaitChangeData);
     if($("#id_forfait").val()==='Forfait 1'){
            $("#id_puissance").val(3)
        }else if ($("#id_forfait").val() === 'Forfait 2'){
            $("#id_puissance").val(21)
        }else if ($("#id_forfait").val() === 'Forfait 3'){
            $("#id_puissance").val(39)
        }else if ($("#id_forfait").val() === 'Forfait 4'){
            $("#id_puissance").val(123)
    }else {
            $("#id_puissance").val(0)
        }
});


$("#id_puissance").change(function () {
        if($("#id_puissance").val()<=18){
            $("#id_forfait").val('Forfait 1')
        }else if ($("#id_puissance").val() >=19){
            $("#id_forfait").val('Forfait 2')
        }else if ($("#id_puissance").val() >= 37){
            $("#id_forfait").val('Forfait 3')
        }else if ($("#id_puissance").val() >= 121){
            $("#id_forfait").val('Forfait 4')
        }else{
            $("#id_forfait").val('---------')
        }
        ajax_forfait($("#id_forfait").val(),forfaitChangeData)
    });