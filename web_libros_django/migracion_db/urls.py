
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('agregar/', views.agregar_libro, name='agregar_libro'),  # Ruta para agregar un libro
    path('libros/', views.libro_list, name='libro_list'),  # Ruta para listar libros
    path('', views.libro_list, name='libro_list'),
    path('editar/<int:libro_id>/', views.libro_editar, name='libro_editar'),
    path('protegida/', views.pagina_protegida, name='pagina_protegida'),

    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),  # Asegúrate de tener una página de inicio


]