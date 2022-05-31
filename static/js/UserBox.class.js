
class UserBox{

    static boxes = [];
    static minimizedHeight = 35;
    static boxOnTop = null;

    onMinimize = null;
    onMaximize = null;
    onBack = null;
    onClose = null;
    $box = null;
    minimized = false;
    opened = false;
    /**
     * 
     * @param {*} $element L'élément html géré par la classe
     */
    constructor($element){
        this.$box = $element;
        this.init();
        UserBox.boxes.push(this);
    }

    /**
     * Méthode appelé dans le constructeur
     * Elle crée les différents écouteurs d'évènements pour les éléments de la boite
     */
    init(){
        let self = this;
        this.$box.find(".user-box-btn-back").hide(-1); // On début on masque le bouton back
        this.$box.delegate(".user-box-btn-close", "click", () => this.close()); // On début on masque le bouton back
        this.$box.delegate(".user-box-btn-min-max", "click",function(){
            if(!self.minimized){
                self.minimize();
            }else{
                self.maximize();
            }
        });
        this.$box.delegate(".user-box-btn-back", "click",function(){
            if(self.onBack != null)
                self.onBack()
        });
    }
    
    static getMaximizedHeightPercent(){
        if(ON_MOBILE){
            return 100;
        }else{
            return 95 - ((UserBox.getOpenedBoxes().length-1) * 5);
        }
                
    }

    /**
     * Affichage de la boite
     */
    open(){
        if(!this.opened){
            //Réduction des autres boites ouvertesthis.
            this.opened = true;
            this.$box.css({"height": UserBox.getMaximizedHeightPercent()+"%"});
            this.$box.slideDown(500);
        }
        this.maximize();
    }
    close(){
        if(this.opened){
            this.$box.slideUp(300);
            this.opened = false;
            UserBox.boxClosed(this);
            if(this.onClose != null)
                this.onClose()
        }
    }

    minimize(){
        if(this.opened && !this.minimized){
            this.$box.animate({"height": UserBox.minimizedHeight+"px"}, 500); //Reduire la boite
            this.$box.find(".user-box-btn-min-max").removeClass("fa-arrow-down").addClass("fa-arrow-up");
            this.$box.find(".user-box-btn-back").hide(300);
            
            this.minimized = true;
            if(this.onMinimize != null)
                this.onMinimize()
        }
    }

    maximize(){
        if(this.opened){
            UserBox.boxMaximized(this);
            if(this.minimized){
                this.$box.find(".user-box-btn-min-max").removeClass("fa-arrow-up").addClass("fa-arrow-down");
                this.$box.animate({"height": UserBox.getMaximizedHeightPercent()+"%"}, 500);
                
                this.minimized = false;
                
                if(this.onMaximize != null)
                    this.onMaximize()
            }
        }
    }

    setOnMinimize(onMinimize){
        this.onMinimize = onMinimize;
    }
    setOnMaximize(onMaximize){
        this.onMaximize = onMaximize;
    }
    setOnBack(onBack){
        this.onBack = onBack;
    }
    setOnClose(onClose){
        this.onClose = onClose;
    }

    static getOpenedBoxes(){
        return UserBox.boxes.filter(box => box.opened);
    }

    static boxMaximized(userBox){
        let i = 0;
        let openedBoxes = [];
        UserBox.boxes.forEach(box => {
            if(box != userBox && box.opened){
                box.minimize();
                let bottom = 10+(i * (box.$box.height()+5));
                box.$box.css({"bottom":bottom+"px"});
                openedBoxes.push(box);
                i++;
            }
        });

        if(ON_MOBILE){

        }else{
            let bottom = 10;
            if(openedBoxes.length > 0){
                bottom  += parseInt(openedBoxes[openedBoxes.length-1].$box.css("bottom")) - bottom + UserBox.minimizedHeight+5; // La boite au dessus des autres parmi celles qui ont été réduites
                
                console.log(openedBoxes[openedBoxes.length-1].$box);
                console.log(parseInt(openedBoxes[openedBoxes.length-1].$box.css("bottom")));
            }
            userBox.$box.animate({"bottom":bottom+"px"}, 200);
            
        }
        
        UserBox.boxOnTop = userBox;
    }

    static boxClosed(userBox){
        if(userBox != UserBox.boxOnTop){
            UserBox.boxMaximized(UserBox.boxOnTop);
        }
    }

}