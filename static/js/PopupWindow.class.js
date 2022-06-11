
class PopupWindow{
    onBack = null;
    onClose = null;
    $box = null;
    /**
     * 
     * @param {*} $element L'élément html géré par la classe
     */
    constructor($element){
        this.$box = $element;
        this.init();
    }

    /**
     * Méthode appelé dans le constructeur
     * Elle crée les différents écouteurs d'évènements pour les éléments de la boite
     */
    init(){
        let self = this;
        this.$box.find(".popup-window-btn-back").hide(-1); // On début on masque le bouton back
        this.$box.delegate(".popup-window-btn-close", "click", () => this.close()); // On début on masque le bouton back
        
        this.$box.delegate(".popup-window-btn-back", "click",function(){
            if(self.onBack != null)
                self.onBack()
        });
    }

    /**
     * Affichage de la boite
     */
    close(){
        if(this.opened){
            if(this.onBeforeClose != null)
                this.onBeforeClose()
            window.close()
        }
    }

    


    setOnBack(onBack){
        this.onBack = onBack;
    }
    setOnBeforeClose(onBeforeClose){
        this.onBeforeClose = onBeforeClose;
    }
    


}