from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.views import LoginView, PasswordResetView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from .forms import *
from .choix import *

## inscription des personnels
def admin_check(user):
    return user.is_authenticated and user.poste == 'Administrateur'

@login_required(login_url="/")
@user_passes_test(admin_check, login_url="applicationidsdemande:erreur")
def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = user.username
            messages.success(request, f"<span class='username'>@{username}</span> créé.")
            return redirect('applicationidsdemande:inscription')
        else:
            #messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
            pass
    else:
        form = InscriptionForm()
    
    context = {'form': form}
    return render(request, 'inscription.html', context)


## connexion du personnel et redirection appropriée
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.poste == 'Administrateur':
                    #return redirect('applicationidsdemande:inscription')
                    return redirect('applicationidsdemande:accueil_admin')
                elif user.poste in ['ChefService', 'DirecteurGeneral', 'DirecteurDepartement', 'ServicePersonnel']:
                    return redirect('applicationidsdemande:accueil_validateur')
                else:
                    return redirect('applicationidsdemande:accueil_personnel')
            else:
                error_message = 'Nom d\'utilisateur et/ou mot de passe incorrect(s).'
    else:
        form = LoginForm()
        error_message = ''

    context = {
        'form': form,
        'error_message': error_message
    }
    return render(request, 'index.html', context)


## acuueil de l'administarteur
@login_required(login_url="/")
def accueil_admin(request):
    return render (request,'accueil_admin.html')


## accueil du validateur (un cs, un dp, un sp ou un dg)
@login_required(login_url="/")
def accueil_validateur(request):
    return render(request, 'accueil_validateur.html')



## accueil du reste du personnel
@login_required(login_url="/")
def accueil_personnel(request):
    return render (request,'accueil_personnel.html')


