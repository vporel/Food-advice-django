
{% block title %}Accueil | Food-advice"; //Titre de la page ?{% endblock %}

<?php ob_start(); ?>  
    <!-- Inclusions css ici -->  
    <?= $css([
        "css/aliments-liste.css"
    ]) ?>

<?php $_STYLES = ob_get_clean(); ?>

<?php ob_start(); ?>
<!-- Contenu de la page ici -->
<div class="container mt-2" id="list">
    <h5 class="title">Filtres</h5>
    <div id="filtres" class="row">
        <div class="col-12 col-md-4">
            <label>Nom </label>
            <input type="text" id="filtre-nom-restaurant"class="form-control"placeholder="Nom du restaurant" value="<?= $nom ?? "" ?>">
        </div>
        <div class="col-12 col-md-3">
            <label>Adresse </label>
            <input type="text" id="filtre-adresse"class="form-control"placeholder="">
        </div>
        <div class="col-12 col-md-4">
            <label>Repas </label>
            <input type="text" id="filtre-nom-repas"class="form-control" placeholder="Nom du repas">
        </div>
        <div class="col-12 col-md-1 d-flex align-items-end">
            <button class="btn btn-primary" onclick="filter()">Appliquer</button>
        </div>
    </div>
    <?php 
        include VIEW_DIR."/components/_loading.php";
    ?>
    <div id="elements" class="mt-3">
        <?php 
            include VIEW_DIR."/load/restaurants.php";
        ?>
    </div>
    <hr>
</div>
     
<?php $_CONTENT = ob_get_clean(); ?>

<?php ob_start() ?>
    <!-- Code javascript ici -->

    <?= $js("js/home-slide.js"); ?>
    <script>
        /**
         * Fonction pour l'application du filtre
         */
        function filter(){
            $('#list .loading').show(200);
            $('#list #elements').html("");
            $.post("/restaurants/filtre", {
                nomRestaurant:$("#filtre-nom-restaurant").val(),
                adresse:$("#filtre-adresse").val(),
                nomRepas:$("#filtre-nom-repas").val(),
            }, function(response){
                $('#list #elements').html(response);
                $('#list .loading').hide(200);
            });
        }
    </script>

<?php $_SCRIPTS = ob_get_clean(); ?>

<?php require VIEW_DIR."/base.php"; ?>