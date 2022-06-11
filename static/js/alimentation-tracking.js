
let $BOX = $("#alimentation-tracking-window");
let $FIRST_SCREEN = $(".popup-window-first-screen");
let $SECOND_SCREEN = $(".popup-window-second-screen");
/**
 * Creation de l'objet PopupWindow qui gère la boite des messages
 */
let windowObject = new PopupWindow($BOX);

/**
 * Masque le bouton back à l'initialisation
 */
 $BOX.find(".popup-window-btn-back").hide(-1);

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
    $("#recommendations-box").fadeIn(500);
});

$("#recommendations-box .duree").click(function(){
    let duree = $(this).attr("data-value");
    $.get("/suivre-alimentation/recommandations", {duree:duree}, function(response){
        if(response == "age_error"){
            showConfirmDialog("", "Pour faire des recommandations, votre âge est nécessaire. Vous allez être redirigé vers une autre page pour l'ajout de votre date de naissance", function(){
                window.open("/mon-compte/modifier-informations", "_blank");
            });
        }
    })
})
