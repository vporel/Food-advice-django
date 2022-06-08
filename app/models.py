"""
    FICHIER DE DEFINITIONS DE TOUTES LES CLASSES UTILISEES DANS LE PROJET
"""

from django.db import models
from django.core.validators import FileExtensionValidator
from django.db.models import Sum, Count, Case, When, F

IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "gif"]

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

class Commentable(models.Model):
    class Meta:
        abstract = True
    nom = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.FileField()
    approuve = models.BooleanField(default=False)
    contributeur = models.ForeignKey(Contributeur, models.CASCADE, null=True, blank=True, editable=False)
    dateCreation = models.DateTimeField(auto_now=True)
    dateDerniereModification = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nom

class Evaluable(Commentable):
    class Meta:
        abstract = True

    def nombreNotes(self):
        return self.evaluations.count()
    
    def totalNotes(self):
        sum = 0
        for evaluation in self.evaluations.all():
            sum += evaluation.note
        return sum

    def moyenneNotes(self):
        nombreNotes = self.nombreNotes()
        return self.totalNotes()/nombreNotes if nombreNotes > 0 else 0

    def noteContributeur(self,contributeur):
        try:
            evaluation = self.evaluations.get(contributeur=contributeur)
            return evaluation.note
        except Exception:
            return 0
    

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
class Repas(Evaluable):
    image = models.FileField(upload_to="static/images/repas/", validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)])
    momentJournee = models.IntegerField(choices=MOMENTS_JOURNEE, null=True, blank = True, verbose_name="Moment de la journée", help_text="Moment habituel de consommation de ce repas")
    origine = models.ForeignKey(OrigineRepas, models.CASCADE, null=True)
    
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

    def minerauxTableau(self):
        if self.recette == None:
            return []
        mineraux = []
        for aliment in self.recette.aliments.all():
            for mineral in aliment.minerauxTableau():
                mineral = mineral.lower().capitalize()
                if not mineraux.__contains__(mineral):
                    mineraux.append(mineral)
        return mineraux
    def mineraux(self):
        return ", ".join(self.minerauxTableau())

    def vitaminesTableau(self):
        if self.recette == None:
            return []
        vitamines = []
        for aliment in self.recette.aliments.all():
            for vitamine in aliment.vitaminesTableau():
                vitamine = vitamine.upper()
                if not vitamines.__contains__(vitamine):
                    vitamines.append(vitamine)
        return vitamines

    def vitamines(self):
        return ", ".join(self.vitaminesTableau())


    @staticmethod
    def filterList(nom=None, composition = None, paysOrigine = None, regionOrigine = None):
        filterDict = {}
        if nom != None:
            filterDict["nom__contains"] = nom
        if paysOrigine != None:
            filterDict["origine__pays__contains"] = paysOrigine
        if regionOrigine != None:
            filterDict["origine__region__contains"] = regionOrigine
        objects = Repas.objects.filter(approuve=True, **filterDict)
        filtreComposition = None
        if composition == "TGC" or composition == "TGD":
            filtreComposition = "tauxGlucides"
        elif composition == "TLC" or composition == "TLD":
            filtreComposition = "tauxLipides"
        elif composition == "TPC" or composition == "TPD":
            filtreComposition = "tauxProteines"
        prefixeOrdreFiltreComposition = "-" if composition == "TGD" or composition == "TLD" or composition == "TPD" or composition == "ACD" else ""
        if(filtreComposition != None):
            objects = objects.annotate(elementComposition=Sum("recette__alimentrecette__aliment__"+filtreComposition)/Count("recette__alimentrecette"))
            objects = objects.order_by(prefixeOrdreFiltreComposition+"elementComposition")
            
        if composition == "ACC" or composition == "ACD":
            objects = objects.annotate(apportCalorifique=(
                (
                    (Sum("recette__alimentrecette__aliment__tauxGlucides") + Sum("recette__alimentrecette__aliment__tauxProteines")) * 4
                    + Sum("recette__alimentrecette__aliment__tauxLipides") * 9
                ) * (F("recette__alimentrecette__aliment__masseUnite") / 100)
            ) /Count("recette__alimentrecette"))
            objects = objects.order_by(prefixeOrdreFiltreComposition+"apportCalorifique")
        return objects

class CommentaireRepas(Commentaire):
    repas = models.ForeignKey(Repas, models.CASCADE)

class EvaluationRepas(Evaluation):
    repas = models.ForeignKey(Repas, models.CASCADE, related_name="evaluations")


class TypeAliment(models.Model):
    nom = models.CharField(max_length=30)
    detailRisques = models.TextField(null=True, blank=True)
    detailApports = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nom

