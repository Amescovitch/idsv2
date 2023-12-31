# Generated by Django 4.1.5 on 2023-07-18 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicationidsdemande', '0029_demandepermission_direction_personnel_direction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnel',
            name='direction',
            field=models.CharField(choices=[('', ''), ('DirectionTechnique', 'Direction Technique'), ('DirectionCommercialeMarketingCommunication', 'Direction Commerciale, Marketing et Communication'), ('DirectionAdministrativeRessourcesHumaines', 'Direction Administrative et des Ressources Humaines')], default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='service',
            field=models.CharField(choices=[('', ''), ('ServiceReseauxClients', 'Service Reseaux et Clients'), ('ServiceSupportAlvanet', 'Service Support ALAVANET'), ('ServiceLogicielFormation', 'Service Logiciel et Formation'), ('ServiceCommercial', 'Service Commercial'), ('ServiceAdministratifRessourcesHumaines', 'Service Administratif et des Ressources Humaines'), ('EquipeLogistiqueCommerciale', 'Equipe Logistique et Commerciale'), ('Direction', 'Direction'), ('Administration', 'Administration')], max_length=255),
        ),
    ]
