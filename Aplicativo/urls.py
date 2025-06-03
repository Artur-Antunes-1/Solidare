from django.urls import path
from . import views
from django.shortcuts import render

urlpatterns = [
    path('', views.home_view, name='home'),
    path('home/admin/', views.home_admin_view, name='homeAdmin'),
    path('registrar/', views.registrar_view, name='registrar'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('mensagens/', views.mensagens_view, name='mensagens'),
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

     # Detalhes do boletim do apadrinhado
    path(
        'aluno/<int:apadrinhado_id>/boletim/',
        views.detalhes_aluno,
        name='detalhes_aluno'
    ),

    # Gráficos de progresso do apadrinhado
    path(
        'aluno/<int:apadrinhado_id>/graficos/',
        views.historico_progresso,
        name='historico_progresso'
    ),

    # Visualização filtrada de progresso
    path(
        'aluno/<int:apadrinhado_id>/filtro/',
        views.progresso_filtrado,
        name='progresso_filtrado'
    ),
]
