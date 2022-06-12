
var CHAT_BOX = null;
var ALIMENTATION_TRACKING_BOX = null;

function openChatBox(idConversation, idProfessionnel, nomProfessionnel){
    if(!USER_CONNECTED){ // constante globale définie dans le fichier base.php
        showConfirmDialog("", "Vous devez vous connecter pour envoyer des messages<br>D'accord pour la redirection ?", function(){
            window.location="/mon-compte/connexion";
        });
    }else{
        CHAT_BOX = window.open("/chat", "chat", "width=1000, height=600");
        if(idConversation != undefined || idProfessionnel != undefined){
            CHAT_BOX.onload = function(){
                CHAT_BOX.openChat(idConversation, idProfessionnel, nomProfessionnel)
            }
        }
        
    }
}

function openAlimentationTrackingBox(){
    if(!USER_CONNECTED){ // constante globale définie dans le fichier base.php
        showConfirmDialog("", "Vous devez vous connecter pour suivre votre alimentation<br>D'accord pour la redirection ?", function(){
            window.location="/mon-compte/connexion";
        });
    }else{
        ALIMENTATION_TRACKING_BOX = window.open("/suivre-alimentation", "alimentation-tracking", "width=1000, height=600");
        
    }
}

