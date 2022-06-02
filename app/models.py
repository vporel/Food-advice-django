"""
    FICHIER DE DEFINITIONS DE TOUTES LES CLASSES UTILISEES DANS LE PROJET
"""

from django.db import models
from django.core.validators import FileExtensionValidator

class Contributeur(models.Model):
    nom = models.CharField(max_length=50, verbose_name="Nom complet")
    nomUtilisateur = models.CharField(max_length=30, verbose_name="Nom d'utilisateur", unique=True)
    motDePasse = models.CharField(max_length=255, verbose_name="Mot de passe")
    email = models.CharField(max_length=255, null=True, blank=True, verbose_name="Adresse email")
    professionnelSante = models.BooleanField(default=False, verbose_name="Professionnel de la santé")

    """
        Retourne les contributeurs professionels
    """
    @staticmethod
    def professionnels():
        return Contributeur.objects.filter(professionnelSante=True)

    """
        Nombre total de messages non lus par le contributeur, toutes les conversations confonfues
    """
    def nbreMessagesNonLus(self):
        nbreMessagesNonLus = 0
        for conversation in self.conversationsProfessionnels.all():
            nbreMessagesNonLus += conversation.nbreMessagesNonLus(self)
        if self.professionnelSante:
            for conversation in self.conversationsContributeurs.all():
                nbreMessagesNonLus += conversation.nbreMessagesNonLus(self)
        return nbreMessagesNonLus

    def __str__(self):
        return self.nomUtilisateur

IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "gif"]
class Commentable(models.Model):
    class Meta:
        abstract = True
    nom = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField()
    approuve = models.BooleanField(default=False)
    contributeur = models.ForeignKey(Contributeur, models.CASCADE, null=True, blank=True)
    dateCreation = models.DateTimeField(auto_now=True)
    dateDerniereModification = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nom

class Evaluable(Commentable):
    class Meta:
        abstract = True
    nombreNotes = models.IntegerField(default=0)
    totalNotes = models.IntegerField(default=0)

class Evaluation(models.Model):
    class Meta:
        abstract = True
    note = models.IntegerField()
    contributeur = models.ForeignKey(Contributeur, models.CASCADE)


class Commentaire(models.Model):
    class Meta:
        abstract = True
    texte = models.TextField()
    date = models.DateTimeField(auto_now=True)
    contributeur = models.ForeignKey(Contributeur,models.CASCADE)


class OrigineRepas(models.Model):
    pays = models.CharField(max_length=20)
    region = models.CharField(max_length=20)
    class Meta:
        unique_together = ["pays", "region"]
    def __str__(self) -> str:
        return self.pays+", "+self.region

MOMENTS_JOURNEE = [
    (1, 'Matin'),
    (2, 'Midi'),
    (3, 'Soir')
]
class Repas(Commentable):
    image = models.FileField(upload_to="static/images/repas/", validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)])
    momentJournee = models.IntegerField(choices=MOMENTS_JOURNEE, null=True)
    origine = models.ForeignKey(OrigineRepas, models.CASCADE, null=True)

    def momentJourneeText(self):
        for m in MOMENTS_JOURNEE:
            if(m[0] == self.momentJournee):
                return m[1]
    def getNoteContributeur(self,contributeur):
        try:
            evaluation = EvaluationRepas.objects.get(contributeur=contributeur)
            return evaluation.note
        except EvaluationRepas.DoesNotExist:
            return 0
    
    def tauxGlucides(self):
        if self.recette is None or self.recette.aliments.count()== 0:
            return None
        aliments = self.recette.aliments.all()
        sommeTaux = 0
        for aliment in aliments:
            sommeTaux += aliment.tauxGlucides
        return round(sommeTaux/aliments.count(), 2)

    def tauxLipides(self):
        if self.recette is None or self.recette.aliments.count()== 0:
                return None
        aliments = self.recette.aliments.all()
        sommeTaux = 0
        for aliment in aliments:
            sommeTaux += aliment.tauxLipides
        return round(sommeTaux/aliments.count(), 2)

    def tauxProteines(self):
        if self.recette is None or self.recette.aliments.count()== 0:
                return None
        aliments = self.recette.aliments.all()
        sommeTaux = 0
        for aliment in aliments:
            sommeTaux += aliment.tauxProteines
        return round(sommeTaux/aliments.count(), 2)

    def calories(self):
        if self.recette is None or self.recette.aliments.count()== 0:
            return None
        alimentsRecettes = self.recette.alimentrecette_set.all()
        somme = 0
        for alimentRecette in alimentsRecettes:
            somme += alimentRecette.calories()
        return somme

    def caloriesUnePersonne(self):
        if self.recette is None or self.recette.aliments.count()== 0:
            return None
        return round(self.calories() / self.recette.nombrePersonnes, 2);

    def minerauxText(self):
        """
        if($this.recette == null)
            return "";
        $mineraux = [];
        for aliment in self.recette.aliments.all():
            foreach(aliment.Mineraux() as $mineral){
                $mineral = ucfirst(strtolower($mineral));
                if(!in_array($mineral, $mineraux)){
                    $mineraux[] = $mineral;
                }
            }
        }
        return implode(", ", $mineraux);
        """
        pass

    def vitaminesText(self):
        """
        if($this.recette == null)
            return "";
        $vitamines = [];
        for aliment in self.recette.aliments.all():
            foreach(aliment.Vitamines() as $vitamine){
                $vitamine = strtoupper($vitamine);
                if(!in_array(strtoupper($vitamine), $vitamines)){
                    $vitamines[] = $vitamine;
                }
            }
        }
        return implode(", ", $vitamines);
        """
        pass

    @staticmethod
    def filterOnList(nom, composition, repasOrigine, regionOrigine):
        pass

