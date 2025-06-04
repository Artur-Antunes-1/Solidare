from django.urls import path
from . import views
from django.shortcuts import render

urlpatterns = [
    #Homes
    path('', views.home_view, name='home'),
    path('home/admin/', views.home_admin_view, name='homeAdmin'),

    #registro/login/logout
    path('registrar/', views.registrar_view, name='registrar'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('doacoes/', views.doacoes_view, name='doacoes'),
    path('progresso/<int:aluno_id>/', views.progresso_view, name='progresso'),
    path('impacto/', views.impacto_view, name='impacto'),
    path('talentos/', views.banco_talentos_view, name='banco_talentos'),
    path('apadrinhar/', views.apadrinhamento_view, name='apadrinhar'),
    path('apadrinhar/<int:apadrinhado_id>/', views.apadrinhar_detalhes, name='apadrinhar_detalhes'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('registrar/apadrinhado/', views.registrar_apadrinhado_view, name='registrar_apadrinhado'),
    path('apadrinhados/', views.lista_apadrinhados, name='lista_apadrinhados'),
    path('apadrinhados/editar<int:apadrinhado_id>/editar', views.editar_apadrinhados, name='editar_apadrinhado'),
    path('apadrinhados/excluir<int:apadrinhado_id>/excluir', views.excluir_apadrinhado, name='excluir_apadrinhado'),
    path('meus_apadrinhados/', views.meus_apadrinhados_view, name='meus_apadrinhados'),
    path('indicar/', views.indicar_aluno, name='indicar_aluno'),
    path('contratar/', views.registrar_contratacao, name='registrar_contratacao'),
    path('sucesso/', lambda request: render(request, 'sucesso.html'), name='sucesso_contratacao'),
    
    #Mensagens
    path('mensagens/', views.mensagens_view, name='mensagens'),
    path('adm/mensagens-pendentes/', views.mensagens_pendentes_view, name='mensagens_pendentes'),
    path('mensagem/aluno/<int:aluno_id>/', views.conversa_aluno, name='conversa_aluno'),

    #Boletim
    path('adm/apadrinhado/<int:apadrinhado_id>/adicionar-progresso/', views.adicionar_progresso_view, name='adicionar_progresso'),
    path('bo letim/<int:apadrinhado_id>', views.boletim_apadrinhado, name='boletim_apadrinhado'),
    path('aluno/<int:apadrinhado_id>/boletim/', views.detalhes_aluno, name='detalhes_aluno'),
    path('aluno/<int:apadrinhado_id>/graficos/', views.historico_progresso, name='historico_progresso'),
    path('aluno/<int:apadrinhado_id>/filtro/', views.progresso_filtrado, name='progresso_filtrado'),

    #visitas
    path('agendar-visita/<int:apadrinhado_id>/', views.agendar_visita_view, name='agendar_visita'),
    path('minhas-visitas/', views.minhas_visitas_view, name='minhas_visitas'),
    path('cancelar-visita/<int:visita_id>/', views.cancelar_visita_view, name='cancelar_visita'),
    path('adm/visitas-pendentes/', views.visitas_pendentes_view, name='visitas_pendentes'),
    path('adm/aprovar-visita/<int:visita_id>/', views.aprovar_visita_view, name='aprovar_visita'),
    path('adm/recusar-visita/<int:visita_id>/', views.recusar_visita_view, name='recusar_visita'),
    path('doar/', views.realizar_doacao, name='realizar_doacao'),
    path('painel/', views. realizar_doacao, name='painel_contribuicoes'),
]
