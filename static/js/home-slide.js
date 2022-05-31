var currentSlideIndex = 0; //Repésente l'indice du slide courant
var $slides = $('#slide .slide-element'); // Stocke les slides dans un objet
var delay = 7000; // Taille d'apparition d'une image
var shownImageRight = ON_MOBILE ? "" : "20%", //MArge à droite pour l'image lorsqu'elle est affichée
    hiddenImageRight = ON_MOBILE ? "-100%" : "-30%"; // ..................
var shownTextLeft = ON_MOBILE ? "0" : "15%", //MArge à gauche pour le texte lorsqu'il est affiché
    hiddenTextLeft = ON_MOBILE ? "-100%" : "-30%"; //...............
var animationSpeed = 1000;// Durée de l'animation 
var timer;

/**
 * Affiche le slide passé en paramètre avec les animations
 * 
 * @param $slide
 * @param {*} callback 
 */
function showSlide($slide, callback = null){
   
    $slide.find("img").animate({
        right:shownImageRight,
    }, animationSpeed);
    $slide.find(".slide-element-text").animate({
        left:shownTextLeft// Affiche l'image
    }, animationSpeed);
    $slide.find(".slide-element-text h4").animate(
        {step:4},
        {
            duration:(animationSpeed/1.5),
            step:function(val){
                $slide.find(".slide-element-text h4").css({"transform":"scale("+val+")"});
            },
            always:function(){
                $slide.find(".slide-element-text h4").animate(
                    {step:1},
                    {
                        duration:(animationSpeed/2),
                        step:function(val){
                            $slide.find(".slide-element-text h4").css({"transform":"scale("+(val)+")"});
                        }
                    }
                );
            }
        }
    );
    $slide.find(".slide-element-text p").animate(
        {step:0.5},
        {
            duration:(animationSpeed/1.5),
            step:function(val){
                $slide.find(".slide-element-text p").css({"transform":"scale("+val+")"});
            },
            always:function(){
                $slide.find(".slide-element-text p").animate(
                    {step:1},
                    {
                        duration:(animationSpeed/2),
                        step:function(val){
                            $slide.find(".slide-element-text p").css({"transform":"scale("+(val)+")"});
                        }
                    }
                );
            }
        }
    );
    $slide.fadeIn(animationSpeed, function(){//apparition de l'élément suivant
        if(callback != null){
            callback();
        }
    }); 
}

/**
 * Masque le slide passé en paramètre avec les animations
 * 
 * @param $slide
 * @param {*} callback 
 */
 function hideSlide($slide, callback = null){
    $slide.find("img").animate({
        right:hiddenImageRight // Masque l'image
    }, animationSpeed);

    $slide.find(".slide-element-text").animate({
        left:hiddenTextLeft// Masque l'image
    }, animationSpeed);
    $slide.find(".slide-element-text h4").animate(
        {step:7},
        {
            duration:(animationSpeed/2),
            step:function(val){
                $slide.find(".slide-element-text h4").css({"transform":"scale("+val+")"});
            }
        }
    );
    $slide.find(".slide-element-text p").animate(
        {step:0},
        {
            duration:(animationSpeed/2),
            step:function(val){
                $slide.find(".slide-element-text p").css({"transform":"scale("+val+")"});
            }
        }
    );
    $slide.fadeOut(animationSpeed, function(){//Disparition de l'élément suivant
        if(callback != null){
            callback();
        }
    }); 
}


/**
 * Fonction d'animation qui fait défiler les slides les uns à la suit edes autres
 */
function changeSlide(targetIndex = null){
    let $currentSlide = $slides.eq(currentSlideIndex);
    var nextSlideIndex = (targetIndex != null) ? targetIndex : currentSlideIndex+1;//Indice du prochain slide

    //Vérifier si on n'est pas à la fin des slides
    if(nextSlideIndex >= $slides.length)
        nextSlideIndex = 0;
    let $nextSlide = $slides.eq(nextSlideIndex);
    $("#slide #radios span").removeClass("active");
    $("#slide #radios span").eq(nextSlideIndex).addClass("active");
    hideSlide($currentSlide);

    showSlide($nextSlide, function(){//apparition de l'élément suivant
        currentSlideIndex = nextSlideIndex;
    }); 
}

/**
 * Inititalisation du slideshow
 */
 function init(){
    $slides.each(function(){
        $(this).hide(-1);
        $(this).find("img").css("right", hiddenImageRight);
        $(this).find(".slide-element-text").css("left", hiddenTextLeft);
    });
    showSlide($slides.eq(currentSlideIndex));
    timer = setInterval(changeSlide, delay); //Appel du slideshow après le delay

    //Ajout des radios
    for(let i =0; i<$slides.length;i++){
        $("#slide #radios").append("<span data-slide='"+i+"'></span>"); //Ajout du bouton
    }
    $("#slide #radios span").eq(0).addClass("active");

    //Gestion du clic sur l'un des boutons radios
    $("#slide #radios span").click(function(){
        clearInterval(timer);
        changeSlide(parseInt($(this).attr("data-slide")));
        timer = setInterval(changeSlide, delay);
    });
}
/*****code pour rendre les images dynamiques */

init();