class CommentaireRepas(Commentaire):
    repas = models.ForeignKey(Repas, models.CASCADE)

class EvaluationRepas(Evaluation):
    repas = models.ForeignKey(Repas, models.CASCADE)


class TypeAliment(models.Model):
    nom = models.CharField(max_length=30)
    detailRisques = models.TextField(null=True, blank=True)
    detailApports = models.TextField(null=True, blank=True)

class Aliment(Commentable):
    uniteComptage = models.CharField(max_length=30, null=True, blank=True)
    masseUnite = models.FloatField()
    image = models.FileField(upload_to="static/images/aliments/", validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)])
    tauxProteines = models.FloatField(default=0)
    tauxLipides = models.FloatField(default=0)
    tauxGlucides = models.FloatField(default=0)
    mineraux = models.CharField(max_length=255, null=True, blank=True)
    vitamines = models.CharField(max_length=255, null=True, blank=True)
    detailApports = models.TextField(null=True, blank=True)
    detailRisques = models.TextField(null=True, blank=True)
    type = models.ForeignKey(TypeAliment, models.CASCADE)

    def calories(self):
        return round(((((self.tauxGlucides + self.tauxProteines) * 4) + (self.tauxLipides * 9)) * (self.masseUnite / 100)), 2)

class Recette(models.Model):
    repas = models.OneToOneField(Repas, models.CASCADE, primary_key=True)
    nombrePersonnes = models.IntegerField()
    tempsPreparation = models.IntegerField(null=True)
    tempsCuisson = models.IntegerField(null=True)
    detailPreparation = models.TextField(null=True, blank=True)
    aliments = models.ManyToManyField(Aliment, through='AlimentRecette', through_fields=("recette", "aliment"))
    
    def __str__(self):
        return str(self.repas)

class AlimentRecette(models.Model):
    aliment = models.ForeignKey(Aliment, models.CASCADE)
    recette = models.ForeignKey(Recette, models.CASCADE)
    quantite = models.IntegerField()
    class Meta:
        unique_together = [['aliment', 'recette']]
        
    def calories(self):
        return self.aliment.calories() * self.quantite

class CommentaireAliment(Commentaire):
    aliment = models.ForeignKey(Aliment, models.CASCADE)

class Restaurant(Commentable):
    image = models.FileField(upload_to="static/images/restaurants/", validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)])
    adresse = models.CharField(max_length=100)
    repass = models.ManyToManyField(Repas)

class CommentaireRestaurant(Commentaire):
    restaurant = models.ForeignKey(Restaurant, models.CASCADE)

class EvaluationRestaurant(Evaluation):
    restaurant = models.ForeignKey(Restaurant, models.CASCADE)


class RepasConsomme(models.Model):
    date = models.DateField()
    momentJournee = models.IntegerField(choices=MOMENTS_JOURNEE)
    repas = models.ForeignKey(Repas, models.CASCADE)
    contributeur = models.ForeignKey(Contributeur, models.CASCADE)

class Conversation(models.Model):
    visiblePourContributeur = models.BooleanField(default=True)
    visiblePourProfessionnel = models.BooleanField(default=True)
    contributeur = models.ForeignKey(Contributeur, models.CASCADE, related_name="conversationsProfessionnels")
    professionnel = models.ForeignKey(Contributeur, models.CASCADE, related_name="conversationsContributeurs")
    dateDernierMessage = models.DateTimeField(null=True)

    """
        Les messages non lus pour le contributeur en paramètre sil est dans la conversation
    """
    def messagesNonLus(self, contributeur):
        if(self.contributeur == contributeur):
            return self.message_set.objects.filter(lu=False, expediteur=2)
        elif self.professionnel == contributeur:
            return self.message_set.objects.filter(lu=False, expediteur=1)
        else:
            raise Exception("Le contributeur "+contributeur.nomUtilisateur+" ne fait pas partie de cette conversation")
        return None
    
    def nbreMessagesNonLus(self, contributeur):
        return self.messagesNonLus(contributeur).count()

    """
        Supprime la conversation pour $contributeur
        L'enregistrement n'est pas réelement supprimé de la base de donnée mais plutôt masqué pour le contributeur
    """
    def supprimer(self, contributeur):
        if self.contributeur.id == contributeur.id:
            self.visiblePourContributeur = False
        elif self.professionnel.id == contributeur.id:
            self.visiblePourProfessionnel = False
        else:
            raise Exception("Le contributeur "+contributeur.nomUtilisateur+" ne fait pas partie de cette conversation")
    
    """
        Le dernier message envoyé dans la conversation
    """
    def dernierMessage(self):
        messages = self.message_set.order_by("-id")
        return messages[0] if messages.count() > 0 else None

class Message(models.Model):
    message = models.TextField()
    lu = models.BooleanField(default=False)
    conversation = models.ForeignKey(Conversation, models.CASCADE)
    expediteur = models.ForeignKey(Contributeur, models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __init__(self, conversation, **args):
        super().__init__(args)
        self.conversation = conversation
    
    def objetExpediteur(self):
        if self.expediteur == 1:
            return self.conversation.contributeur
        else:
            return self.conversation.professionnel
        

class AdresseNewsletter(models.Model):
    email = models.CharField(max_length=255)