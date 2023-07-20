from .models import DemandePermission
from django.contrib import admin
from .models import *


class PersonnelAdmin(admin.ModelAdmin):
    model = Personnel
    # Définir les champs affichés dans la liste des utilisateurs dans l'interface d'administration
    list_display = ('username', 'email', 'nom', 'prenom', 'poste', 'service', 'direction', 'telephone', 'is_staff')
    # Définir les champs utilisés pour la recherche des utilisateurs dans l'interface d'administration
    search_fields = ('username', 'direction', 'service', 'poste')

admin.site.register(Personnel, PersonnelAdmin)



class DemandePermissionAdmin(admin.ModelAdmin):
    list_display = ('date_emission', 'initiateur', 'NomComplet', 'poste', 'service', 'direction', 'motif', 'lieu', 'date_heure_sortie', 'date_heure_retour', 'statut', 'valide_par')
    #list_filter = ('statut', 'service', 'poste')
    search_fields = ('NomComplet', 'valide_par', 'initiateur')
    date_hierarchy = 'date_emission'
    readonly_fields = ('date_emission',)

admin.site.register(DemandePermission, DemandePermissionAdmin)


""" class DemandePermissionAdmin(admin.ModelAdmin):
    list_display = ('date_emission', 'initiateur', 'NomComplet', 'poste', 'service', 'motif', 'lieu', 'date_heure_sortie', 'date_heure_retour', 'statut', 'valide_par', 'validateurs_list', 'rejeteurs_pour_correction_list', 'rejeteurs_strict_list')
    search_fields = ('NomComplet', 'valide_par', 'initiateur')
    date_hierarchy = 'date_emission'
    readonly_fields = ('date_emission',)

    def validateurs_list(self, obj):
        return ", ".join(str(validateur) for validateur in obj.validateurs.all())

    validateurs_list.short_description = 'Validateurs'

    def rejeteurs_strict_list(self, obj):
        return ", ".join(str(rejeteur_strict) for rejeteur_strict in obj.rejeteurs_strict.all())

    rejeteurs_strict_list.short_description = 'Rejeteurs Strict'

    def rejeteurs_pour_correction_list(self, obj):
        return ", ".join(str(rejeteur_pour_correction) for rejeteur_pour_correction in obj.rejeteurs_pour_correction.all())

    rejeteurs_pour_correction_list.short_description = 'Rejeteur Pour Correction'

admin.site.register(DemandePermission, DemandePermissionAdmin) """


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    
admin.site.register(Notification, NotificationAdmin)