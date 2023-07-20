# Generated by Django 4.2.2 on 2023-06-26 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('applicationidsdemande', '0005_alter_personnel_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demandepermission',
            name='validee',
        ),
        migrations.AddField(
            model_name='demandepermission',
            name='statut',
            field=models.CharField(choices=[('attente_employe', "En attente de validation par l'employé"), ('attente_chef', 'En attente de validation par le chef de service'), ('attente_directeur', 'En attente de validation par le directeur général'), ('validee', 'Demande validée')], default='attente_employe', max_length=20),
        ),
        migrations.AddField(
            model_name='demandepermission',
            name='valide_par',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]