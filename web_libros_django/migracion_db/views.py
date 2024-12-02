
from .models import Libro
from .forms import LibroForm
from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.db.models import Q  # Importar Q para condiciones OR
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

# @login_required

# def agregar_libro(request):
#     if request.method == 'POST':
#         form = LibroForm(request.POST)
#         if form.is_valid():
#             libro = form.save(commit=False)  # No guardar aún
#             libro.fecha_termino = date.today()  # Establecer la fecha actual
#             libro.save()  # Guardar con la fecha de hoy
#             return redirect('libro_list')  # Redirigir a la lista de libros
#     else:
#         form = LibroForm()
#     return render(request, 'agregar_libro.html', {'form': form})


@login_required
def agregar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST)
        if form.is_valid():
            libro = form.save(commit=False)
            libro.user = request.user  # Asociar el libro al usuario autenticado
            libro.fecha_termino = date.today()  # Fecha actual como ejemplo
            libro.save()
            return redirect('libro_list')
    else:
        form = LibroForm()
    return render(request, 'agregar_libro.html', {'form': form})

@login_required
def libro_editar(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id, user=request.user)  # Verificar que el usuario sea el propietario

    if request.method == 'POST':
        form = LibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cambios guardados correctamente.')
            return redirect('libro_list')
    else:
        form = LibroForm(instance=libro)

    return render(request, 'libro_editar.html', {'form': form, 'libro': libro})
# def libro_list(request):
#     # Obtener todos los libros
#     libros_filtrados = Libro.objects.all()

#     # Obtener los filtros aplicados
#     año = request.GET.get('año', '')  
#     mes = request.GET.get('mes', '')  
#     busqueda = request.GET.get('busqueda', '')

#     # Filtrar por año si se ha seleccionado un valor
#     if año and año != "":
#         try:
#             año = int(año)  # Asegurarse de que el año sea un entero
#             libros_filtrados = libros_filtrados.filter(fecha_termino__year=año)
#         except ValueError:
#             pass  # Si no se puede convertir a entero, no hacer el filtro
    
#     # Filtrar por mes si se ha seleccionado un valor
#     if mes and mes != "":
#         try:
#             mes = int(mes)  # Asegurarse de que el mes sea un entero
#             libros_filtrados = libros_filtrados.filter(fecha_termino__month=mes)
#         except ValueError:
#             pass  # Si no se puede convertir a entero, no hacer el filtro
    
#     # Filtrar por búsqueda si se ha ingresado algo
#     if busqueda:
#         libros_filtrados = libros_filtrados.filter(
#             Q(titulo__icontains=busqueda) | 
#             Q(autor__icontains=busqueda) | 
#             Q(tag__icontains=busqueda)
#         )

#     # Filtros adicionales por puntuación
#     puntuacion_min = request.GET.get('puntuacion_min', None)
#     puntuacion_max = request.GET.get('puntuacion_max', None)
#     if puntuacion_min:
#         libros_filtrados = libros_filtrados.filter(puntuacion__gte=puntuacion_min)
#     if puntuacion_max:
#         libros_filtrados = libros_filtrados.filter(puntuacion__lte=puntuacion_max)

#     # Ordenar por la opción seleccionada
#     ordenar_por = request.GET.get('ordenar_por', None)
#     if ordenar_por == 'puntuacion':
#         libros_filtrados = libros_filtrados.order_by('-puntuacion')
#     elif ordenar_por == 'fecha_termino':
#         libros_filtrados = libros_filtrados.order_by('-fecha_termino')

#     # Obtener los años y meses únicos para los filtros
#     años_disponibles = sorted(Libro.objects.values_list('fecha_termino__year', flat=True).distinct())
#     meses_disponibles = sorted(Libro.objects.values_list('fecha_termino__month', flat=True).distinct())

#     # Contar el número de libros que se muestran
#     total_libros = libros_filtrados.count()

#     # Si se va a eliminar uno o más libros
#     if request.method == 'POST' and 'eliminar_libros' in request.POST:
#         ids_a_eliminar = request.POST.getlist('eliminar_ids')
#         libros_filtrados.filter(id__in=ids_a_eliminar).delete()
#         return redirect('libro_list')  # Redirige a la misma página después de eliminar

#     # Renderizar la plantilla con los filtros, libros y el contador
#     return render(request, 'libro_list.html', {
#         'libros': libros_filtrados,
#         'años': años_disponibles,
#         'meses': meses_disponibles,
#         'año': año,
#         'mes': mes,
#         'busqueda': busqueda,
#         'puntuacion_min': puntuacion_min,
#         'puntuacion_max': puntuacion_max,
#         'ordenar_por': ordenar_por,
#         'total_libros': total_libros,  # Agregar el total de libros filtrados
#     })


@login_required
def libro_list(request):
    libros_filtrados = Libro.objects.filter(user=request.user)  # Filtrar libros del usuario actual

    # Mantén el resto del código de filtros y búsquedas
    año = request.GET.get('año', '')  
    mes = request.GET.get('mes', '')  
    busqueda = request.GET.get('busqueda', '')

    if año:
        try:
            año = int(año)
            libros_filtrados = libros_filtrados.filter(fecha_termino__year=año)
        except ValueError:
            pass

    if mes:
        try:
            mes = int(mes)
            libros_filtrados = libros_filtrados.filter(fecha_termino__month=mes)
        except ValueError:
            pass

    if busqueda:
        libros_filtrados = libros_filtrados.filter(
            Q(titulo__icontains=busqueda) | 
            Q(autor__icontains=busqueda) | 
            Q(tag__icontains=busqueda)
        )

    total_libros = libros_filtrados.count()

    return render(request, 'libro_list.html', {
        'libros': libros_filtrados,
        'total_libros': total_libros,
    })


from django.contrib import messages
# def libro_editar(request, libro_id):
#     # Obtener el libro a editar
#     libro = get_object_or_404(Libro, id=libro_id)

#     if request.method == 'POST':
#         form = LibroForm(request.POST, instance=libro)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Se guardaron correctamente los cambios.')
#             return redirect('libro_list')  # Redirige a la lista de libros
#     else:
#         form = LibroForm(instance=libro)

#     return render(request, 'libro_editar.html', {
#         'form': form,
#         'libro': libro,
#     })



from django.contrib.auth.views import LoginView

class MiLoginView(LoginView):
    template_name = 'login.html'

@login_required
def pagina_protegida(request):
    return render(request, 'pagina_protegida.html', {'mensaje': 'Estás autenticado'})
from .forms import UserRegistrationForm


from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Crea el nuevo usuario, pero no lo guarda aún
            user = form.save(commit=False)
            
            # Establece la contraseña de forma segura (encriptada)
            user.set_password(form.cleaned_data['password'])
            
            # Guarda el usuario en la base de datos
            user.save()
            
            # Inicia sesión con el nuevo usuario
            login(request, user)
            
            # Redirige al usuario a la página de inicio (o la que prefieras)
            return redirect('home')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Inicia sesión con el usuario
            return redirect('home')  # Redirige a la página principal después del login
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def home(request):
    return render(request, 'home.html')  # Crea una plantilla para la página principal

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')  # Redirige al usuario a la página de login (o donde prefieras)

                  