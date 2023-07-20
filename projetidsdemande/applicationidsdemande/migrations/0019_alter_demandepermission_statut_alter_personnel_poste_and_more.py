# Generated by Django 4.1.5 on 2023-07-10 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicationidsdemande', '0018_alter_personnel_poste'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demandepermission',
            name='statut',
            field=models.CharField(choices=[('attente_CS', 'En attente par le CS'), ('attente_DP', 'En attente par le DP'), ('attente_SP', 'En attente par le SP'), ('attente_DG', 'En attente par le DG'), ('validee', 'Demande validée'), ('rejetee', 'Demande rejetée'), ('a_corriger', 'Demande à corriger')], default='attente_CS', max_length=100),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='poste',
            field=models.CharField(choices=[('Autre', 'Choisir un poste'), ('em', 'Employé'), ('cs', 'Chef Service'), ('ad', 'Administrateur'), ('sp', 'Service Personnel'), ('dg', 'Directeur Général'), ('dp', 'Directeur de Département')], max_length=255),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='service',
            field=models.CharField(choices=[('Autre', 'Choisir un service'), ('com', 'Commerciale'), ('cli', 'Clientèle'), ('dir', 'Direction'), ('ad', 'Administration')], max_length=255),
        ),
    ]