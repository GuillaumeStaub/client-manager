# Generated by Django 3.1.2 on 2020-10-08 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0002_auto_20201004_1733'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='saison',
            options={'verbose_name': 'Saison', 'verbose_name_plural': 'Saisons'},
        ),
        migrations.AlterField(
            model_name='commande',
            name='infos_techniques',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='general.infostechniques', verbose_name='Informations techniques'),
        ),
        migrations.AlterField(
            model_name='commande',
            name='nb_jours',
            field=models.IntegerField(default=16, verbose_name='Nombre de jours'),
        ),
    ]
