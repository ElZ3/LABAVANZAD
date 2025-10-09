from django.shortcuts import render, redirect
from .models import Paciente

def lista_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'pacientes/lista.html', {'pacientes': pacientes})

def registro_paciente(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        sexo = request.POST.get('sexo')
        dui = request.POST.get('dui')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')

        Paciente.objects.create(
            nombre=nombre,
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            dui=dui,
            telefono=telefono,
            correo=correo
        )
        return redirect('lista_pacientes')
    return render(request, 'pacientes/registro.html')
