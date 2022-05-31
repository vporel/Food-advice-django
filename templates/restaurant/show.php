
<?php $_TITLE = $aliment->nom." | Food-advice"; //Titre de la page ?>

<?php ob_start(); ?>  
    <!-- Inclusions css ici -->  
    <?= $css([
        "css/aliment-show.css"
    ]) ?>

<?php $_STYLES = ob_get_clean(); ?>
 
<?php ob_start(); ?>
    <!-- Contenu de la page ici -->

    <h2 id="restaurant-title">
        <?= $restaurant->nom ?>
    </h2>
<div class="container">
    <div class="row">
        <div class="col-12 col-md-5">
            <img src="<?= $asset("images/restaurants/".$restaurant->image) ?>" alt="" id="restaurant-image">
        </div>
        <div class="col-12 col-md-7" id="details">
            <div id="description">
                <?= $restaurant->description ?>
            </div>
            <hr>
            <?php if($restaurant->contributeur != null){ ?>
                <div>
                    <span class="label">Recommandé par : </span>
                    <span class="value"><?= $restaurant->contributeur ?></span>
                </div>
            <?php } ?>
            
                
        </div>
    </div>
    <div class="row mt-3">
        <div class="col-12 col-md-6 order-2 order-md-1">
            <h5 class="title">Restaurant du meme genre</h5>
        </div>
        <div class="col-12 col-md-6 order-1 order-md-2">
            <h5 class="title">Commentaires</h5>
            <?php if($app->user != null){ ?>
                <span>Ajouter un commentaire</span>
                <form id="new-comment-form">
                    <textarea id="comment-text" placeholder="Votre commentaire ici"></textarea>
                    <div class="d-flex justify-content-end mt-1">
                        <button class="btn btn-primary" id="add-comment" type="button">Ajouter</button>
                    </div>
                </form>
            <?php }else{ ?>
                <a id="btn-commenter" class="text-primary">Ajouter un commentaire</a>
            <?php } ?>
            <div id="commentaires" class="mt-2">
                <?php include VIEW_DIR."/load/comments.php"; ?>
            </div>
        </div>
    </div>
</div>
     
<?php $_CONTENT = ob_get_clean(); ?>

<?php ob_start() ?>
    <!-- Code javascript ici -->
    <script>
        const ALIMENT_ID = parseInt("<?= $aliment->id ?>");
    </script>
    <script src="<?= $asset("js/restaurant-show.js") ?>"></script>
    <script>
        updateStarsWithAverage(NOTES_AVERAGE);
    </script>
<?php $_SCRIPTS = ob_get_clean(); ?>

<?php require VIEW_DIR."/base.php"; ?>