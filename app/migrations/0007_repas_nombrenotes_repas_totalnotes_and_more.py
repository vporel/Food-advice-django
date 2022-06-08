# Generated by Django 4.0.4 on 2022-06-07 12:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_conversation_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='repas',
            name='nombreNotes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='repas',
            name='totalNotes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='nombreNotes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='totalNotes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='aliment',
            name='detailApports',
            field=models.TextField(blank=True, help_text="Vertus de l'aliment", null=True, verbose_name='Détail des apports'),
        ),
        migrations.AlterField(
            model_name='aliment',
            name='detailRisques',
            field=models.TextField(blank=True, help_text='Problèmes liés à une consommation non suivie', null=True, verbose_name='Détail des risques'),
        ),
        migrations.AlterField(
            model_name='aliment',
            name='masseUnite',
            field=models.FloatField(help_text="La masse en grammes d'un élément (ex: 120 pour la banage)", verbose_name='Masse unité (g)'),
        ),
        migrations.AlterField(
            model_name='aliment',
            name='mineraux',
            field=models.CharField(blank=True, help_text='Motif : mineral1, minearl2, ...', max_length=255, null=True, verbose_name='Mineraux'),
        ),
        migrations.AlterField(
            model_name='aliment',
            name='tauxGlucides',
            field=models.FloatField(default=0, help_text='Taux de glucides dans 100g', verbose_name='Taux de glucides'),
        ),
        migrations.AlterField(
            model_name='aliment',
            name='tauxLipides',
            field=models.FloatField(default=0, help_text='Taux de lipides dans 100g', verbose_name='Taux de lipides'),
        ),
        migrations.AlterField(
            model_name='aliment',
            name='tauxProteines',
            field=models.FloatField(default=0, help_text='Taux de proteines dans 100g', verbose_name='Taux de proteines'),
        ),
        migrations.AlterField(
            model_name='aliment',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.typealiment', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='aliment',
            name='uniteComptage',
            field=models.CharField(blank=True, help_text="Comment on compte l'aliment (ex:doigt pour une banane)", max_length=30, null=True, verbose_name='Unité de comptage'),
        ),
        migrations.AlterField(
            model_name='aliment',
            name='vitamines',
            field=models.CharField(blank=True, help_text='Motif : vitamine1, vitamine2, ...', max_length=255, null=True, verbose_name='Vitamines'),
        ),
    ]
