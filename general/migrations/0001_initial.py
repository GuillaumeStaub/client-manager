# Generated by Django 3.1.1 on 2020-09-16 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InfosTechniques',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricule_compteur', models.CharField(blank=True, max_length=3, null=True)),
                ('num_armoire', models.CharField(max_length=5)),
                ('emplacement', models.CharField(default=0, max_length=2)),
            ],
            options={
                'verbose_name': 'Informations Techniques',
                'verbose_name_plural': 'Informations Techniques',
                'unique_together': {('num_armoire', 'emplacement')},
            },
        ),
    ]