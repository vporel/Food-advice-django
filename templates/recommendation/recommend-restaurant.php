<!-- 
   recommendation de restaurant
-->   
{% block title %}Recommendation restaurant | Food-advice"; //Titre de la page?{% endblock %}

<?php ob_start(); ?>   
    <!-- Inclusions css ici -->   
    
<?php $_STYLES = ob_get_clean(); ?>

<?php ob_start(); ?>
    <!-- Contenu de la page ici -->
<div class="container">
    <h4 class="title">Recommandation d'un restaurant</h4>
    <?php if($message != ""){ ?>
        <div class="alert alert-warning"><?= $message; ?></div>
    <?php } ?>
    <form method="post" enctype="multipart/form-data"><!-- enctype : permet au formulaire gerer l'envoie de fichiers -->
        <?php echo $form->createHTML(); //création du formulaire de façon automatique avec un framework?>
        <div class="mt-2 text-end"><!-- style du boutton "continuer" -->
            <button type="submit" class="btn btn-primary">Continuer</button>
        </div>
    </form>
</div>

<?php $_CONTENT = ob_get_clean(); ?>

<?php ob_start() ?>
    <!-- Code javascript ici -->
    

<?php $_SCRIPTS = ob_get_clean(); ?>

<?php require VIEW_DIR."/base.php"; ?>
