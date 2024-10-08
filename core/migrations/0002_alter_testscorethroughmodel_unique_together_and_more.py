# Generated by Django 5.1 on 2024-08-23 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='testscorethroughmodel',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='behaviorchallenges',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='child',
            name='age',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='child',
            name='gender',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='child',
            name='gpa',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
        migrations.AlterField(
            model_name='child',
            name='grade',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='child',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='child',
            name='learning_style',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='child',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='hobbies',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='standardtestscore',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='testscorethroughmodel',
            name='score',
            field=models.IntegerField(),
        ),
    ]
