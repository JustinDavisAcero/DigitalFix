from django.contrib import admin
from django.utils.html import format_html
from .models import Cliente, Dispositivo, RetiroEntrega, CitaDiagnostico, Mensaje, DiagnosticoTecnico, Inventario


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono')
    search_fields = ('nombre', 'correo')


@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    list_display = ('numero_orden','cliente', 'tipo_dispositivo', 'modelo', 'estado', 'fecha_ingreso')
    list_filter = ('estado','tipo_dispositivo')
    search_fields = ('numero_orden','modelo','cliente__nombre')
    
    # 👇 Agregamos tu campo existente + el botón
    readonly_fields = ('numero_orden', 'boton_informe')

    # -------- BOTÓN PARA DESCARGAR INFORME --------
    def boton_informe(self, obj):
        return format_html(
            f'<a class="button" href="/diagnostico/informe/{obj.id}/" '
            f'style="padding:8px 12px; background:#28a745; color:white; border-radius:4px; text-decoration:none;">'
            f'Descargar Informe</a>'
        )
    boton_informe.short_description = "Informe Técnico"


@admin.register(RetiroEntrega)
class RetiroEntregaAdmin(admin.ModelAdmin):
    list_display = ('numero_orden','cliente','tipo_servicio','direccion','fecha_solicitud','estado')
    search_fields = ('numero_orden','cliente__nombre')


@admin.register(CitaDiagnostico)
class CitaDiagnosticoAdmin(admin.ModelAdmin):
    list_display = ('cliente','correo','fecha_hora')
    search_fields = ('cliente__nombre','correo')


@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('cliente','asunto','fecha_envio')
    search_fields = ('cliente__nombre','asunto')


@admin.register(DiagnosticoTecnico)
class DiagnosticoTecnicoAdmin(admin.ModelAdmin):
    list_display = ('dispositivo', 'fecha')
    search_fields = ('dispositivo__numero_orden',)


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad')
    search_fields = ('nombre',)
