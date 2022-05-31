<!-- 
    Page affichée après que le visiteur ait souscrit à la newsletter
-->   
{% block title %}Aide | Food-advice"; //Titre de la page?{% endblock %}

<?php ob_start(); ?>   
    <!-- Inclusions css ici -->   

<?php $_STYLES = ob_get_clean(); ?>

<?php ob_start(); ?>
    <!-- Contenu de la page ici -->
<div class="container">
    <h2 class="title">
        Souscription à la newsletter
    </h2>
    <p>
        <?php 
            if($alreadySubscriber) 
                echo "L'adresse <strong class='text-primary'>$email</strong> est déjà enregistrée pour la newsletter";
            else
                echo "Vous avez souscrit avec succès à la newsltter. votre adresse ne sera pas partagée";
        ?>
    </p>
    <h5 class="">
        Quelles informations allez-vous recevoir ?
    </h5>
</div>

<?php $_CONTENT = ob_get_clean(); ?>

<?php ob_start() ?>
    <!-- Code javascript ici -->
    

<?php $_SCRIPTS = ob_get_clean(); ?>

<?php require VIEW_DIR."/base.php"; ?>
