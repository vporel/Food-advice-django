
let $MESSAGES_BOX = $("#messages-box");
let $MESSAGES_HOME_SCREEN = $("#messages-box #messages-home-screen");
let $MESSAGES_CHAT_SCREEN = $("#messages-box #messages-chat-screen");
let MESSAGES_CHAT_OPENED = false;
/**
 * Creation de l'objet UserBox qui gère la boite des messages
 */
let messagesBox = new UserBox($MESSAGES_BOX);

let loadConversationsTimer = null;
let loadMessagesTimer = null;

function loadMessages(idConversation){

    $MESSAGES_BOX.find(".conversation").removeClass("active");
    $MESSAGES_BOX.find(".conversation[data-id='"+idConversation+"']").addClass("active");

    $MESSAGES_BOX.find("#messages").load("/conversation/"+idConversation+"/messages", function(){
        $MESSAGES_BOX.find("#messages").scrollTop($MESSAGES_BOX.find("#messages").prop("scrollHeight"));
    });
    loadMessagesTimer = setInterval(function(){
        $.get("/conversation/"+idConversation+"/messages-non-lus", function(messagesCode){
            if(messagesCode != ""){
                $MESSAGES_BOX.find("#messages").append(messagesCode);
                $MESSAGES_BOX.find("#messages").scrollTop($MESSAGES_BOX.find("#messages").prop("scrollHeight"));
            }
        });
    }, 3000);
}
/**
 * Ouverture du chat après le clic sur une conversation ou le clic sur le un professionnel dans la zone de recherche
 *
 * @param int idConversation
 * @param string name Nom de l'interlocuteur
 * @param int idProfessionnel Si le chat est ouvert à partir du nom d'un professionnel (dans la zone de recherche). C-a-d que ce n'est pas directement une conversation
 * @return void
 */
function openChat(idConversation, idProfessionnel = 0,name){

    if(!messagesBox.opened){
        openMessagesBox();
    }
    if(ON_MOBILE){
        $MESSAGES_BOX.find(".user-box-title").text(name);
        $MESSAGES_CHAT_SCREEN.css({"left":"0%"}); // Affichage de la boite de chat
        $MESSAGES_BOX.find(".user-box-btn-back").show(300);
    }else{
        $MESSAGES_HOME_SCREEN.addClass("second-screen-opened");
        $MESSAGES_CHAT_SCREEN.addClass("second-screen-opened");
    }
    MESSAGES_CHAT_OPENED = true;
    //Recherche de la conversation et de ses messages
    $MESSAGES_BOX.find("#messages").html("");
    if(idConversation == 0){
        if(idProfessionnel != 0){
            $MESSAGES_CHAT_SCREEN.attr("data-idProfessionnel", idProfessionnel);
            $.post("/conversation/recherche" ,{idProfessionnel:idProfessionnel}, function(response){
                response = JSON.parse(response);
                $MESSAGES_CHAT_SCREEN.attr("data-idConversation", response.idConversation);
                
                if(response.idConversation > 0){
                    loadMessages(response.idConversation);
                }
            });
        }else{
            showAlertDialog("Ouverture conversation", "Une erreur est survenue. Réessayez plus tard");
        }
    }else{
        $MESSAGES_CHAT_SCREEN.attr("data-idConversation", idConversation);
        loadMessages(idConversation);
    }
}


 function closeChat(){
    if(ON_MOBILE){
        $MESSAGES_CHAT_SCREEN.css({"left":"100%"}); // Affichage de la boite de chat
        $MESSAGES_BOX.find(".user-box-btn-back").hide(300);
    }else{
        $MESSAGES_HOME_SCREEN.removeClass("second-screen-opened");
        $MESSAGES_CHAT_SCREEN.removeClass("second-screen-opened");
    }
    MESSAGES_CHAT_OPENED = false;
    $MESSAGES_BOX.find(".user-box-title").text("Messages");
    //Recherche de la conversation et de ses messages
    $MESSAGES_BOX.find("#messages").html("");
    $MESSAGES_BOX.find("#message-text").val("");
    clearInterval(loadMessagesTimer);
}

let lastConversationsLoad = "";
function loadConversations(){
    $.get("/conversations", function(response){
        if(response != lastConversationsLoad){
            lastConversationsLoad = response;
            $MESSAGES_BOX.find("#messages-conversations").html(response);
            //On réactive la conversation
            let activeConversationId = $MESSAGES_CHAT_SCREEN.attr("data-idConversation");
            $MESSAGES_BOX.find("#messages-conversations").find(".conversation[data-id='"+activeConversationId+"']").addClass("active");
        }
    })
}

function openMessagesBox(){
    if(!USER_CONNECTED){ // constante globale définie dans le fichier base.php
        showConfirmDialog("", "Vous devez vous connecter pour envoyer des messages<br>D'accord pour la redirection ?", function(){
            window.location="/mon-compte/connexion";
        });
    }else{
        if(!messagesBox.opened){
            messagesBox.open();
            //Premier chargement des conversations
            loadConversations();
            loadConversationsTimer = setInterval(loadConversations, 2000);
            messagesBox.setOnClose(function(){
                clearInterval(loadMessagesTimer);
                clearInterval(loadConversationsTimer);
            })
        }
    }
}
/**
 * Masque le bouton back à l'initialisation
 */
 $MESSAGES_BOX.find(".user-box-btn-back").hide(-1);
