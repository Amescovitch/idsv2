from django import forms
from .models import *
from .choix import *
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)



class PermissionForm(forms.ModelForm):
    NomComplet = forms.CharField(
        label="Mr / Mme / Mlle",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': "Veuillez fournir votre nom complet.",
        }
    )
    poste = forms.ChoiceField(
        label="Poste occupé",
        choices=POSTE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={
            'required': "Veuillez sélectionner un poste.",
        }
    )
    service = forms.ChoiceField(
        label="Service relatif",
        choices=SERVICE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={
            'required': "Veuillez sélectionner un service.",
        }
    )
    motif = forms.CharField(
        label="Motif de la demande",
        widget=forms.Textarea(attrs={'placeholder': 'Pourquoi vous demandez la permission ?', 'class': 'form-control', 'rows': 2}),
        error_messages={
            'required': "Veuillez fournir le motif de la demande.",
        }
    )
    lieu = forms.CharField(
        label="Lieu à se rendre",
        widget=forms.TextInput(attrs={'placeholder': 'Où allez-vous ?', 'class': 'form-control'}),
        error_messages={
            'required': "Veuillez fournir le lieu à se rendre.",
        }
    )
    date_heure_sortie = forms.DateTimeField(
        label="Date et heure de sortie",
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'placeholder': 'dd/mm/yyyy HH:MM', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        ),
        error_messages={
            'required': "Veuillez fournir la date et l'heure de sortie.",
        }
    )
    date_heure_retour = forms.DateTimeField(
        label="Date et heure de retour",
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'placeholder': 'dd/mm/yyyy HH:MM', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        ),
        error_messages={
            'required': "Veuillez fournir la date et l'heure de retour.",
        }
    )
    raison_rejet = forms.CharField(
        label="Raison du rejet",
        widget=forms.TextInput(attrs={'placeholder': 'Expliquez un peu le pourquoi vous rejetez la demande', 'class': 'form-control', 'rows':2 }),
        required=False,
        error_messages={
            'required': "Veuillez fournir la raison du rejet.",
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        date_heure_sortie = cleaned_data.get('date_heure_sortie')
        date_heure_retour = cleaned_data.get('date_heure_retour')

        if date_heure_sortie and date_heure_retour:
            if date_heure_sortie < timezone.now():
                self.add_error('date_heure_sortie', "La date de sortie doit être ultérieure ou égale à l'heure actuelle.")

            if date_heure_retour < timezone.now():
                self.add_error('date_heure_retour', "La date de retour doit être ultérieure ou égale à l'heure actuelle.")

            if date_heure_sortie >= date_heure_retour:
                self.add_error('date_heure_retour', "La date de retour doit être postérieure à la date de sortie.")

        return cleaned_data


    class Meta:
        model = DemandePermission
        fields = ['NomComplet', 'poste', 'service', 'motif', 'date_heure_sortie', 'lieu', 'date_heure_retour', 'raison_rejet']
        

class InscriptionForm(UserCreationForm):
    nom = forms.CharField(
        label=_("Nom"),
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Votre nom', 'class': 'form-control'}),
        error_messages={
            'required': _("Veuillez fournir votre nom."),
        }
    )
    prenom = forms.CharField(
        label=_("Prénom"),
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Votre prénom', 'class': 'form-control'}),
        error_messages={
            'required': _("Veuillez fournir votre prénom."),
        }
    )
    username = forms.CharField(
        label=_("Nom d'utilisateur"),
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur", 'class': 'form-control'}),
        error_messages={
            'required': _("Veuillez fournir un nom d'utilisateur."),
            'unique': _("Ce nom d'utilisateur est déjà utilisé."),
        }
    )
    email = forms.EmailField(
        label=_("Adresse e-mail"),
        widget=forms.EmailInput(attrs={'placeholder': 'Votre adresse e-mail', 'class': 'form-control'}),
        error_messages={
            'required': _("Veuillez fournir une adresse e-mail."),
            'unique': _("Cette adresse e-mail est déjà utilisée."),
        }
    )
    poste = forms.ChoiceField(
        label=_("Poste"),
        choices=Personnel.POSTE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={
            'required': _("Veuillez sélectionner un poste."),
        }
    )
    service = forms.ChoiceField(
        label=_("Service"),
        choices=Personnel.SERVICE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={
            'required': _("Veuillez sélectionner un service."),
        }
    )
    direction = forms.ChoiceField(
        label=_("Direction"),
        choices=Personnel.DIRECTION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={
            'required': _("Veuillez sélectionner une direction."),
        }
    )
    telephone = forms.CharField(
        label=_("Numéro de téléphone"),
        widget=forms.TextInput(attrs={'placeholder': 'Numéro de téléphone', 'class': 'form-control'}),
        error_messages={
            'required': _("Veuillez fournir un numéro de téléphone."),
        }
    )
    password1 = forms.CharField(
        label=_("Mot de passe"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'class': 'form-control'}),
        error_messages={
            'required': _("Veuillez fournir un mot de passe."),
        }
    )
    password2 = forms.CharField(
        label=_("Confirmer le mot de passe"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer le mot de passe', 'class': 'form-control'}),
        error_messages={
            'required': _("Veuillez confirmer votre mot de passe."),
            'password_mismatch': _("Les mots de passe ne correspondent pas."),
        }
    )

    class Meta:
        model = Personnel
        fields = ('nom', 'prenom', 'username', 'email', 'poste', 'service', 'direction', 'telephone')
        error_messages = {
            'password1': {
                'required': _("Veuillez fournir un mot de passe."),
            },
            'password2': {
                'required': _("Veuillez confirmer votre mot de passe."),
                'password_mismatch': _("Les mots de passe ne correspondent pas."),
            },
        }
