# Generated by Django 4.1.5 on 2023-07-20 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicationidsdemande', '0034_alter_demandepermission_rejeteurs_pour_correction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demandepermission',
            name='statut',
            field=models.CharField(choices=[('attente_CS', 'En attente du Chef Service'), ('attente_DS', 'En attente du Directeur Service'), ('attente_SP', 'En attente du Service Personnel'), ('attente_DG', 'En attente du Directeur Général'), ('validee', 'Demande validée'), ('rejetee', 'Demande rejetée'), ('a_corriger', 'Demande à corriger')], max_length=50),
        ),
    ]
