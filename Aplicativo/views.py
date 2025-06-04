from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count, Q
from django.http import HttpResponseForbidden
from django import forms
from .models import Doacao, Aluno
import json

from .models import (
    Aluno,
    Apadrinhado,
    Boletim,
    ComentarioProfessor,
    Contratacao,
    Desempenho,
    Doacao,
    Indicacao,
    Perfil,
    Profile,
    Visita,
    Mensagem,
)

def home_view(request):
    return render(request, 'home.html')

def home_admin_view(request):
    return render(request, 'homeAdmin.html')

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

@login_required
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

            try:
                perfil = Perfil.objects.get(user=user)
                if perfil.tipo_usuario == 'administrador':
                    return redirect('homeAdmin') 
                else:
                    return redirect('home')  
            except Perfil.DoesNotExist:
                return render(request, "login.html", {"erro": "Perfil de usuário não encontrado."})
        
        else:
            return render(request, "login.html", {"erro": "Usuário ou senha inválidos"})

    return render(request, "login.html")

@login_required

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
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

@login_required
def mensagens_view(request):
    perfil = getattr(request.user, 'perfil', None)
    if not perfil:
        return HttpResponseForbidden("Perfil não encontrado.")

    if perfil.tipo_usuario != 'colaborador':
        # Se não for colaborador, redireciona ao painel de pendentes (admin)
        return redirect('mensagens_pendentes')

    # Filtra apenas os apadrinhados que pertencem a este colaborador
    meus_apadrinhados = Apadrinhado.objects.filter(apadrinhado_por=request.user)

    if request.method == 'POST':
        ap_id = request.POST.get('apadrinhado_id')
        texto = request.POST.get('texto', '').strip()
        if ap_id and texto:
            # Garante que o colaborador só envie mensagem a um apadrinhado realmente seu
            ap = get_object_or_404(Apadrinhado, id=ap_id, apadrinhado_por=request.user)
            Mensagem.objects.create(
                remetente=request.user,
                destinatario=ap,
                texto=texto,
                entregue=False   # marca como “pendente” até o admin visualizar
            )
        # after sending, volta para a mesma lista de mensagens do colaborador
        return redirect('mensagens')

    # Ao exibir a página, passamos uma lista de dicionários com cada apadrinhado
    lista_info = [{'apadrinhado': ap} for ap in meus_apadrinhados]
    return render(request, 'mensagens.html', {
        'lista_info': lista_info,
    })


@login_required
def mensagens_pendentes_view(request):
    perfil = getattr(request.user, 'perfil', None)
    if not perfil or perfil.tipo_usuario != 'administrador':
        return HttpResponseForbidden("Acesso restrito: apenas administradores podem ver mensagens.")

    # “mensagens” é o related_name que ligamos no modelo Mensagem.destinatario
    apadrinhados = Apadrinhado.objects.annotate(
        pendentes=Count('mensagens', filter=Q(mensagens__entregue=False))
    ).order_by('nome')

    return render(request, 'mensagens_pendentes.html', {
        'apadrinhados': apadrinhados,
    })


@login_required
def conversa_aluno(request, aluno_id):
    perfil = getattr(request.user, 'perfil', None)
    if not perfil:
        return HttpResponseForbidden("Perfil não encontrado.")
    
    if request.user.perfil.tipo_usuario == 'administrador':
        base = 'homeAdmin.html'
    else:
        base = 'home.html'

    apadrinhado = get_object_or_404(Apadrinhado, id=aluno_id)

    # Se for colaborador, só acessa se ele for padrinho desse apadrinhado
    if perfil.tipo_usuario == 'colaborador' and apadrinhado.apadrinhado_por != request.user:
        return HttpResponseForbidden("Você não tem permissão para acessar esta conversa.")

    # Marca todas as mensagens pendentes como entregues (independente de ser GET ou POST)
    Mensagem.objects.filter(destinatario=apadrinhado, entregue=False).update(entregue=True)

    # Se vier um POST e for admin, cria a mensagem de resposta
    if request.method == 'POST' and perfil.tipo_usuario == 'administrador':
        texto_resposta = request.POST.get('texto_resposta', '').strip()
        if texto_resposta:
            Mensagem.objects.create(
                remetente=request.user,
                destinatario=apadrinhado,
                texto=texto_resposta,
                entregue=False  # já cadastra como pendente, para que o colaborador saiba que tem mensagem nova
            )
        # Depois redireciona para mesmo view, para recarregar a lista de mensagens (e já marcar como entregues antigas)
        return redirect('conversa_aluno', aluno_id=aluno_id)

    # Para GET: busca todas as mensagens (já marcadas como entregues na linha anterior)
    todas_mensagens = Mensagem.objects.filter(destinatario=apadrinhado).order_by('timestamp')

    return render(request, 'conversa_aluno.html', {
        'apadrinhado': apadrinhado,
        'mensagens': todas_mensagens,
        'base_template': base,
    })


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
    alunos = Aluno.objects.filter(apadrinhado_por=request.user).count()
    return render(request, 'impacto.html', {'total_doado': total, 'num_alunos': alunos})

