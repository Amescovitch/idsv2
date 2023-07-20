from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from datetime import date
from .choix import *


class CustomUserManager(BaseUserManager):
    def create_user(self, nom, prenom, username, email, password=None, poste=None, service=None, telephone=None):
        # Crée un utilisateur avec les champs fournis
        user = self.model(
            nom=nom,
            prenom=prenom,
            username=username,
            email=self.normalize_email(email),
            poste=poste,
            service=service,
            telephone=telephone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nom, prenom, username, email, password=None, poste=None, service=None, telephone=None):
        # Crée un superutilisateur avec les champs fournis
        user = self.create_user(
            nom=nom,
            prenom=prenom,
            username=username,
            email=self.normalize_email(email),
            password=password,
            poste=poste,
            service=service,
            telephone=telephone,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Personnel(AbstractBaseUser, PermissionsMixin):
    POSTE_CHOICES = (
        ('Stagiaire', 'Stagiaire'),
        ('Employe', 'Employé'),
        ('ChefService', 'Chef Service'),
        ('Administrateur', 'Administrateur'),
        ('ServicePersonnel', 'Service Personnel'),
        ('DirecteurGeneral', 'Directeur Général'),
        ('DirecteurDepartement', 'Directeur de Département'),
    )

    SERVICE_CHOICES = (
        ('Aucun', 'Aucun Service Particulier'),
        ('ServiceReseauxClients', 'Service Reseaux et Clients'),
        ('ServiceSupportAlvanet', 'Service Support ALAVANET'),
        ('ServiceLogicielFormation', 'Service Logiciel et Formation'),
        ('ServiceCommercial', 'Service Commercial'),
        ('ServiceAdministratifRessourcesHumaines', 'Service Administratif et des Ressources Humaines'),
        ('EquipeLogistiqueCommerciale', 'Equipe Logistique et Commerciale'),
        ('Direction', 'Direction'),
        ('Administration', 'Administration'),
    )

    DIRECTION_CHOICES = (
        ('Aucune', 'Aucune Direction Particulière'),
        ('DirectionTechnique', 'Direction Technique'),
        ('DirectionCommercialeMarketingCommunication', 'Direction Commerciale, Marketing et Communication'),
        ('DirectionAdministrativeRessourcesHumaines', 'Direction Administrative et des Ressources Humaines'),
    )

    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    poste = models.CharField(max_length=255, choices=POSTE_CHOICES)
    service = models.CharField(max_length=255, choices=SERVICE_CHOICES)
    direction = models.CharField(max_length=100, choices=DIRECTION_CHOICES, default="")
    telephone = PhoneNumberField()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nom', 'prenom', 'email', 'poste', 'service', 'telephone']



class DemandePermission(models.Model):
    initiateur = models.ForeignKey(Personnel, on_delete=models.SET_NULL, null=True, blank=True, related_name='demandes_initiees')
    validateurs = models.ManyToManyField(Personnel, blank=True, related_name='demandes_validees')
    rejeteurs_strict = models.ManyToManyField(Personnel, blank=True, related_name='demandes_strictements_rejetees')
    rejeteurs_pour_correction = models.ManyToManyField(Personnel, blank=True, related_name='demandes_rejetees_pour_corrections')
    valide_par = models.ForeignKey(Personnel, on_delete=models.SET_NULL, null=True, blank=True, related_name='demandes_vérifiees')
    date_emission = models.DateTimeField(default=timezone.now)
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES)

    NomComplet = models.CharField(max_length=100)
    poste = models.CharField(max_length=100, choices=POSTE_CHOICES)
    service = models.CharField(max_length=255, choices=SERVICE_CHOICES)
    direction = models.CharField(max_length=100, choices=DIRECTION_CHOICES, default="")
    
    motif = models.TextField()
    lieu = models.CharField(max_length=100)
    date_heure_sortie = models.DateTimeField()
    date_heure_retour = models.DateTimeField()
    raison_rejet = models.TextField(blank=True, null=True)

    def clean(self):
        now = timezone.now()
        if self.date_heure_sortie and self.date_heure_retour:
            if self.date_heure_sortie < now or self.date_heure_retour < now:
                raise ValidationError("Les dates de sortie et de retour doivent être supérieures ou égales à l'heure actuelle.")
            if self.date_heure_sortie >= self.date_heure_retour:
                raise ValidationError("La date de sortie doit être antérieure à la date de retour.")

    def __str__(self):
        return f"Demande de {self.NomComplet}"


class Notification(models.Model):
    user = models.ForeignKey(Personnel, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
