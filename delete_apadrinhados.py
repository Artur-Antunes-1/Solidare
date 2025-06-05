import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema.settings')  
django.setup()

from Aplicativo.models import Apadrinhado
apadrinhados = Apadrinhado.objects.all()

for a in apadrinhados:
    try:
        a.delete()
        print(f"Usuário {a.nome} deletado")
    except Exception as e:
        print(f"Erro ao deletar {a.nome}: {e}")