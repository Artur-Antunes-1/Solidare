from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# MODELS
class Perfil(models.Model):
    TIPOS_USUARIO = (
        ('administrador', 'Administrador'),
        ('colaborador', 'Colaborador'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO)

    def __str__(self):
        return f"{self.user.username} - {self.get_tipo_usuario_display()}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    nome = models.CharField(max_length=100, blank=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'

    @property
    def foto_url(self):
        if self.foto:
            return self.foto.url
        return '/static/img/user-icon.jpg'

@receiver(post_save, sender=User)
def criar_ou_atualizar_perfil(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='alunos_fotos/')
    apadrinhado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apadrinhados')

    def __str__(self):
        return self.nome


class Mensagem(models.Model):
    remetente = models.ForeignKey(User, on_delete=models.CASCADE)
    destinatario = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    texto = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    entregue = models.BooleanField(default=False)

class Doacao(models.Model):
    TIPO_CHOICES = [('Financeira', 'Financeira'), ('Material', 'Material')]
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    descricao = models.CharField(max_length=255, blank=True)
    comprovante = models.FileField(upload_to='comprovantes/', null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

class Boletim(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    materia = models.CharField(max_length=50)
    nota = models.FloatField()
    frequencia = models.IntegerField()

class ComentarioProfessor(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    comentario = models.TextField()
    data = models.DateField(auto_now_add=True)

class Indicacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    colaborador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='indicacoes_feitas')
    empresa = models.CharField(max_length=100)
    descricao_vaga = models.TextField()
    recomendacao = models.TextField()
    status = models.CharField(max_length=30, default='Pendente')

    def __str__(self):
        return f"{self.aluno.nome} indicado por {self.colaborador.username} para {self.empresa}"

class FeedbackEmpresa(models.Model):
    indicacao = models.OneToOneField(Indicacao, on_delete=models.CASCADE)
    feedback = models.TextField()
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Feedback sobre {self.indicacao.aluno.nome} em {self.data}"

class Contratacao(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    empresa = models.CharField(max_length=100)
    data_contratacao = models.DateField()
    registrada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.aluno.nome} contratado por {self.empresa}"

class Apadrinhado(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]

    nome = models.CharField(max_length=100)
    idade = models.PositiveIntegerField()
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    apadrinhado_por = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='meus_apadrinhados',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.nome


class Desempenho(models.Model):
    apadrinhado = models.ForeignKey(Apadrinhado, on_delete=models.CASCADE)
    mes = models.CharField(max_length=20)
    nota = models.DecimalField(max_digits=4, decimal_places=2)
    frequencia = models.DecimalField(max_digits=5, decimal_places=2)
    comentario_professor = models.TextField(blank=True)

    def __str__(self):
        # Exibe “<nome do apadrinhado> – <mês>”
        return f"{self.apadrinhado.nome} - {self.mes}"
    
class Visita(models.Model):
    STATUS_CHOICES = (
        ('Pendente', 'Pendente'),
        ('Confirmada', 'Confirmada'),
        ('Cancelada', 'Cancelada'),
    )

    padrinho = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='visitas_solicitadas'
    )
    apadrinhado = models.ForeignKey(
        Apadrinhado,
        on_delete=models.CASCADE,
        related_name='visitas_recebidas'
    )
    data = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pendente'
    )
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visita de {self.padrinho.username} a {self.apadrinhado.nome} em {self.data} {self.hora} ({self.status})"