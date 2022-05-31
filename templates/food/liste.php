
{% block title %}Accueil | Food-advice"; //Titre de la page ?{% endblock %}

<?php ob_start(); ?>  
    <!-- Inclusions css ici -->  
    <?= $css([
        "css/repas-liste.css"
    ]) ?>

<?php $_STYLES = ob_get_clean(); ?>

<?php ob_start(); ?>
<!-- Contenu de la page ici -->
<div class="container mt-2" id="list">
    <h5 class="title">Filtres</h5>
    <div id="filtres" class="row">
        <div class="col-12 col-md-3">
            <label>Nom </label>
            <input type="text" id="filtre-nom"class="form-control" value="<?= $nom ?? "" ?>">
        </div>
        <div class="col-12 col-md-4">
            <label>Régime</label> 
            <select id="filtre-regime" class="form-select">
                <option value="">Peu importe</option>
                <option value="RM">Regime Minceur</option>
                <option value="RG">Regime Grosseur</option>
            </select>
        </div>
        <div class="col-12 col-md-4">
            <label>Composition</label> 
            <select id="filtre-composition" class="form-select">
                <option value="">Peu importe</option>
                <option value="TGC">Taux de glucides croissant</option>
                <option value="TGD">Taux de glucides décroissant</option>
                <option value="TLC">Taux de lipides croissant</option>
                <option value="TLD">Taux de lipides décroissant</option>
                <option value="TPC">Taux de proteines croissant</option>
                <option value="TPD">Taux de proteines décroissant</option>
                <option value="ACC">Apport calorifique croissant</option>
                <option value="ACD">Apport calorifique décroissant</option>
            </select>
        </div>
        <div class="col-12 col-md-1 d-flex align-items-end">
            <button class="btn btn-primary" onclick="filter()">Appliquer</button>
        </div>
    </div>
    <?php 
        include VIEW_DIR."/components/_loading.php";
    ?>
    <div id="repass">
        <?php 
            include VIEW_DIR."/load/foods.php";
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
            $('#list #repass').html("");
            $.post("/repas/filtre", {
                nom:$("#filtre-nom").val().trim(),
                regime:$("#filtre-regime").val(),
                composition:$("#filtre-composition").val()
            }, function(response){
                $('#list #repass').html(response);
            $('#list .loading').hide(200);
            });
        }
    </script>

<?php $_SCRIPTS = ob_get_clean(); ?>

<?php require VIEW_DIR."/base.php"; ?>