# Generated by Django 4.2.1 on 2025-05-25 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commodities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('metal_type', models.CharField(choices=[('gold', 'Gold'), ('silver', 'Silver')], max_length=10)),
                ('close', models.FloatField()),
                ('open', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('volume', models.FloatField()),
            ],
        ),
    ]
