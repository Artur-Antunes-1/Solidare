# Generated by Django 5.1.7 on 2025-06-03 16:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Aplicativo', '0008_apadrinhado_apadrinhado_por'),
    ]

    operations = [
        migrations.CreateModel(
            name='Desempenho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.CharField(max_length=20)),
                ('nota', models.DecimalField(decimal_places=2, max_digits=4)),
                ('frequencia', models.DecimalField(decimal_places=2, max_digits=5)),
                ('comentario_professor', models.TextField(blank=True)),
                ('apadrinhado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Aplicativo.apadrinhado')),
            ],
        ),
    ]
