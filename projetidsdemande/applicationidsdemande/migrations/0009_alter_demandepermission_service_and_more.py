# Generated by Django 4.2.2 on 2023-06-26 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicationidsdemande', '0008_demandepermission_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demandepermission',
            name='service',
            field=models.CharField(choices=[('com', 'Commerciale'), ('cli', 'Clientèle'), ('dg', 'Direction'), ('ad', 'Administration')], max_length=255),
        ),
        migrations.AlterField(
            model_name='demandepermission',
            name='statut',
            field=models.CharField(choices=[('attente_chef', 'En av par le CS'), ('attente_directeur', 'En av par le DG'), ('validee', 'Demande validée')], default='attente_chef', max_length=100),
        ),
    ]