@login_required
def banco_talentos_view(request):
    alunos = Aluno.objects.all()
    return render(request, 'banco_talentos.html', {'alunos': alunos})

@login_required
def apadrinhamento_view(request):
    # carrega todos os apadrinhados
    apadrinhados = Apadrinhado.objects.all()
    # sempre retorna um HttpResponse
    return render(request, 'apadrinhar.html', {
        'apadrinhados': apadrinhados
    })
    
@login_required
def apadrinhar_detalhes(request, apadrinhado_id):
    ap = get_object_or_404(Apadrinhado, id=apadrinhado_id)
    if request.method == 'POST':
        ap.apadrinhado_por = request.user
        ap.save()
        # aqui você executa a lógica de “apadrinhar” (salvar no banco, enviar email etc.)
        messages.success(request, f'Você escolheu apadrinhar {ap.nome}.')
        return redirect('meus_apadrinhados')
    return render(request, 'apadrinhar_confirm.html', {
        'apadrinhado': ap
    })

@login_required
def meus_apadrinhados_view(request):
    meus = Apadrinhado.objects.filter(apadrinhado_por=request.user)
    return render(request, 'meus_apadrinhados.html', {
        'apadrinhados': meus
    })

@login_required
def indicar_aluno(request):
    if request.method == 'POST':
        aluno_id        = request.POST.get('aluno_id')
        empresa         = request.POST.get('empresa')
        descricao_vaga  = request.POST.get('descricao_vaga')
        recomendacao    = request.POST.get('recomendacao')

        erros = []
        if not aluno_id:
            erros.append('Selecione o aluno.')
        if not empresa:
            erros.append('Nome da empresa é obrigatório.')
        if not descricao_vaga:
            erros.append('Descreva a vaga.')
        if not recomendacao:
            erros.append('Escreva sua recomendação.')

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
                )
                return redirect('sucesso_indicacao')
            
    alunos = Aluno.objects.all() 
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

@login_required
def detalhes_aluno(request, apadrinhado_id):
    """
    Cenário 1: Consulta ao boletim do apadrinhado (notas, frequência, comentários).
    """
    apadrinhado = get_object_or_404(Apadrinhado, id=apadrinhado_id)
    desempenho = Desempenho.objects.filter(apadrinhado=apadrinhado).order_by('mes')

    if request.user.perfil.tipo_usuario == 'administrador':
        base = 'homeAdmin.html'
    else:
        base = 'home.html'

    return render(request, 'detalhes_aluno.html', {
        'apadrinhado': apadrinhado,
        'base_template': base,
        'desempenho': desempenho,
    })


@login_required
def boletim_apadrinhado(request, apadrinhado_id):
    apadrinhado = get_object_or_404(Apadrinhado, id=apadrinhado_id)

    if request.user.perfil.tipo_usuario == 'administrador':
        base = 'homeAdmin.html'
    else:
        base = 'home.html'

    # Se já existir lógica de permissão, mantenha aqui antes de buscar desempenho
    desempenho_list = Desempenho.objects.filter(apadrinhado=apadrinhado).order_by('mes')

    return render(request, 'boletim_apadrinhado.html', {
        'apadrinhado': apadrinhado,
        'base_template': base,
        'desempenho_list': desempenho_list,
    })

@login_required
def historico_progresso(request, apadrinhado_id):
    """
    Cenário 2: Relatórios de progresso periódicos - gráficos e estatísticas
    Somente administradores ou o próprio padrinho do apadrinhado podem acessar.
    """
    apadrinhado = get_object_or_404(Apadrinhado, id=apadrinhado_id)

    if request.user.perfil.tipo_usuario == 'administrador':
        base = 'homeAdmin.html'
    else:
        base = 'home.html'

    # 1) Verifica permissão: se não for admin nem padrinho, nega.
    perfil = getattr(request.user, 'perfil', None)
    if not perfil:
        return HttpResponseForbidden("Perfil não encontrado.")

    if perfil.tipo_usuario != 'administrador' and apadrinhado.apadrinhado_por != request.user:
        return HttpResponseForbidden("Você não tem permissão para visualizar este histórico.")

    # 2) Busca os registros de Desempenho
    desempenho = Desempenho.objects.filter(apadrinhado=apadrinhado).order_by('mes')

    meses = [d.mes for d in desempenho]
    notas = [float(d.nota) for d in desempenho]
    frequencias = [float(d.frequencia) for d in desempenho]

    meses_json = json.dumps(meses)
    notas_json = json.dumps(notas)
    frequencias_json = json.dumps(frequencias)

    context = {
        'apadrinhado': apadrinhado,
        'meses_json': meses_json,
        'notas_json': notas_json,
        'frequencias_json': frequencias_json,
        'base_template': base,
    }
    return render(request, 'historico_progresso.html', context)

