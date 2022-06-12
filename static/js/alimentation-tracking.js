
let $BOX = $("#alimentation-tracking-window");
let $FIRST_SCREEN = $(".popup-window-first-screen");
let $SECOND_SCREEN = $(".popup-window-second-screen");

/**
 * Masque le bouton back à l'initialisation
 */
$BOX.find(".popup-window-btn-back").hide(-1);
$BOX.delegate(".popup-window-btn-close", "click", function(){
    showConfirmDialog("", "Voulez-vous vraiment quitter cette fenêtre ? ", function(){
        window.close();
    });
});

$.get("/suivre-alimentation/repas-consommes", function(response){
$("#consumed-foods").html(response);
})

$("#add-consumed-food-form #submit-btn").click(function(){
    let formData = new FormData($("#add-consumed-food-form form")[0]);
    let repas = formData.get("repas");
    if(repas != "" && formData.get("date") != "" && formData.get("momentJournee") != ""){
        $.post("/suivre-alimentation/ajouter-repas-consomme/"+repas, {
                repas:repas,
                date:formData.get("date"),
                momentJournee:formData.get("momentJournee"),
                contributeur:formData.get("contributeur")
            },function(response){
                if(response == "integrity_error"){
                    showAlertDialog("Erreur", "Vous avez déjà enregistré un repas pour cette date et ce moment de journée")
                }else{
                    $("#consumed-foods").html(response);
                }
            }
        );
    }else{
        showAlertDialog("Ajout repas consommé", "Remplissez tous les champs");
    }
})

$("#show-recommendations-btn").click(function(){

    $("#recommendations-box #step1").slideDown(-1);
    $("#recommendations-box #step2").slideUp(-1);
    $("#recommendations-box").fadeIn(500);
});

$("#recommendations-box .duree").click(function(){
    let duree = $(this).attr("data-value");
    $.get("/suivre-alimentation/verifier-remplissage", {duree:duree}, function(response){
        if(response == "age_error"){
            showConfirmDialog("", "Pour faire des recommandations, votre âge est nécessaire. Vous allez être redirigé vers une autre page pour l'ajout de votre date de naissance", function(){
                window.open("/mon-compte/modifier-informations", "_blank");
            });
        }else if(response == "sexe_error"){
            showConfirmDialog("", "Pour faire des recommandations, votre sexe est nécessaire. Vous allez être redirigé vers une autre page pour l'ajout de votre date de naissance", function(){
                window.open("/mon-compte/modifier-informations", "_blank");
            });
        }else if(response.indexOf("fill_error") == 0){
            let splitResponse = response.split(":");
            if(splitResponse.length == 2)
                msg ="Vous n'avez pas entré de repas pour la date <strong>"+splitResponse[1]+"</strong>. <br><i>Les estimations seront moins correctes.</i> <br>Voulez-vous quand même continuer ?";
            else if(splitResponse.length == 3)
                msg = "Vous n'avez pas entré de repas pour <strong>"+splitResponse[2]+"</strong> à la date <strong>"+splitResponse[1]+"</strong>. <br><i>Les estimations seront moins correctes.</i> <br>Voulez-vous quand même continuer ?";
            
            showConfirmDialog("", msg, function(){
                showRecommendations(duree)
            });
        }else{
            showRecommendations(duree)
        }
    })
})

function showRecommendations(duree){
    
    $.get("/suivre-alimentation/recommandations", {duree:duree}, function(response){
        $("#recommendations").html(response);
        $("#recommendations-box #step1").slideUp(500);
        $("#recommendations-box #step2").slideDown(500);
    })
}