
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
        this.$box.find(".user-box-btn-back").hide(-1); // On début on masque le bouton back
        this.$box.delegate(".user-box-btn-close", "click", () => this.close()); // On début on masque le bouton back
        
        this.$box.delegate(".user-box-btn-back", "click",function(){
            if(self.onBack != null)
                self.onBack()
        });
    }

    /**
     * Affichage de la boite
     */
    close(){
        if(this.opened){
            this.$box.slideUp(300);
            this.opened = false;
            UserBox.boxClosed(this);
            if(this.onClose != null)
                this.onClose()
        }
    }

    


    setOnBack(onBack){
        this.onBack = onBack;
    }
    setOnClose(onClose){
        this.onClose = onClose;
    }
    


}