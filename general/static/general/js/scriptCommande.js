//########################## AJAX FUNCTIONS ##########################
/*
This feature queries the server with Ajax to retrieve customer information and executes the associated
callback and displays an error if necessary.
 */
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
/*
This feature queries the server with Ajax to retrieve forfait information and executes the associated
callback and displays an error if necessary.
 */
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


//########################## CALLBACKS ##########################

/*
This feature is the callback associated with ajax_infos_clients. It simply displays
 customer information in the intended fields.
 */
function loadInfosClient(data) {
    $('#nom').val(data.nom);
    $('#prenom').val(data.prenom);
    $('#manege').val(data.manege);
    $('#adresse').val(data.adresse);
    $('#telephone').val(data.telephone);
    $('#email').val(data.email);

};
/*
This feature is the callback associated with ajax_forfait. It simply displays the package information in the planned
fields and calculates the TTC prices and totals with the calc_total function.
 */
function forfaitChangeData(data) {
    $('#forfaitHelp').html(data.forfait_description);
    $('#prix_ht').val(data.forfait_price_ht);
    $('#prix_ttc').val(data.forfait_price_ttc);
    $('#taxe').val(data.forfait_taxe);
    let nb_jours = $('#id_nb_jours').val();
    $('#id_total_ht').val((data.forfait_price_ht * nb_jours).toFixed(2))
    $('#id_total_ttc').val(calc_total(data.forfait_price_ht,data.forfait_taxe, nb_jours ))

};

//########################## WHEN DOM LOAD ##########################

$(document).ready(function() {
    ajax_infos_clients($('#id_client').val(),loadInfosClient); //Update clients infos when DOM is load
    /*
    Turns the tables into DataTable and allows for the integration of sorting.
     */
    $('#tableCommande').DataTable( {
        "paging":   false,
        "ordering": false,
        "info":     false
    } );
    ////Update forfait infos when DOM is load
    if(document.querySelector('#id_forfait').value){
        ajax_forfait(document.querySelector("#id_forfait").value,forfaitChangeData);
    }

});

//########################## EVENTS ##########################

//Update clients infos if client input change value
$('#id_client').change(function() {
    ajax_infos_clients($('#id_client').val(),loadInfosClient)
})

/*
Connects the plan and power that are dependent on each other.
If the power changes the appropriate package is displayed and vice versa.
 */
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
        }else if ($("#id_puissance").val() >=19 && $("#id_puissance").val()<37 ){
            $("#id_forfait").val('Forfait 2')
        }else if ($("#id_puissance").val() >= 37 && $("#id_puissance").val()<121){
            $("#id_forfait").val('Forfait 3')
        }else if ($("#id_puissance").val() >= 121){
            $("#id_forfait").val('Forfait 4')
        }else{
            $("#id_forfait").val('---------')
        }
        ajax_forfait($("#id_forfait").val(),forfaitChangeData)
    });