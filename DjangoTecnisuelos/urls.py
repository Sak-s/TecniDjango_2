"""
URL configuration for DjangoTecnisuelos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.contrib import admin
from django.urls import path
from .views import export_pdf_report
from django.contrib.auth import views as auth_views
from .views import export_pdf_report_labo


# Media files
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    
    path('admin/', admin.site.urls, name='admin:index'),
    path('crearCuenta/', views.register_view, name='crearCuenta'),
    path('inicio/', views.login_view, name='inicio'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.index, name = 'index'),
    path('servicios/', views.servicios, name='servicios'),
    path('confirmar_cita_email/', views.confirmar_cita_email, name='confirmar_cita_email'),
    path('agendar/', views.agendar, name='agendar'),
    path('contacto/', views.contacto, name='contacto'),
    path('histoInformes/', views.histoInformes, name='histoInformes'),
    path('Pnatural/', views.persona_natural, name='Pnatural'),
    path('Pjuridica/', views.persona_juridica, name='Pjuridica'),
    path('export-pdf-report/', views.export_pdf_report, name='export_pdf_report'),
    path('export_pdf_report_inve/', views.export_pdf_report_inve, name='export_pdf_report_inve'),
    path('export_pdf_report_test/', views.export_pdf_report_test, name='export_pdf_report_test'),
    path('export_pdf_report_labo/', views.export_pdf_report_labo, name='export_pdf_report_labo'),
    path('store_cliente/', views.store_cliente, name='store_cliente'),
    path('store_cliente_juridica/', views.store_cliente_juridica, name='store_cliente_juridica'),
    path('404/', views.error404, name='404'),
    path('500/', views.error500, name='500'),
    path('laboratorista/', views.laboratorista, name='laboratorista'),
    path('cronograma/', views.cronograma, name='cronograma'),
    path('administrador/', views.administrador, name='administrador'),
    
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='RecupContra.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='AnuncioR.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='nuevaC.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='contraseñaC.html'), name='password_reset_complete'),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




