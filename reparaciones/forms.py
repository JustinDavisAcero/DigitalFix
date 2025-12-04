from django import forms
from .models import Cliente, RetiroEntrega, CitaDiagnostico, Mensaje, DiagnosticoTecnico, Inventario
from datetime import time, datetime

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'correo', 'telefono', 'direccion']

class RetiroEntregaForm(forms.ModelForm):
    class Meta:
        model = RetiroEntrega
        fields = ['direccion', 'telefono', 'tipo_servicio']

class CitaDiagnosticoForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha de la cita"
    )
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'min': '09:00', 'max': '20:00', 'step': '1800'}),
        label="Hora de la cita (09:00 a 20:00)"
    )

    class Meta:
        model = CitaDiagnostico
        fields = ['correo']  # solo los campos del modelo aquí; fecha/hora son campos extra en el form

    def clean_hora(self):
        h = self.cleaned_data.get('hora')
        if h:
            min_t = time(9, 0)
            max_t = time(20, 0)
            if not (min_t <= h <= max_t):
                raise forms.ValidationError("La hora debe estar entre 09:00 y 20:00")
        return h

    def save(self, commit=True):
        instance = super().save(commit=False)
        fecha = self.cleaned_data.get('fecha')
        hora = self.cleaned_data.get('hora')
        if fecha is None or hora is None:
            raise forms.ValidationError("Fecha y hora son requeridas")
        instance.fecha_hora = datetime.combine(fecha, hora)
        if commit:
            instance.save()
        return instance

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['asunto', 'mensaje']

class DiagnosticoTecnicoForm(forms.ModelForm):
    class Meta:
        model = DiagnosticoTecnico
        fields = ['descripcion_problema', 'diagnostico']

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['nombre', 'cantidad']
