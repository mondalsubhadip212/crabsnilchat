# Generated by Django 3.2 on 2021-06-01 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crabsnil_chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userid',
            field=models.CharField(default='ZZ5DNOV', max_length=7),
        ),
    ]
