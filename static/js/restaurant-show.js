
/**
 * Changement de couleur des etoiles en fonction de la moyenne des notes
 */
function updateStarsWithAverage(notesAverage){
    $("#stars .star").removeClass("fas active fa-star-half-stroke").addClass("far fa-star");
    for(let i = 1;i<= 5;i++){
        if(i<=notesAverage)
            $("#stars .star").eq(i-1).removeClass("far").addClass("fas active");
        else if(i < notesAverage+1)
            $("#stars .star").eq(i-1).removeClass("far fa-star").addClass("fas fa-star-half-stroke active");     
    }
}

/**
 * Clic sur le bouton pour noter
 */
$('#user-note').delegate('.btn-noter', 'click', function(){
    if(!USER_CONNECTED){ // constante globale définie dans le fichier base.php
        showConfirmDialog("Note", "Vous devez vous connecter pour noter.<br>Etes vous d'accord pour la redirection ?", function(){
            window.location="/mon-compte/connexion";
        });
    }else{
        showRatingDialog(function(rating){
            $.post('/restaurants/'+RESTAURANT_ID+"/noter/"+rating, function(response){
                response = JSON.parse(response);
                updateStarsWithAverage(response.moyenneNotes);
                $('#notesCount').text(response.nombreNotes)
            });
            $('#user-note').html(' <span>Vous avez donné une note de <strong>'+rating+'. <a class="btn-noter text-primary">Changer</a></strong></span>');
        });
    }
});

/**
 * Au click sur le bouton de commentaire (cas où l'utilisateur n'est pas connecté)
 */
$('#btn-commenter').click(function(){
    showConfirmDialog("Note", "Vous devez vous connecter pour commenter.<br>Etes vous d'accord pour la redirection ?", function(){
        window.location="/mon-compte/connexion";
    });
});

$('#add-comment').click(function(){
    let comment = $('#comment-text').val().trim();
    if(comment != ""){
        $.post('/restaurants/'+RESTAURANT_ID+"/commenter", {comment:comment}, function(response){
            $("#commentaires").prepend(response);
        });
    }else{
        showAlertDialog("Commentaire", "Entrez du texte");
    }
});