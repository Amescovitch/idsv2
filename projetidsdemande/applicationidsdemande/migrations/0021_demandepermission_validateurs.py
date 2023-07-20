# Generated by Django 4.1.5 on 2023-07-13 16:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applicationidsdemande', '0020_alter_personnel_poste_alter_personnel_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='demandepermission',
            name='validateurs',
            field=models.ManyToManyField(related_name='validateurs_demandes', to=settings.AUTH_USER_MODEL),
        ),
    ]