@login_required
def progresso_filtrado(request, apadrinhado_id):
    """
    Cenário 3: Relatórios personalizados com filtros via GET
    Parâmetro 'filtro' pode ser: 'nota', 'frequencia' ou 'comentario'.
    """
    apadrinhado = get_object_or_404(Apadrinhado, id=apadrinhado_id)
    
    if request.user.perfil.tipo_usuario == 'administrador':
        base = 'homeAdmin.html'
    else:
        base = 'home.html'

    filtro = request.GET.get('filtro', 'nota')  # valor padrão: nota

    desempenho = Desempenho.objects.filter(apadrinhado=apadrinhado).order_by('mes')

    if filtro == 'nota':
        dados = [(registro.mes, registro.nota) for registro in desempenho]
    elif filtro == 'frequencia':
        dados = [(registro.mes, registro.frequencia) for registro in desempenho]
    elif filtro == 'comentario':
        dados = [(registro.mes, registro.comentario_professor) for registro in desempenho]
    else:
        dados = []

    return render(request, 'progresso_filtrado.html', {
        'apadrinhado': apadrinhado,
        'dados': dados,
        'filtro': filtro,
        'base_template': base,
    })

@login_required
def agendar_visita_view(request, apadrinhado_id):
    # Apenas padrinhos podem agendar (todos usuários que não sejam admin, por exemplo).
    # Aqui pressupomos que 'administrador' é o tipo de perfil que não faz agendamentos.
    try:
        tipo = request.user.perfil.tipo_usuario
    except Perfil.DoesNotExist:
        return HttpResponseForbidden("Perfil não encontrado.")

    if tipo == 'administrador':
        return HttpResponseForbidden("Administradores não podem agendar visita como padrinho.")

    apadrinhado = get_object_or_404(Apadrinhado, id=apadrinhado_id)

    # Verifica se este apadrinhado já está com outro padrinho?
    # Se quiser permitir apenas padrinhos já vinculados, faça:
    # if apadrinhado.apadrinhado_por != request.user:
    #     return HttpResponseForbidden("Você não é padrinho deste aluno.")

    if request.method == 'POST':
        data = request.POST.get('data')
        hora = request.POST.get('hora')
        motivo = request.POST.get('motivo', '').strip()

        erros = []
        if not data:
            erros.append("Data é obrigatória.")
        if not hora:
            erros.append("Hora é obrigatória.")
        if not motivo:
            erros.append("Motivo é obrigatório.")

        if erros:
            for erro in erros:
                messages.error(request, erro)
            # Re-renderiza o form com os erros
            return render(request, 'agendar_visita.html', {
                'apadrinhado': apadrinhado,
                'data': data,
                'hora': hora,
                'motivo': motivo,
            })

        # Cria a visita com status “Pendente”
        Visita.objects.create(
            padrinho=request.user,
            apadrinhado=apadrinhado,
            data=data,
            hora=hora,
            motivo=motivo,
            status='Pendente'
        )

        messages.success(request, "Visita solicitada com sucesso! Aguarde aprovação do administrador.")
        return redirect('minhas_visitas')

    # GET: exibe formulário em branco
    return render(request, 'agendar_visita.html', {
        'apadrinhado': apadrinhado
    })

@login_required
def minhas_visitas_view(request):
    visitas = Visita.objects.filter(padrinho=request.user).order_by('-data_solicitacao')
    return render(request, 'minhas_visitas.html', {
        'visitas': visitas
    })

@login_required
def cancelar_visita_view(request, visita_id):
    visita = get_object_or_404(Visita, id=visita_id)

    # Só o próprio padrinho da visita pode cancelar
    if visita.padrinho != request.user:
        return HttpResponseForbidden("Você não tem permissão para cancelar esta visita.")

    # Se já estiver cancelada, apenas redireciona
    if visita.status == 'Cancelada':
        messages.info(request, "Visita já está cancelada.")
        return redirect('minhas_visitas')

    # Permite cancelar visitas pendentes ou confirmadas
    visita.status = 'Cancelada'
    visita.save()
    messages.success(request, "Visita cancelada com sucesso.")
    return redirect('minhas_visitas')

@login_required
def visitas_pendentes_view(request):
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        return HttpResponseForbidden("Perfil não encontrado.")

    if perfil.tipo_usuario != 'administrador':
        return HttpResponseForbidden("Acesso restrito a administradores.")

    visitas_pendentes = Visita.objects.filter(status='Pendente').order_by('data', 'hora')
    return render(request, 'visitas_pendentes.html', {
        'visitas': visitas_pendentes
    })