#réinitialisation du mot de passe 1/4
def custom_password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            return redirect('applicationidsdemande:password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})


#réinitialisation du mot de passe 2/4
def custom_password_reset_done(request):
    return render(request, 'password_reset_done.html')


#réinitialisation du mot de passe 3/4
def custom_password_reset_confirm(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64).decode()
    user = Personnel.objects.get(pk=uid)

    if default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('applicationidsdemande:password_reset_complete')
        else:
            form = SetPasswordForm(user)
        
        context = {
            'form': form,
            'uidb64': uidb64,
            'token': token
        }
        return render(request, 'password_reset_confirm.html', context)

    # Si le lien de réinitialisation du mot de passe est invalide, 
    #rediriger vers une page d'erreur ou afficher un message d'erreur
    return render(request, 'password_reset_invalid.html')


#réinitialisation du mot de passe 4/4
def custom_password_reset_complete(request):
    return render(request, 'password_reset_complete.html')


## page de consultation des différentes demandes en attenete de validation
@login_required(login_url="/")
def controle(request):
    user = request.user

    if user.poste == 'ChefService':
        demandes = DemandePermission.objects.filter(statut='attente_CS', service=user.service)
    elif user.poste == 'DirecteurDepartement':
        demandes = DemandePermission.objects.filter(statut='attente_DS', direction=user.direction)
    elif user.poste == 'ServicePersonnel':
        demandes = DemandePermission.objects.filter(statut='attente_SP')
    elif user.poste == 'DirecteurGeneral':
        demandes = DemandePermission.objects.filter(statut='attente_DG')    
    else:   
        return redirect('applicationidsdemande:erreur')

    total_demandes = demandes.count()

    context = {
        'demandes': demandes,
        'total_demandes': total_demandes,
        'poste': user.poste,
    }
    return render(request, 'controle.html', context)


# remplissage et envoi approprié d'une demande de permission
@login_required(login_url="/")
def demande_permission(request):
    User = get_user_model()
    user = request.user

    if user.poste == 'DirecteurGeneral':
        return redirect('applicationidsdemande:erreur')

    if request.method == 'POST':
        form = PermissionForm(request.POST)
        if form.is_valid():
            demande = form.save(commit=False)

            # Affecter l'initiateur
            demande.initiateur = user
            demande.direction = user.direction

            if user.poste == 'Employe' or user.poste == 'Stagiaire':
                demande.statut = 'attente_CS'  # En attente de validation par le chef de service
                demande.valide_par = None
                destinataires = ['ameviyovo9@gmail.com']
                message = 'M. CS, vous avez une nouvelle demande de permission en attente de validation.'
            elif user.poste == 'ChefService':
                demande.statut = 'attente_DS'  # En attente de validation par le chef de service
                demande.valide_par = user
                destinataires = ['directeurdep@gmail.com']
                message = 'M. DP, vous avez une nouvelle demande de permission en attente de validation.'
            elif user.poste == 'DirecteurDepartement':
                demande.statut = 'attente_SP'  # Envoyer directement au service personnel
                demande.valide_par = user
                destinataires = ['servicepers@gmail.com']
                message = 'M. SP, vous avez une nouvelle demande de permission en attente de validation.'
            elif user.poste == 'Administrateur':
                demande.statut = 'attente_SP'  # Envoyer directement au service personnel
                demande.valide_par = user
                destinataires = ['servicepersonnel@gmail.com']
                message = 'M. SP, vous avez une nouvelle demande de permission en attente de validation.'
            elif user.poste == 'ServicePersonnel':
                demande.statut = 'attente_DG'  # Envoyer directement au directeur général
                demande.valide_par = user
                destinataires = ['directeurgeneral@gmail.com']
                message = 'M. DG, vous avez une nouvelle demande de permission en attente de validation.'
            else:
                demande.statut = 'attente_SP'  # En attente de validation par le service personnel
                demande.valide_par = None
                destinataires = ['ameviyovo9@gmail.com']
                message = 'M. SP, vous avez une nouvelle demande de permission en attente de validation.'

            demande.save()

            # Envoyer le formulaire par e-mail
            sujet = 'NOUVELLE DEMANDE DE PERMISSION'
            send_mail(sujet, message, None, destinataires)

            messages.success(request, 'Votre demande de permission a été soumise avec succès. Vous recevrez un message d\'accord de permission ou de rejet selon les cas.')
            return redirect('applicationidsdemande:demande_permission')
        else:
            # Le formulaire est invalide, nous devons gérer les erreurs
            context = {'form': form, 'user': user}
            return render(request, 'demande_permission.html', context)
    else:
        # Récupérer les valeurs existantes pour préremplir les champs
        initial_values = {
            'NomComplet': f'{user.nom} {user.prenom}',
            'poste': user.poste,
            'service': user.service,
            'direction': user.direction,
        }
        form = PermissionForm(initial=initial_values)

    context = {'form': form, 'user': user}
    return render(request, 'demande_permission.html', context)

# vérification de la demande si bon ou pas (valider, rejeter, corriger)
@login_required(login_url="/")
def valider_demande(request, demande_id):

    demande = get_object_or_404(DemandePermission, id=demande_id)
    user = request.user

    if user.poste == 'ChefService' and (demande.statut == 'attente_CS' or demande.statut == 'a_corriger'):
        if request.method == 'POST':
            form = PermissionForm(request.POST, instance=demande)
            if form.is_valid():
                demande = form.save(commit=False)
                
                if 'valider' in request.POST:
                    # Effectuer la validation de la demande ici
                    demande.statut = 'attente_DS'
                    demande.valide_par = user
                    demande.raison_rejet = ''
                    demande.validateurs.add(user)  # Ajouter le validateur à la liste des validateurs de la demande
                    demande.save()

                    # Envoyer une notification par e-mail au directeur de département
                    sujet = 'NOUVELLE DEMANDE DE PERMISSION'
                    message = 'Monsieur Directeur de Département, vous avez une nouvelle demande de permission en attente de validation. Chap Chap DP'
                    destinataires = ['directeurdep@gmail.com']
                    send_mail(sujet, message, None, destinataires)
                    # ...

                elif 'rejeter' in request.POST:
                    # Marquer la demande comme "rejetee"
                    demande.statut = 'rejetee'
                    demande.valide_par = user
                    demande.rejeteurs_strict.add(user)  # Ajouter le validateur à la liste des validateurs de la demande
                    demande.save()

                    # Envoyer une notification par e-mail à l'employé
                    sujet = 'REJET DE DEMANDE DE PERMISSION'
                    message = "Monsieur l'employé, votre demande de permission a été rejetée."
                    destinataires = ['employe@gmail.com']
                    send_mail(sujet, message, None, destinataires)
                    # ...
                elif 'a_corriger' in request.POST:
                    # Marquer la demande comme "à corriger"
                    demande.statut = 'a_corriger'
                    demande.valide_par = user
                    demande.rejeteurs_pour_correction.add(user)  # Ajouter le validateur à la liste des validateurs de la demande
                    demande.save()

                    # Envoyer une notification par e-mail à l'employé
                    sujet = 'REJET POUR CORRECTION DE DEMANDE DE PERMISSION'
                    message = "Monsieur l'employé, votre demande de permission a été rejetée pour correction."
                    destinataires = ['employe@gmail.com']
                    send_mail(sujet, message, None, destinataires)
                    # ...

                return redirect('applicationidsdemande:controle')
        else:
            form = PermissionForm(instance=demande)

        context = {'form': form}
        return render(request, 'valider_demande.html', context)

    elif user.poste == 'DirecteurDepartement' and (demande.statut == 'attente_DP' or demande.statut == 'a_corriger'):
        if request.method == 'POST':
            form = PermissionForm(request.POST, instance=demande)
            if form.is_valid():
                demande = form.save(commit=False)

                if 'valider' in request.POST:
                    # Effectuer la validation de la demande ici
                    demande.statut = 'attente_SP'
                    demande.valide_par = user
                    demande.raison_rejet = ''
                    demande.validateurs.add(user)  # Ajouter le validateur à la liste des validateurs de la demande
                    demande.save()

                    # Envoyer une notification par e-mail au service personnel
                    sujet = 'NOUVELLE DEMANDE DE PERMISSION'
                    message = 'Service Personnel, vous avez une nouvelle demande de permission en attente de validation. Chap Chap SP'
                    destinataires = ['servicepersonnel@gmail.com']
                    send_mail(sujet, message, None, destinataires)
                    # ...

                elif 'rejeter' in request.POST:
                    # Marquer la demande comme "rejetee"
                    demande.statut = 'rejetee'
                    demande.valide_par = user
                    demande.rejeteurs_strict.add(user)  # Ajouter le validateur à la liste des validateurs de la demande
                    demande.save()

                    # Envoyer une notification par e-mail à l'employé
                    sujet = 'REJET DE DEMANDE DE PERMISSION'
                    message = "Monsieur l'employé, votre demande de permission a été rejetée."
                    destinataires = ['employe@gmail.com']
                    send_mail(sujet, message, None, destinataires)
                    # ...
                elif 'a_corriger' in request.POST:
                    # Marquer la demande comme "à corriger"
                    demande.statut = 'a_corriger'
                    demande.valide_par = user
                    demande.rejeteurs_pour_correction.add(user)  # Ajouter le validateur à la liste des validateurs de la demande
                    demande.save()

                    # Envoyer une notification par e-mail à l'employé
                    sujet = 'REJET POUR CORRECTION DE DEMANDE DE PERMISSION'
                    message = "Monsieur l'employé, votre demande de permission a été rejetée pour correction."
                    destinataires = ['employe@gmail.com']
                    send_mail(sujet, message, None, destinataires)
                    # ...

                return redirect('applicationidsdemande:controle')
        else:
            form = PermissionForm(instance=demande)

        context = {'form': form}
        return render(request, 'valider_demande.html', context)

    elif user.poste == 'ServicePersonnel' and (demande.statut == 'attente_SP' or demande.statut == 'a_corriger'):
        if request.method == 'POST':
            form = PermissionForm(request.POST, instance=demande)
            if form.is_valid():
                demande = form.save(commit=False)

                if 'valider' in request.POST:
                    # Effectuer la validation de la demande ici
                    demande.statut = 'attente_DG'
                    demande.valide_par = user
                    demande.raison_rejet = ''
                    demande.validateurs.add(user)  # Ajouter le validateur à la liste des validateurs de la demande
                    demande.save()

                    # Envoyer une notification par e-mail au directeur général
                    sujet = 'NOUVELLE DEMANDE DE PERMISSION'
                    message = 'Monsieur le Directeur Général, vous avez une nouvelle demande de permission en attente de validation. Chap Chap DG'
                    destinataires = ['directeurgeneral@gmail.com']
                    send_mail(sujet, message, None, destinataires)
                    # ...

                elif 'rejeter' in request.POST:
                    # Marquer la demande comme "rejetee"
                    demande.statut = 'rejetee'
                    demande.valide_par = user
                    demande.rejeteurs_strict.add(user)  # Ajouter le validateur à la liste des validateurs de la demande
                    demande.save()

                    # Envoyer une notification par e-mail à l'employé
                    sujet = 'REJET DE DEMANDE DE PERMISSION'
                    message = "Monsieur l'employé, votre demande de permission a été rejetée."
                    destinataires = ['employe@gmail.com']
                    send_mail(sujet, message, None, destinataires)
                    # ...
                elif 'a_corriger' in request.POST:
                    # Marquer la demande comme "à corriger"
                    demande.statut = 'a_corriger'
                    demande.valide_par = user
                    demande.rejeteurs_pour_correction.add(user)  # Ajouter le validateur à la liste des validateurs de la demande
                    demande.save()

                    # Envoyer une notification par e-mail à l'employé
                    sujet = 'REJET POUR CORRECTION DE DEMANDE DE PERMISSION'
                    message = "Monsieur l'employé, votre demande de permission a été rejetée pour correction."
                    destinataires = ['employe@gmail.com']
                    send_mail(sujet, message, None, destinataires)
                    # ...

                return redirect('applicationidsdemande:controle')
        else:
            form = PermissionForm(instance=demande)

        context = {'form': form}
        return render(request, 'valider_demande.html', context)

    elif user.poste == 'DirecteurGeneral' and (demande.statut == 'attente_DG' or demande.statut == 'a_corriger'):
        if request.method == 'POST':
            form = PermissionForm(request.POST, instance=demande)
            if form.is_valid():
                demande = form.save(commit=False)
                if 'valider' in request.POST:
                    # Effectuer la validation de la demande
                    demande.statut = 'validee'
                    demande.valide_par = user
                    demande.raison_rejet = ''
                    demande.validateurs.add(user)  # Ajouter le validateur à la liste des validateurs de la demande
                    demande.save()

                    # Envoyer une notification par e-mail à l'employé
                    sujet = 'VALIDATION DE DEMANDE DE PERMISSION'
                    message = "Monsieur l'employé, votre demande de permission a été validée. Bon Congé !"
                    destinataires = ['employe@gmail.com']
                    send_mail(sujet, message, None, destinataires)
                    # ...

                elif 'rejeter' in request.POST:
                    # Marquer la demande comme "rejetee"
                    demande.statut = 'rejetee'
                    demande.valide_par = user
                    demande.rejeteurs_strict.add(user)  # Ajouter le validateur à la liste des validateurs de la demande
                    demande.save()

                    # Envoyer une notification par e-mail à l'employé
                    sujet = 'REJET DE DEMANDE DE PERMISSION'
                    message = "Monsieur l'employé, votre demande de permission a été rejetée."
                    destinataires = ['employe@gmail.com']
                    send_mail(sujet, message, None, destinataires)
                    # ...
                elif 'a_corriger' in request.POST:
                    # Marquer la demande comme "à corriger"
                    demande.statut = 'a_corriger'
                    demande.valide_par = user
                    demande.rejeteurs_pour_correction.add(user)  # Ajouter le validateur à la liste des validateurs de la demande
                    demande.save()

                    # Envoyer une notification par e-mail à l'employé
                    sujet = 'REJET POUR CORRECTION DE DEMANDE DE PERMISSION'
                    message = "Monsieur l'employé, votre demande de permission a été rejetée pour correction."
                    destinataires = ['employe@gmail.com']
                    send_mail(sujet, message, None, destinataires)
                    # ...

                return redirect('applicationidsdemande:controle')
        else:
            form = PermissionForm(instance=demande)

        context = {'form': form}
        return render(request, 'valider_demande.html', context)

    else:
        # Rediriger les utilisateurs autres que le chef de service, le directeur de département, le service personnel et le directeur général vers une page d'erreur ou de permission refusée
        return redirect('applicationidsdemande:erreur')


# filtre des demandes rejetées pour un utilisateur
@login_required(login_url="/")
def demandes_rejetees_initiateur(request):

    user = request.user

    if user.poste != 'DirecteurGeneral':
        # Filtrer les demandes rejetées pour l'employé actuel
        demandes_rejetees = DemandePermission.objects.filter(initiateur=user, statut='rejetee')

        # Passer les demandes filtrées au template pour affichage
        total_demandes_rejetees = demandes_rejetees.count()
        context = {'demandes_rejetees': demandes_rejetees, 'total_demandes_rejetees': total_demandes_rejetees}
        return render(request, 'demandes_rejetees_initiateur.html', context)
    else:
        return redirect('applicationidsdemande:erreur')


# filtre des demandes validées pour un utilisateur
@login_required(login_url="/")
def demandes_validees_initiateur(request):

    user = request.user

    if user.poste != 'DirecteurGeneral':
        # Filtrer les demandes validées pour l'employé actuel
        demandes_validees = DemandePermission.objects.filter(initiateur=user, statut='validee')

        # Passer les demandes filtrées au template pour affichage
        total_demandes_validees = demandes_validees.count()
        context = {'demandes_validees': demandes_validees, 'total_demandes_validees': total_demandes_validees}
        return render(request, 'demandes_validees_initiateur.html', context)
    else:
        return redirect('applicationidsdemande:erreur')


# filtre des demandes validées par un validateur (pour au moins une fois)
@login_required(login_url="/")
def demandes_validees_validateur(request):
    POSTE_VALIDATEUR = ['ChefService', 'DirecteurDepartement', 'ServicePersonnel', 'DirecteurGenenral']
    user = request.user
    if user.poste in POSTE_VALIDATEUR:

        # Filtrer les demandes en vérifiant si l'utilisateur actuel est présent dans le champ "validateurs"
        demandes_validees = DemandePermission.objects.filter(validateurs=user)

        # Passer les demandes filtrées au template pour affichage
        total_demandes_validees = demandes_validees.count()
        context = {'demandes_validees': demandes_validees, 'total_demandes_validees': total_demandes_validees}
        return render(request, 'demandes_validees_validateur.html', context)
    else:
        return redirect('applicationidsdemande:erreur')
    
    
# filtre des demandes strictement rejetées par un validateur
@login_required(login_url="/")
def demandes_strictement_rejetees_validateur(request):
    POSTE_VALIDATEUR = ['ChefService', 'DirecteurDepartement', 'ServicePersonnel', 'DirecteurGenenral']
    user = request.user
    if user.poste in POSTE_VALIDATEUR:

        # Filtrer les demandes en vérifiant si l'utilisateur actuel est présent dans le champ "rejeteur_strict"
        demandes_strictement_rejetees_validateur = DemandePermission.objects.filter(rejeteurs_strict=user)

        # Passer les demandes filtrées au template pour affichage
        total_demandes_strictement_rejetees_validateur = demandes_strictement_rejetees_validateur.count()
        context = {'demandes_strictement_rejetees_validateur': demandes_strictement_rejetees_validateur, 'total_demandes_strictement_rejetees_validateur': total_demandes_strictement_rejetees_validateur}
        return render(request, 'demandes_strictement_rejetees_validateur.html', context)
    else:
        return redirect('applicationidsdemande:erreur')

# filtre des demandes rejetées pour correction par un validateur
@login_required(login_url="/")
def demandes_rejetees_acorriger_validateur(request):
    POSTE_VALIDATEUR = ['ChefService', 'DirecteurDepartement', 'ServicePersonnel', 'DirecteurGenenral']
    user = request.user
    if user.poste in POSTE_VALIDATEUR:

        # Filtrer les demandes en vérifiant si l'utilisateur actuel est présent dans le champ "rejeteur_pour_correction"
        demandes_rejetees_acorriger_validateur = DemandePermission.objects.filter(rejeteurs_pour_correction=user)

        # Passer les demandes filtrées au template pour affichage
        total_demandes_rejetees_acorriger_validateur = demandes_rejetees_acorriger_validateur.count()
        context = {'demandes_rejetees_acorriger_validateur': demandes_rejetees_acorriger_validateur, 'total_demandes_rejetees_acorriger_validateur': total_demandes_rejetees_acorriger_validateur}
        return render(request, 'demandes_rejetees_acorriger_validateur.html', context)
    else:
        return redirect('applicationidsdemande:erreur')

# filtre des demandes en cours pour un utilisateur
@login_required(login_url="/")
def demandes_encours_initiateur(request):

    user = request.user

    if user.poste != 'DirecteurGeneral':
        # Filtrer les demandes rejetées pour l'employé actuel
        demandes_encours = DemandePermission.objects.filter(initiateur=user).exclude(statut__in=['rejetee', 'validee', 'a_corriger'])

        # Passer les demandes filtrées au template pour affichage
        total_demandes_encours = demandes_encours.count()
        context = {'demandes_encours': demandes_encours, 'total_demandes_encours': total_demandes_encours}
        return render(request, 'demandes_encours_initiateur.html', context)
    else:
        return redirect('applicationidsdemande:erreur')
    

# filtre des demandes à corriger par un utilsateur
@login_required(login_url="/")
def demandes_a_corriger_initiateur(request):
    
    user = request.user

    if user.poste != 'DirecteurGeneral':
        # Filtrer les demandes rejetées pour l'employé actuel
        demandes_a_corriger = DemandePermission.objects.filter(initiateur=user, statut='a_corriger')

        # Passer les demandes filtrées au template pour affichage
        total_demandes_a_corriger = demandes_a_corriger.count()
        context = {'demandes_a_corriger': demandes_a_corriger, 'total_demandes_a_corriger': total_demandes_a_corriger}
        return render(request, 'demandes_a_corriger_initiateur.html', context)
    else:
        return redirect('applicationidsdemande:erreur')


#correction d'une demande et reinsertion dans le circuit
@login_required(login_url="/")
def corriger_demande_initiateur(request, demande_id):

    demande = get_object_or_404(DemandePermission, id=demande_id)
    user = request.user

    if demande.statut == 'a_corriger' and demande.initiateur == user:
        if request.method == 'POST':
            form = PermissionForm(request.POST, instance=demande)
            if form.is_valid():
                demande = form.save(commit=False)

                if user.poste == 'Employe' or user.poste == 'Stagiaire':
                    demande.statut = 'attente_CS'  # Réinsérer la demande dans le circuit

                    # Réinitialiser les champs de validation
                    demande.valide_par = None
                    demande.raison_rejet = ''
                    demande.date_emission = timezone.now()

                    # Envoyer la demande au chef de service
                    destinataires = ['ameviyovo9@gmail.com']
                    message = 'M. CS, vous avez une demande de permission corrigée en attente de validation.'

                    demande.save()

                    # Envoyer le formulaire par e-mail
                    sujet = 'DEMANDE DE PERMISSION CORRIGÉE'
                    send_mail(sujet, message, None, destinataires)

                    #messages.success(request, 'Votre demande de permission corrigée a été soumise avec succès.')
                elif user.poste == 'ChefService':
                    demande.statut = 'attente_DS'  # Réinsérer la demande dans le circuit

                    # Réinitialiser les champs de validation
                    demande.valide_par = user
                    demande.raison_rejet = ''
                    demande.date_emission = timezone.now()

                    # Envoyer la demande au chef de service
                    destinataires = ['ameviyovo9@gmail.com']
                    message = 'M. DP, vous avez une demande de permission corrigée en attente de validation.'

                    demande.save()

                    # Envoyer le formulaire par e-mail
                    sujet = 'DEMANDE DE PERMISSION CORRIGÉE'
                    send_mail(sujet, message, None, destinataires)
                    # ...

                    #messages.success(request, 'Votre demande de permission corrigée a été soumise avec succès.')
                elif user.poste == 'DirecteurDepartement':
                    demande.statut = 'attente_SP'  # Réinsérer la demande dans le circuit

                    # Réinitialiser les champs de validation
                    demande.valide_par = user
                    demande.raison_rejet = ''
                    demande.date_emission = timezone.now()

                    # Envoyer la demande au chef de service
                    destinataires = ['ameviyovo9@gmail.com']
                    message = 'M. SP, vous avez une demande de permission corrigée en attente de validation.'

                    demande.save()

                    # Envoyer le formulaire par e-mail
                    sujet = 'DEMANDE DE PERMISSION CORRIGÉE'
                    send_mail(sujet, message, None, destinataires)
                    # ...

                    #messages.success(request, 'Votre demande de permission corrigée a été soumise avec succès.')
                elif user.poste == 'Administrateur':
                    demande.statut = 'attente_SP'  # Réinsérer la demande dans le circuit

                    # Réinitialiser les champs de validation
                    demande.valide_par = user
                    demande.raison_rejet = ''
                    demande.date_emission = timezone.now()

                    # Envoyer la demande au chef de service
                    destinataires = ['ameviyovo9@gmail.com']
                    message = 'M. SP, vous avez une demande de permission corrigée en attente de validation.'

                    demande.save()

                    # Envoyer le formulaire par e-mail
                    sujet = 'DEMANDE DE PERMISSION CORRIGÉE'
                    send_mail(sujet, message, None, destinataires)
                    # ...

                    #messages.success(request, 'Votre demande de permission corrigée a été soumise avec succès.')
                elif user.poste == 'ServicePersonnel':
                    demande.statut = 'attente_DG'  # Réinsérer la demande dans le circuit

                    # Réinitialiser les champs de validation
                    demande.valide_par = user
                    demande.raison_rejet = ''
                    demande.date_emission = timezone.now()

                    # Envoyer la demande au chef de service
                    destinataires = ['ameviyovo9@gmail.com']
                    message = 'M. DG, vous avez une demande de permission corrigée en attente de validation.'

                    demande.save()

                    # Envoyer le formulaire par e-mail
                    sujet = 'DEMANDE DE PERMISSION CORRIGÉE'
                    send_mail(sujet, message, None, destinataires)
                    # ...

                    #messages.success(request, 'Votre demande de permission corrigée a été soumise avec succès.')
                return redirect('applicationidsdemande:demandes_a_corriger_initiateur')
        else:
            form = PermissionForm(instance=demande)

        context = {'form': form}
        return render(request, 'corriger_demande_initiateur.html', context)
    else:
        return redirect('applicationidsdemande:erreur')
    
#envoi des notifications
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user)
    context = {
        'notifications': notifications
    }

    # Marquer les notifications comme lues
    for notification in notifications:
        if not notification.is_read:
            notification.is_read = True
            notification.save()

    return render(request, 'notifications.html', context)


#page d'erreur de permission ou de redirection
def erreur(request):
    return render(request, 'erreur.html')

#page d'erreur 404 personnalisée
def handler404(request, exception):
    return render(request, '404.html', status=404)