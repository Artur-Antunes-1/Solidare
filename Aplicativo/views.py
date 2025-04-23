from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from .models import Aluno, Doacao, Boletim, ComentarioProfessor, Perfil
from django.db import IntegrityError
from .models import Apadrinhado
from django.http import HttpResponseForbidden
from .models import Indicacao, Contratacao

def home_view(request):
    return render(request, 'home.html')

def registrar_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        tipo_usuario = request.POST.get('tipo_usuario', 'colaborador')  

        if password1 != password2:
            messages.error(request, "As senhas não coincidem.")
            return render(request, 'registrar.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Nome de usuário já existe.")
            return render(request, 'registrar.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Já existe uma conta com este e-mail.")
            return render(request, 'registrar.html')

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            Perfil.objects.create(user=user, tipo_usuario=tipo_usuario)
            login(request, user)
            return redirect('login')
        except IntegrityError:
            messages.error(request, "Erro ao criar o usuário.")
    return render(request, 'registrar.html')


def registrar_apadrinhado_view(request):
    if not request.user.perfil.tipo_usuario == 'administrador':
        return HttpResponseForbidden("Apenas administradores podem cadastrar apadrinhados.")
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        idade = request.POST.get('idade', '')
        genero = request.POST.get('genero', '')

        if not nome or not idade or not genero:
            messages.error(request, "Todos os campos são obrigatórios.")
            return render(request, 'registrar_apadrinhado.html')
        
        try:
            Apadrinhado.objects.create(
                nome=nome,
                idade=idade,
                genero=genero
            )
            messages.success(request, "Apadrinhado cadastrado com sucesso!")
            return redirect('lista_apadrinhados')
        except Exception:
            messages.error(request, "Erro ao cadastrar apadrinhado.")
            
    return render(request, 'registrar_apadrinhado.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "login.html", {"erro": "Usuário ou senha inválidos"})

    return render(request, "login.html")
@login_required

def logout_view(request):
    logout(request)
    return redirect('login')

def lista_apadrinhados(request):
    
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        messages.error(request, "Cadastre-se como administrador para acessar essa página.")
        return redirect('home')
    
    if perfil.tipo_usuario != 'administrador':
        return HttpResponseForbidden("Acesso restrito a administradores.")

    apadrinhados = Apadrinhado.objects.all()  
    return render(request, "lista_apadrinhados.html", {'apadrinhados': apadrinhados})

@login_required
def editar_apadrinhados(request,apadrinhado_id):
    if request.user.perfil.tipo_usuario != 'administrador':
        return redirect('home')
    
    apadrinhado = get_object_or_404(Apadrinhado, id=apadrinhado_id)

    if request.method == 'POST':
        apadrinhado.nome = request.POST.get('nome')
        apadrinhado.idade = request.POST.get('idade')
        apadrinhado.genero = request.POST.get('genero')
        apadrinhado.save()
        return redirect('lista_apadrinhados')

    return render(request, 'editar_apadrinhados.html', {'apadrinhado': apadrinhado})

@login_required
def excluir_apadrinhado(request, apadrinhado_id):

    if request.user.perfil.tipo_usuario != 'administrador':
        return redirect('home')
    apadrinhado = get_object_or_404(Apadrinhado, id=apadrinhado_id)
    if request.method == 'POST':
        apadrinhado.delete()
    return redirect('lista_apadrinhados')

def mensagens_view(request):
    alunos = Aluno.objects.filter(aluno_por=request.user)
    return render(request, 'mensagens.html', {'alunos': alunos})

@login_required
def doacoes_view(request):
    return render(request, 'doacoes.html')

@login_required
def progresso_view(request, aluno_id):
    aluno = Aluno.objects.get(id=aluno_id)
    boletins = Boletim.objects.filter(aluno=aluno)
    comentarios = ComentarioProfessor.objects.filter(aluno=aluno)
    return render(request, 'progresso.html', {'aluno': aluno, 'boletins': boletins, 'comentarios': comentarios})

@login_required
def impacto_view(request):
    doacoes = Doacao.objects.filter(usuario=request.user)
    total = sum(d.valor for d in doacoes if d.valor)
    alunos = Aluno.objects.filter(aluno_por=request.user).count()
    return render(request, 'impacto.html', {'total_doado': total, 'num_alunos': alunos})

@login_required
def banco_talentos_view(request):
    alunos = Aluno.objects.all()
    return render(request, 'banco_talentos.html', {'alunos': alunos})

@login_required
def apadrinhamento_view(request):
    return render(request, 'apadrinhamento.html')

@login_required
def indicar_aluno(request):
    if request.method == 'POST':
        # capturar dados
        aluno_id        = request.POST.get('aluno_id')
        empresa         = request.POST.get('empresa')
        descricao_vaga  = request.POST.get('descricao_vaga')
        recomendacao    = request.POST.get('recomendacao')

        # validação mínima
        erros = []
        if not aluno_id:
            erros.append('Selecione o aluno.')
        if not empresa:
            erros.append('Nome da empresa é obrigatório.')
        if not descricao_vaga:
            erros.append('Descreva a vaga.')
        if not recomendacao:
            erros.append('Escreva sua recomendação.')

        # exibir erros, se houver
        if erros:
            for erro in erros:
                messages.error(request, erro)
        else:
            try:
                aluno = Aluno.objects.get(id=aluno_id)
            except Aluno.DoesNotExist:
                messages.error(request, 'Aluno não encontrado.')
            else:
                Indicacao.objects.create(
                    aluno       = aluno,
                    colaborador = request.user,
                    empresa     = empresa,
                    descricao_vaga = descricao_vaga,
                    recomendacao = recomendacao,
                    # status fica no default “Pendente”
                )
                return redirect('sucesso_indicacao')

    # GET ou POST inválido → mostra o formulário
    alunos = Aluno.objects.all()   # para popular um <select>
    return render(request, 'indicar.html', {'alunos': alunos})

@login_required
def registrar_contratacao(request):
    if request.method == 'POST':
        aluno_id        = request.POST.get('aluno_id')
        data_admissao   = request.POST.get('data_admissao')
        cargo           = request.POST.get('cargo')
        salario         = request.POST.get('salario')

        erros = []
        if not aluno_id:
            erros.append('Aluno é obrigatório.')
        if not data_admissao:
            erros.append('Data de admissão é obrigatória.')
        if erros:
            for erro in erros:
                messages.error(request, erro)
        else:
            Contratacao.objects.create(
                aluno_id=aluno_id,
                data_admissao=data_admissao,
                cargo=cargo,
                salario=salario,
                registrada_por=request.user
            )
            return redirect('sucesso_contratacao')

    return render(request, 'contratacoes/registrar.html')

@login_required
def perfil_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    is_editing = request.GET.get('editar') == '1'

    if request.method == 'POST':
        bio = request.POST.get('bio')
        foto = request.FILES.get('foto')
        email = request.POST.get('email')

        request.user.email = email
        request.user.save()

        if bio:
            profile.bio = bio
        if foto:
            profile.foto = foto
        profile.save()


        messages.success(request, "Perfil atualizado com sucesso!")
        return redirect('perfil')

    return render(request, 'perfil.html', {
        'email': request.user.email,
        'usuario': request.user.usuario,
        'foto': profile.foto.url if profile.foto else None,
        'profile': profile,
        'is_editing': is_editing,
    })
