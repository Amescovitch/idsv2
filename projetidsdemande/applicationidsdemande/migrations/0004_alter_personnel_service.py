# Generated by Django 4.1.5 on 2023-06-24 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicationidsdemande', '0003_demandepermission_validee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnel',
            name='service',
            field=models.CharField(choices=[('com', 'Commerciale'), ('cli', 'Clientèle'), ('dg', 'Direction'), ('ad', 'Administrateur')], max_length=255),
        ),
    ]