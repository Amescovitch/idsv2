# Generated by Django 4.1.5 on 2023-07-14 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicationidsdemande', '0022_demandepermission_rejeteurs_pour_correction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demandepermission',
            name='date_heure_retour',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='demandepermission',
            name='date_heure_sortie',
            field=models.DateTimeField(),
        ),
    ]