@login_required
def aprovar_visita_view(request, visita_id):
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        return HttpResponseForbidden("Perfil não encontrado.")

    if perfil.tipo_usuario != 'administrador':
        return HttpResponseForbidden("Acesso restrito a administradores.")

    visita = get_object_or_404(Visita, id=visita_id)

    # Só aprova se estiver pendente
    if visita.status != 'Pendente':
        messages.error(request, "Esta visita não está mais pendente.")
        return redirect('visitas_pendentes')

    visita.status = 'Confirmada'
    visita.save()
    messages.success(request, f"Visita de {visita.padrinho.username} a {visita.apadrinhado.nome} confirmada.")
    return redirect('visitas_pendentes')

@login_required
def recusar_visita_view(request, visita_id):
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        return HttpResponseForbidden("Perfil não encontrado.")

    if perfil.tipo_usuario != 'administrador':
        return HttpResponseForbidden("Acesso restrito a administradores.")

    visita = get_object_or_404(Visita, id=visita_id)

    # Só recusar se estiver pendente
    if visita.status != 'Pendente':
        messages.error(request, "Esta visita não está mais pendente.")
        return redirect('visitas_pendentes')

    visita.status = 'Cancelada'
    visita.save()
    messages.success(request, f"Visita de {visita.padrinho.username} a {visita.apadrinhado.nome} recusada.")
    return redirect('visitas_pendentes')

@login_required
def adicionar_progresso_view(request, apadrinhado_id):
    # 1) Verifica se é administrador
    try:
        if request.user.perfil.tipo_usuario != 'administrador':
            return HttpResponseForbidden("Acesso restrito: somente administradores podem adicionar progresso.")
    except Perfil.DoesNotExist:
        return HttpResponseForbidden("Perfil não encontrado.")

    # 2) Busca o objeto Apadrinhado ou 404
    ap = get_object_or_404(Apadrinhado, id=apadrinhado_id)

    if request.method == 'POST':
        mes = request.POST.get('mes', '').strip()
        nota = request.POST.get('nota', '').strip()
        frequencia = request.POST.get('frequencia', '').strip()
        comentario = request.POST.get('comentario', '').strip()

        erros = []
        if not mes:
            erros.append("Campo 'Mês' é obrigatório.")
        if not nota:
            erros.append("Campo 'Nota' é obrigatório.")
        if not frequencia:
            erros.append("Campo 'Frequência' é obrigatório.")

        # Se houver erros, exibe no template
        if erros:
            for e in erros:
                messages.error(request, e)
            return render(request, 'adicionar_progresso.html', {'apadrinhado': ap})

        # Cria o Desempenho
        try:
            Desempenho.objects.create(
                apadrinhado=ap,
                mes=mes,
                nota=nota,
                frequencia=frequencia,
                comentario_professor=comentario
            )
            messages.success(request, f"Progresso de '{ap.nome}' registrado para {mes}.")
            return redirect('historico_progresso', apadrinhado_id=ap.id)
        except Exception:
            messages.error(request, "Falha ao salvar o progresso.")
            return render(request, 'adicionar_progresso.html', {'apadrinhado': ap})

    # GET: apenas exibe o formulário vazio
    return render(request, 'adicionar_progresso.html', {'apadrinhado': ap})


class InlineDoacaoForm(forms.Form):
    aluno = forms.ModelChoiceField(queryset=Aluno.objects.all())
    tipo = forms.ChoiceField(choices=Doacao.TIPO_CHOICES)
    valor = forms.DecimalField(required=False)
    descricao = forms.CharField(widget=forms.Textarea, required=False)

def realizar_doacao(request):
    if request.method == 'POST':
        form = InlineDoacaoForm(request.POST)
        if form.is_valid():
            aluno = form.cleaned_data['aluno']
            tipo = form.cleaned_data['tipo']
            valor = form.cleaned_data['valor']
            descricao = form.cleaned_data['descricao']
            doacao = Doacao(
                colaborador=request.user,
                aluno=aluno,
                tipo=tipo,
                valor=valor,
                descricao=descricao
            )
            try:
                if tipo == 'financeira' and (not valor or valor <= 0):
                    raise ValueError("Valor inválido para doação financeira.")
                doacao.sucesso = True
                messages.success(request, "Doação realizada com sucesso!")
            except Exception as e:
                doacao.sucesso = False
                doacao.mensagem_erro = str(e)
                messages.error(request, f"Erro na doação: {e}")
            doacao.save()
            return redirect('painel_contribuicoes')
    else:
        form = InlineDoacaoForm()
    return render(request, 'doacoes/realizar_doacao.html', {'form': form})
