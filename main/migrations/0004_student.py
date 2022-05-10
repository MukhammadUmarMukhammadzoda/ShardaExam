# Generated by Django 4.0.3 on 2022-04-10 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_specialization_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('unique_id', models.CharField(blank=True, max_length=100, null=True)),
                ('sgpa1', models.FloatField()),
                ('sgpa2', models.FloatField()),
                ('cgpa', models.FloatField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.group')),
                ('specializetion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.specialization')),
                ('subject', models.ManyToManyField(to='main.subject')),
            ],
        ),
    ]
