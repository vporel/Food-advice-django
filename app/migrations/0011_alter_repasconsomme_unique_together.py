# Generated by Django 4.0.4 on 2022-06-08 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_contributeur_datenaissance_contributeur_sexe_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='repasconsomme',
            unique_together={('date', 'momentJournee', 'repas', 'contributeur')},
        ),
    ]