/**
 * Clic sur une conversation
 */
$MESSAGES_BOX.delegate(".conversation", "click",function(){
    openChat($(this).attr("data-id"), $(this).attr("data-nom"));
});


/**
 * Clic sur le bouton (en trois points) pour l'affichage d'options supplémentaires
 */
$MESSAGES_BOX.delegate(".conversation .show-more-options", "click",function(e){
    e.stopPropagation();
    let $conversation = $(this).parent().parent();
    $conversation.find(".more-options").slideToggle(150);
});

/**
 * Clic sur le bouton de suppression de la conversation
 */
 $MESSAGES_BOX.delegate(".conversation .delete-btn", "click",function(e){
    e.stopPropagation();
    let $conversation = $(this).parent().parent();
    let idConversation = $conversation.attr("data-id");
    $.post("/conversation/"+idConversation+"/supprimer", function(response){
        //console.log(response);
    });
    $conversation.hide(200);

    if(idConversation == $MESSAGES_CHAT_SCREEN.attr("data-idConversation")){
        closeChat();
    }
});

/**
 * Définition de l'action lorsque la boite des message est agrandie
 */
messagesBox.setOnMaximize(function(){
    if(MESSAGES_CHAT_OPENED)
        $MESSAGES_BOX.find("#messages-btn-back").show(300);
});
/**
 * Définition de l'action lorsqu'on clique sur le bouton back
 */
messagesBox.setOnBack(closeChat);

function closeMessagesProfessionalSearch(){
    $MESSAGES_BOX.find("#messages-professional-search-result .elements").html("");
    $MESSAGES_BOX.find("#messages-professional-search-result").fadeOut(200);
    $MESSAGES_BOX.find("#messages-professional-search form button").hide(-1);
    $MESSAGES_BOX.find("#messages-professional-search form input").val("");
}
/**
 * A l'envoie du formulaire pour la recherche du professionnel
 */
$MESSAGES_BOX.find("#messages-professional-search form input").keyup(function(){
    let value = $(this).val().trim();
    if(value != ""){
        $MESSAGES_BOX.find("#messages-professional-search-result .elements").load("/filtre-professionnels", {nom:value, messagesBox:true});
        $MESSAGES_BOX.find("#messages-professional-search-result").fadeIn(200);
        $MESSAGES_BOX.find("#messages-professional-search form button").show(-1);
    }else{
        closeMessagesProfessionalSearch();
    }
})

$MESSAGES_BOX.find("#messages-professional-search form button").click(closeMessagesProfessionalSearch)

/**
 * Lorsqu'on clique sur un professionnel dans les résultats d ela recherche
 */
$MESSAGES_BOX.find("#messages-professional-search-result .elements").delegate(".professional", "click", function(){
    openChat(0, $(this).attr("data-id"), $(this).attr("data-nom"));
    closeMessagesProfessionalSearch();
});

/**
 * Lorsqu'on clique sur un professionnel dans les résultats d ela recherche
 */
 $MESSAGES_BOX.find("#messages-professional-search-result .elements").delegate(".professional a", "click", function(e){
    e.stopPropagation();
});

function sendMessage(idConversation, message){
    $.post("/conversation/"+idConversation+"/envoie-message", {"message":message}, function(messageCode){
        $MESSAGES_BOX.find("#messages").append(messageCode);
        $MESSAGES_BOX.find("#messages").scrollTop($MESSAGES_BOX.find("#messages").prop("scrollHeight"));
        loadConversations();
    });
}

/**
 * Envoie du message
 */
$MESSAGES_BOX.find("#message-send-btn").click(function(){
    let message = $MESSAGES_BOX.find("#message-text").val().trim();
    let idConversation = parseInt($MESSAGES_CHAT_SCREEN.attr("data-idConversation"));
    let idProfessionnel = parseInt($MESSAGES_CHAT_SCREEN.attr("data-idProfessionnel"));
    if(message != ""){
        if(idConversation == 0 || isNaN(idConversation)){
            if(idProfessionnel == 0 || isNaN(idProfessionnel)){
                showAlertDialog("Envoie du message", "Une erreur est survenue. Réessayez plus tard");
            }else{
                $.post("/conversation/nouvelle", {"idProfessionnel":idProfessionnel}, function(response){
                    response = JSON.parse(response);
                    $MESSAGES_CHAT_SCREEN.attr("data-idConversation", response.idConversation);
                    sendMessage(response.idConversation, message);
                    loadMessages(response.idConversation);
                });
            }
        }else{
            sendMessage(idConversation, message);
        }
        //Effacement du message
        $MESSAGES_BOX.find("#message-text").val("");
    }
});

/**
 * **********************************
 *          SUIVI ALIMENTATION
 * *********************
 */
let $ALIMENTATION_TRACKING_BOX = $("#alimentation-tracking-box");

let alimentationTrackingBox = new UserBox($ALIMENTATION_TRACKING_BOX);

function openAlimentationTrackingBox(){
    if(!USER_CONNECTED){ // constante globale définie dans le fichier base.php
        showConfirmDialog("", "Vous devez vous connecter pour suivre votre alimentation<br>D'accord pour la redirection ?", function(){
            window.location="/mon-compte/connexion";
        });
    }else{
        if(!alimentationTrackingBox.opened){
            alimentationTrackingBox.open();
        }
    }
}