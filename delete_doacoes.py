# delete_doacoes.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seu_projeto.settings')
django.setup()

from Aplicativo.models import Doacao
Doacao.objects.all().delete()
print("Doações removidas.")
