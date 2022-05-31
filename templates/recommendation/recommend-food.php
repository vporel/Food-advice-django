<!-- 
   recommendation de repas
-->   
{% block title %}Recommendation repas | Food-advice"; //Titre de la page?{% endblock %}

<?php ob_start(); ?>   
    <!-- Inclusions css ici -->   
    
<?php $_STYLES = ob_get_clean(); ?>

<?php ob_start(); ?>
    <!-- Contenu de la page ici -->
<div class="container">
    <h4 class="title">Recommandation d'un repas</h4>
    <?php if($message != ""){ ?>
        <div class="alert alert-warning"><?= $message; ?></div>
    <?php } ?>
    <form method="post" enctype="multipart/form-data" class="row row-cols-1 row-cols-md-2"><!-- enctype : permet au formulaire gerer l'envoie de fichiers -->
        <?php echo $form->createHTML(); //création du formulaire de façon automatique avec un framework?>
        <div class="mt-2 text-end col-12 col-md-12"><!-- style du boutton "continuer" -->
            <button type="submit" class="btn btn-primary">Continuer</button>
        </div>
    </form>
</div>

<?php $_CONTENT = ob_get_clean(); ?>

<?php ob_start() ?>
    <!-- Code javascript ici -->
    

<?php $_SCRIPTS = ob_get_clean(); ?>

<?php require VIEW_DIR."/base.php"; ?>
