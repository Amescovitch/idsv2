STATUT_CHOICES = (
    ('attente_CS', 'En attente du Chef Service'),
    ('attente_DS', 'En attente du Directeur Service'),
    ('attente_SP', 'En attente du Service Personnel'),
    ('attente_DG', 'En attente du Directeur Général'),
    ('validee', 'Demande validée'),
    ('rejetee', 'Demande rejetée'),
    ('a_corriger', 'Demande à corriger'),
)

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