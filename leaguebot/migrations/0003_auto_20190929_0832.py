# Generated by Django 2.2.4 on 2019-09-29 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaguebot', '0002_auto_20190928_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flexmatch',
            name='adc',
            field=models.CharField(default='0', max_length=200),
        ),
        migrations.AlterField(
            model_name='flexmatch',
            name='jun',
            field=models.CharField(default='0', max_length=200),
        ),
        migrations.AlterField(
            model_name='flexmatch',
            name='mid',
            field=models.CharField(default='0', max_length=200),
        ),
        migrations.AlterField(
            model_name='flexmatch',
            name='sup',
            field=models.CharField(default='0', max_length=200),
        ),
        migrations.AlterField(
            model_name='flexmatch',
            name='top',
            field=models.CharField(default='0', max_length=200),
        ),
        migrations.AlterField(
            model_name='solomatch',
            name='adc',
            field=models.CharField(default='0', max_length=200),
        ),
        migrations.AlterField(
            model_name='solomatch',
            name='jun',
            field=models.CharField(default='0', max_length=200),
        ),
        migrations.AlterField(
            model_name='solomatch',
            name='mid',
            field=models.CharField(default='0', max_length=200),
        ),
        migrations.AlterField(
            model_name='solomatch',
            name='sup',
            field=models.CharField(default='0', max_length=200),
        ),
        migrations.AlterField(
            model_name='solomatch',
            name='top',
            field=models.CharField(default='0', max_length=200),
        ),
    ]