class Aliment(Commentable):
    uniteComptage = models.CharField(max_length=30, verbose_name="Unité de comptage", null=True, blank=True, help_text="Comment on compte l'aliment (ex:doigt pour une banane)")
    masseUnite = models.FloatField(verbose_name="Masse unité (g)", help_text="La masse en grammes d'un élément (ex: 120 pour la banage)")
    image = models.FileField(upload_to="static/images/aliments/", validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)])
    tauxProteines = models.FloatField(default=0, verbose_name="Taux de proteines", help_text="Taux de proteines dans 100g")
    tauxLipides = models.FloatField(default=0, verbose_name="Taux de lipides", help_text="Taux de lipides dans 100g")
    tauxGlucides = models.FloatField(default=0, verbose_name="Taux de glucides", help_text="Taux de glucides dans 100g")
    mineraux = models.CharField(max_length=255, null=True, blank=True, verbose_name="Mineraux", help_text="Motif : mineral1, minearl2, ...")
    vitamines = models.CharField(max_length=255, null=True, blank=True, verbose_name="Vitamines", help_text="Motif : vitamine1, vitamine2, ...")
    detailApports = models.TextField(null=True, blank=True, verbose_name="Détail des apports", help_text="Vertus de l'aliment")
    detailRisques = models.TextField(null=True, blank=True, verbose_name="Détail des risques", help_text="Problèmes liés à une consommation non suivie")
    type = models.ForeignKey(TypeAliment, models.CASCADE, verbose_name="Type")

    def minerauxTableau(self):
        return [] if self.mineraux == None else [mineral.strip() for mineral in self.mineraux.split(",")]

    def vitaminesTableau(self):
        return [] if self.vitamines == None else [vitamine.strip() for vitamine in self.vitamines.split(",")] 
    
    def calories(self):
        return round(((((self.tauxGlucides + self.tauxProteines) * 4) + (self.tauxLipides * 9)) * (self.masseUnite / 100)), 2)

    def __str__(self):
        return self.nom + (" (en "+self.uniteComptage+")" if self.uniteComptage != None else "")
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

    def  __str__(self):
        return str(self.recette) + " - " + str(self.aliment)
class CommentaireAliment(Commentaire):
    aliment = models.ForeignKey(Aliment, models.CASCADE)

class Restaurant(Evaluable):
    image = models.FileField(upload_to="static/images/restaurants/", validators=[FileExtensionValidator(allowed_extensions=IMAGE_EXTENSIONS)])
    adresse = models.CharField(max_length=100)
    repass = models.ManyToManyField(Repas)

class CommentaireRestaurant(Commentaire):
    restaurant = models.ForeignKey(Restaurant, models.CASCADE)

class EvaluationRestaurant(Evaluation):
    restaurant = models.ForeignKey(Restaurant, models.CASCADE,related_name="evaluations")


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
    class Meta:
        unique_together = ["contributeur", "professionnel"]

    """
        Les messages non lus pour le contributeur en paramètre sil est dans la conversation
    """
    def messagesNonLus(self, contributeur):
        if(self.contributeur == contributeur):
            return self.message_set.filter(lu=False, expediteur=2)
        elif self.professionnel == contributeur:
            return self.message_set.filter(lu=False, expediteur=1)
        else:
            raise Exception("Le contributeur "+contributeur.nomUtilisateur+" ne fait pas partie de cette conversation")
        return None
    
    def nbreMessagesNonLus(self, contributeur):
        return self.messagesNonLus(contributeur).count()

    """
        Supprime la conversation pour contributeur
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
    expediteur = models.IntegerField() # 1 pour le contributeur, 2 pour le professionnel
    date = models.DateTimeField(auto_now=True)

    def objetExpediteur(self):
        if self.expediteur == 1:
            return self.conversation.contributeur
        else:
            return self.conversation.professionnel
    
    def __setattr__(self, name:str, value):
        if name == "expediteur":
            if value == None:
                return
            elif type(value) == int:
                if value != 1 and value != 2:
                    raise Exception("Les valeurs entières acceptées pour la propriété expediteur sont 1 (Contributeur) et 2 (professionnel)");
            elif type(value) == str:
                value = value.lower()
                if value == "contributeur":
                    value = 1
                elif value == "professionnel": 
                    value = 2
                else:
                    raise Exception("Les chaines acceptées pour la propriété expediteur sont 'contributeur' et 'professionnel'");
            elif type(value) == Contributeur:
                if self.conversation.contributeur == value:
                    value = 1
                else:
                    value = 2
            else:
                raise Exception("Type de la propriété 'expediteur' non pris en compte");
        super().__setattr__(name, value)
        

class AdresseNewsletter(models.Model):
    email = models.CharField(max_length=255)