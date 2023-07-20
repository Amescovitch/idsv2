from applicationidsdemande.views import *
from . import views as custom_auth_views
from django.urls import path



app_name = 'applicationidsdemande'

urlpatterns = [
    #connexion, page d'accueil
    path('', login_view, name="index"),

    #notification
    path('notification/', notifications, name="notifications"),

    #page d'erreur
    path('err/', erreur, name='erreur'),

    #tableaux de bord
    path('accueil_admin/', accueil_admin, name="accueil_admin"),
    path('accueil_validateur/', accueil_validateur, name="accueil_validateur"),
    path('accueil_personnel/', accueil_personnel, name="accueil_personnel"),

    #page d'inscription des utilisateurs
    path('ins/', inscription, name="inscription"),

    #page de consultation de différentes demandes en attente de validation
    path('con/', controle, name="controle"),
    
    #pages de demande de permission à l'initiation
    path('dp/', demande_permission, name="demande_permission"),

    #pages pour vérifier la validité d'une demande (le validateur )
    path('vd/<int:demande_id>/', valider_demande, name='valider_demande'),

    #pages où l'initiatiateur peut vérifier ses demandes qui sont rejetées
    path('dr/', demandes_rejetees_initiateur, name='demandes_rejetees_initiateur'),

    #pages où l'initiatiateur peut vérifier ses demandes qui sont en cours de validation
    path('dec/', demandes_encours_initiateur, name='demandes_encours_initiateur'),

    #pages où l'initiatiateur peut vérifier ses demandes qui sont déjà validées
    path('dvi/', demandes_validees_initiateur, name='demandes_validees_initiateur'),

    #pages où le validateur peut voir les demandes qu'il a déjà validées
    path('dvv/', demandes_validees_validateur, name='demandes_validees_validateur'),

    #pages où l'initiatiateur peut voir la liste de ses demandes qui sont rejetées pour correction
    path('dac/', demandes_a_corriger_initiateur, name='demandes_a_corriger_initiateur'),

    #pages où le validateur peut voir les demandes qu'il a strictement rejetées
    path('dsrv/', demandes_strictement_rejetees_validateur, name='demandes_strictement_rejetees_validateur'),

    #pages où le validateur peut voir les demandes qu'il a rejetées pour correction
    path('dracv/', demandes_rejetees_acorriger_validateur, name='demandes_rejetees_acorriger_validateur'),    

    #pages où l'initiatiateur peut corriger ses demandes qui sont rejetées pour correction
    path('cdi/<int:demande_id>/', corriger_demande_initiateur, name='corriger_demande_initiateur'),

    
    #réinitialisation de mot de passe
    path('password_reset/', custom_auth_views.custom_password_reset, name='password_reset'),
    path('password_reset/done/', custom_auth_views.custom_password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', custom_auth_views.custom_password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', custom_auth_views.custom_password_reset_complete, name='password_reset_complete'),
]
