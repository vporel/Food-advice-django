<!-- 
    Vue présentant aux visiteurs une aide pour la naviagation dans le site
    Chemin /help
-->   
{% block title %}Aide | Food-advice"; //Titre de la page?{% endblock %}

<?php ob_start(); ?>   
    <!-- Inclusions css ici -->   
    <style>
        h1{


        }
        #help img{
            width:100%;
        }
    </style>
<?php $_STYLES = ob_get_clean(); ?>

<?php ob_start(); ?>
    <!-- Contenu de la page ici -->
<div class="container" id="help">
    <h1 class="title">AIDE</h1>
    <section>
        <h3>Effectuer une recherche</h3>
        <p>
            Pour éffectuer une recherche sur food-advice, il suffit juste de cliquer sur la loupe puis taper dans la barre de recherche
            le nom de l'aliment ou repas que vous recherchez.
            <img src="<?= $asset('images/captures/recherche.png'); ?>" alt="">
        </p>
    </section>
</div>

<?php $_CONTENT = ob_get_clean(); ?>

<?php ob_start() ?>
    <!-- Code javascript ici -->
    

<?php $_SCRIPTS = ob_get_clean(); ?>

<?php require VIEW_DIR."/base.php"; ?>
