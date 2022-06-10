
let $BOX = $("#messages-window");
let $MESSAGES_HOME_SCREEN = $("#messages-window #messages-home-screen");
let $MESSAGES_CHAT_SCREEN = $("#messages-window #messages-chat-screen");
/**
 * Creation de l'objet PopupWindow qui gère la boite des messages
 */
let messagesWindow = new PopupWindow($BOX);

let loadMessagesTimer = null;

function loadMessages(idConversation){

    $BOX.find(".conversation").removeClass("active");
    $BOX.find(".conversation[data-id='"+idConversation+"']").addClass("active");

    $BOX.find("#messages").load("/conversation/"+idConversation+"/messages", function(){
        $BOX.find("#messages").scrollTop($BOX.find("#messages").prop("scrollHeight"));
    });
    loadMessagesTimer = setInterval(function(){
        $.get("/conversation/"+idConversation+"/messages-non-lus", function(messagesCode){
            if(messagesCode != ""){
                $BOX.find("#messages").append(messagesCode);
                $BOX.find("#messages").scrollTop($BOX.find("#messages").prop("scrollHeight"));
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
    if(ON_MOBILE()){
        $BOX.find(".popup-window-title").text(name);
        $MESSAGES_CHAT_SCREEN.css({"left":"0%"}); // Affichage de la boite de chat
        $BOX.find(".popup-window-btn-back").show(300);
    }
    $MESSAGES_CHAT_SCREEN.addClass("opened");
    //Recherche de la conversation et de ses messages
    $BOX.find("#messages").html("");
    if(idConversation == 0){
        if(idProfessionnel != 0){
            $MESSAGES_CHAT_SCREEN.attr("data-idProfessionnel", idProfessionnel);
            $.post("/conversation/recherche/"+idProfessionnel, function(response){
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
    if(ON_MOBILE()){
        $MESSAGES_CHAT_SCREEN.css({"left":"100%"}); // Affichage de la boite de chat
        $BOX.find(".popup-window-btn-back").hide(300);
    }
    $MESSAGES_CHAT_SCREEN.removeClass("opened");
    $BOX.find(".popup-window-title").text("Messages");
    //Recherche de la conversation et de ses messages
    $BOX.find("#messages").html("");
    $BOX.find("#message-text").val("");
    clearInterval(loadMessagesTimer);
}

let lastConversationsLoad = "";
function loadConversations(){
    $.get("/conversations", function(response){
        if(response != lastConversationsLoad){
            lastConversationsLoad = response;
            $BOX.find("#messages-conversations").html(response);
            //On réactive la conversation
            let activeConversationId = $MESSAGES_CHAT_SCREEN.attr("data-idConversation");
            $BOX.find("#messages-conversations").find(".conversation[data-id='"+activeConversationId+"']").addClass("active");
        }
    })
}
/**
 * Masque le bouton back à l'initialisation
 */
 $BOX.find(".popup-window-btn-back").hide(-1);
/**
 * Clic sur une conversation
 */
$BOX.delegate(".conversation", "click",function(){
    openChat($(this).attr("data-id"), 0, $(this).attr("data-nom"));
});


/**
 * Clic sur le bouton (en trois points) pour l'affichage d'options supplémentaires
 */
$BOX.delegate(".conversation .show-more-options", "click",function(e){
    e.stopPropagation();
    let $conversation = $(this).parent().parent();
    $conversation.find(".more-options").slideToggle(150);
});

/**
 * Clic sur le bouton de suppression de la conversation
 */
 $BOX.delegate(".conversation .delete-btn", "click",function(e){
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
 * Définition de l'action lorsqu'on clique sur le bouton back
 */
messagesWindow.setOnBack(closeChat);

function closeMessagesProfessionalSearch(){
    $BOX.find("#messages-professional-search-result .elements").html("");
    $BOX.find("#messages-professional-search-result").fadeOut(200);
    $BOX.find("#messages-professional-search form button").hide(-1);
    $BOX.find("#messages-professional-search form input").val("");
}
/**
 * A l'envoie du formulaire pour la recherche du professionnel
 */
$BOX.find("#messages-professional-search form input").keyup(function(){
    let value = $(this).val().trim();
    if(value != ""){
        $BOX.find("#messages-professional-search-result .elements").load("/filtre-professionnels", {nom:value, messagesWindow:true});
        $BOX.find("#messages-professional-search-result").fadeIn(200);
        $BOX.find("#messages-professional-search form button").show(-1);
    }else{
        closeMessagesProfessionalSearch();
    }
})

$BOX.find("#messages-professional-search form button").click(closeMessagesProfessionalSearch)

/**
 * Lorsqu'on clique sur un professionnel dans les résultats d ela recherche
 */
$BOX.find("#messages-professional-search-result .elements").delegate(".professional", "click", function(){
    openChat(0, $(this).attr("data-id"), $(this).attr("data-nom"));
    closeMessagesProfessionalSearch();
});

/**
 * Lorsqu'on clique sur un professionnel dans les résultats d ela recherche
 */
 $BOX.find("#messages-professional-search-result .elements").delegate(".professional a", "click", function(e){
    e.stopPropagation();
});

function sendMessage(idConversation, message){
    $.post("/conversation/"+idConversation+"/envoie-message/", {"message":message}, function(messageCode){
        $BOX.find("#messages").append(messageCode);
        $BOX.find("#messages").scrollTop($BOX.find("#messages").prop("scrollHeight"));
        loadConversations();
    });
}

/**
 * Envoie du message
 */
$BOX.find("#message-send-btn").click(function(){
    let message = $BOX.find("#message-text").val().trim();
    let idConversation = parseInt($MESSAGES_CHAT_SCREEN.attr("data-idConversation"));
    let idProfessionnel = parseInt($MESSAGES_CHAT_SCREEN.attr("data-idProfessionnel"));
    if(message != ""){
        if(idConversation == 0 || isNaN(idConversation)){
            if(idProfessionnel == 0 || isNaN(idProfessionnel)){
                showAlertDialog("Envoie du message", "Une erreur est survenue. Réessayez plus tard");
            }else{
                $.post("/conversation/nouvelle/"+idProfessionnel, function(response){
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
        $BOX.find("#message-text").val("");
    }
});
loadConversations();
let loadConversationsTimer = setInterval(loadConversations, 2000);