<!-- 
    regles pour faire des recommandations 
-->   
{% block title %}Politique de Recommendation | Food-advice"; //Titre de la page?{% endblock %}

<?php ob_start(); ?>   
    <!-- Inclusions css ici -->  
    
<?php $_STYLES = ob_get_clean(); ?>

<?php ob_start(); ?>
    <!-- Contenu de la page ici -->
<div class="container">
    <h4 class="title mb-5"> Quelques astuces apres une recommandation:</h4>
    <div class="row">
        <h6>1. Il est possible de supprimer votre recommandation tant qu'elle n'a pas encore ete approuvee.</h6>
        <h6>2. Vous pouvez egalement modifier votre recommandation tant qu'elle n'est pas approuvee.</h6>
    </div>
</div>

<?php $_CONTENT = ob_get_clean(); ?>

<?php ob_start() ?>
    <!-- Code javascript ici -->
    

<?php $_SCRIPTS = ob_get_clean(); ?>

<?php require VIEW_DIR."/base.php"; ?>
