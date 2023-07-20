# Generated by Django 4.1.5 on 2023-07-08 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicationidsdemande', '0017_remove_demandepermission_datesortie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnel',
            name='poste',
            field=models.CharField(choices=[('dg', 'Directeur Général'), ('dp', 'Directeur de Département'), ('sp', 'Service Personnel'), ('ad', 'Administrateur'), ('cs', 'Chef Service'), ('em', 'Employé')], default='Employé', max_length=255),
        ),
    ]