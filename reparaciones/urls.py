from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='index'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registrarse/', views.registro, name='registrarse'),
    path('perfil/', views.perfil_cliente, name='perfil_cliente'),

    path('agendar_cita/', views.agendar_cita, name='agendar_cita'),
    path('estado-reparacion/', views.estado_reparacion, name='estado_reparacion'),
    path('retiro-entrega/', views.retiro_entrega, name='retiro_entrega'),
    path('mensajes/', views.mensajes, name='mensajes'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('inventario/', views.inventario, name='inventario'),

    path('diagnostico/registrar/<int:dispositivo_id>/', views.registrar_diagnostico, name='registrar_diagnostico'),
    path('diagnostico/informe/<int:dispositivo_id>/', views.generar_informe, name='generar_informe'),

]
