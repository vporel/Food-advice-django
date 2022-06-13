

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
        $.post('/aliments/'+ALIMENT_ID+"/commenter", {comment:comment}, function(response){
            $("#commentaires").prepend(response);
        });
    }else{
        showAlertDialog("Commentaire", "Entrez du texte");
    }
});