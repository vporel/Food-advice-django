let $ALERT_CONFIRM_DIALOG_BOX = $("#alert-confirm-dialog-box");
let $RATING_DIALOG_BOX = $("#rating-dialog-box");
let ALERT_CONFIRM_DIALOG_BOX_CALLBACK_IF_YES;// Fonction appelée lorsqu'on clique sur le bouton YES
let ALERT_CONFIRM_DIALOG_BOX_CALLBACK_IF_NO;// Fonction appelée lorsqu'on clique sur le bouton NO
let ALERT_CONFIRM_DIALOG_BOX_CALLBACK_WHEN_OK; // Fonction appelée lorsqu'on clique sur le bouton OK
let RATING_DIALOG_BOX_CALLBACK_ON_CLICK; // Fonction appelée lorsqu'on clique sur le bouton OK

$ALERT_CONFIRM_DIALOG_BOX.find("#alert-confirm-dialog-btn-yes").click(function(){
    $ALERT_CONFIRM_DIALOG_BOX.fadeOut(300);
    if(ALERT_CONFIRM_DIALOG_BOX_CALLBACK_IF_YES != null)
        ALERT_CONFIRM_DIALOG_BOX_CALLBACK_IF_YES();
});
$ALERT_CONFIRM_DIALOG_BOX.find("#alert-confirm-dialog-btn-no").click(function(){
    $ALERT_CONFIRM_DIALOG_BOX.fadeOut(300);
    if(ALERT_CONFIRM_DIALOG_BOX_CALLBACK_IF_NO != null)
        ALERT_CONFIRM_DIALOG_BOX_CALLBACK_IF_NO();
});
$ALERT_CONFIRM_DIALOG_BOX.find("#alert-confirm-dialog-btn-ok").click(function(){
    $ALERT_CONFIRM_DIALOG_BOX.fadeOut(300);
    if(ALERT_CONFIRM_DIALOG_BOX_CALLBACK_WHEN_OK != null)
        ALERT_CONFIRM_DIALOG_BOX_CALLBACK_WHEN_OK();
});

$RATING_DIALOG_BOX.find(".rating-dialog-box-btn-rate").click(function(){
    $RATING_DIALOG_BOX.fadeOut(300);
    if(RATING_DIALOG_BOX_CALLBACK_ON_CLICK != null)
        RATING_DIALOG_BOX_CALLBACK_ON_CLICK(parseInt($(this).text()));
});

$RATING_DIALOG_BOX.find("#rating-dialog-box-btn-cancel").click(function(){
    $RATING_DIALOG_BOX.fadeOut(300);
    if(RATING_DIALOG_BOX_CALLBACK_ON_CLICK != null)
        RATING_DIALOG_BOX_CALLBACK_ON_CLICK(parseInt($(this).text()));
});


/**
 * @param string title
 * @param string msg
 * 
 * @return void
 */
function fillAlertConfirmDialogBox(title, msg){
    if(title == ""){
        $ALERT_CONFIRM_DIALOG_BOX.find(".dialog-box-title").hide();
    }else{
        $ALERT_CONFIRM_DIALOG_BOX.find(".dialog-box-title").text(title).show();
    }
    $ALERT_CONFIRM_DIALOG_BOX.find(".dialog-box-content").html(msg);
}

/**
 * Affiche la boite d'alerte
 * @param string title
 * @param string msg
 * @param callable callbackWhenOk Fonction appelée Lorsqu'on clique sur le bouton OK
 * 
 * @return void
 */
function showAlertDialog(title, msg, callbackWhenOk = null){
    fillAlertConfirmDialogBox(title, msg);
    $ALERT_CONFIRM_DIALOG_BOX.find(".alert-confirm-dialog-btn-confirm").hide();
    $ALERT_CONFIRM_DIALOG_BOX.find("#alert-confirm-dialog-btn-ok").show();
    ALERT_CONFIRM_DIALOG_BOX_CALLBACK_WHEN_OK = callbackWhenOk;
    $ALERT_CONFIRM_DIALOG_BOX.fadeIn(300);
}

/**
 * Affiche la boite d'alerte avec les boutons pour une confirmation
 * @param string title
 * @param string msg
 * @param callable callbackIfYes Fonction appelée si on clique sur le bouton Yes (Oui)
 * @param callable callbackIfNo Fonction appelée si on clique sur le bouton No (Non)
 * 
 * @return void
 */
function showConfirmDialog(title, msg, callbackIfYes = null, callbackIfNo = null){
    fillAlertConfirmDialogBox(title, msg);
    $ALERT_CONFIRM_DIALOG_BOX.find(".alert-confirm-dialog-btn-confirm").show();
    $ALERT_CONFIRM_DIALOG_BOX.find("#alert-confirm-dialog-btn-ok").hide();
    ALERT_CONFIRM_DIALOG_BOX_CALLBACK_IF_YES = callbackIfYes;
    ALERT_CONFIRM_DIALOG_BOX_CALLBACK_IF_NO = callbackIfNo;
    $ALERT_CONFIRM_DIALOG_BOX.fadeIn(300);
}

/**
 * Affiche la boite d'alerte pour le choix d'une note
 * @param callable callbackOnClick Fonction appelée si on clique sur une note
 * 
 * @return void
 */
function showRatingDialog(callbackOnClick = null){
    RATING_DIALOG_BOX_CALLBACK_ON_CLICK = callbackOnClick;
    $RATING_DIALOG_BOX.fadeIn(300);
}