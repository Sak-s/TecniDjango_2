# views.py
import math
from pyexpat.errors import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from core.models import LegalClient, Client, FielTrial, Inventory, LaboratoryTrial, LaboratoryWorker
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from core.forms import CustomUserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string

from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate
from io import BytesIO


def index(request):
    return render(request, "index.html")


def servicios(request):
    return render(request, "servicios.html")


def agendar(request):
    return render(request, "agendar.html")


def cronograma(request):
    return render(request, "cronograma.html")


def administrador(request):
    return render(request, "administrador.html")


def histoInformes(request):
    return render(request, "histoInformes.html")


def contacto(request):
    return render(request, "contactos.html")


def recuperar_contrasena(request):
    return render(request, "RecupContra.html")


def error404(request, exceptiopn):
    return render(request, "404.html", status=404)


def error500(request):
    return render(request, "500.html", status=500)


def laboratorista(request):
    return render(request, "laboratorista.html")


def persona_natural(request):
    return render(request, "Pnatural.html")

def persona_juridica(request):
    return render(request, "Pjuridica.html")

def anuncioR(request):
    return render(request, "AnuncioR.html")

def nuevaC(request):
    return render(request, "nuevaC.html")

def contraseñaC(request):
    return render(request, "contraseñaC.html")


def reset_done (request):
    return render(request, "reset_done.html")


def confirmar_cita_email(request):
    return render(request, "confirmar_cita_email.html")

def export_pdf_report_test(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="FielTrial_report.pdf"'
    pdf = canvas.Canvas(response, pagesize=landscape(letter))

    image_path = 'static/Imagenes/logito.jpg'   
    pdf.drawImage(image_path, x=20, y=550, width=200, height=50)
    
    col_widths = [pdf.stringWidth(field.verbose_name, 'Helvetica', 10) + 35 for field in FielTrial._meta.fields]
    row_height = 16  
    table_width = sum(col_widths)
    table_height = row_height * 2
    x = 20
    y = pdf._pagesize[1] - 120  # Ajuste en la posición vertical
    text_y = y + (row_height / 2) - 4
    
    # Encabezado con fondo de color y líneas divisorias
    pdf.setFillColor(colors.HexColor('#2d7da5'))  # Azul
    pdf.setStrokeColor(colors.black)
    pdf.setLineWidth(1)
    pdf.rect(x, y, table_width, row_height, fill=True)
    pdf.setFont("Helvetica-Bold", 10)  # Texto en negrita
    
    # Dibujar líneas divisorias entre las columnas
    for i, width in enumerate(col_widths, start=1):
        pdf.line(x + sum(col_widths[:i]), y, x + sum(col_widths[:i]), y - table_height)
    
    # Escribir los encabezados centrados verticalmente
    for i, field in enumerate(FielTrial._meta.fields):
        pdf.setFillColor(colors.white)
        text_width = pdf.stringWidth(field.verbose_name, 'Helvetica', 10)
        text_x = x + sum(col_widths[:i]) + (col_widths[i] - text_width) / 2
        pdf.drawString(text_x, text_y, field.verbose_name)
        pdf.setFillColor(colors.black) 
    
    # Líneas divisorias entre columnas
    for i, width in enumerate(col_widths, start=1):
        pdf.line(x + sum(col_widths[:i]), y, x + sum(col_widths[:i]), y - table_height)

    # Datos de la tabla

    FielTrials = FielTrial.objects.all()
    pdf.setFont("Helvetica", 10)  # Texto normal
    for fielTrial in FielTrials:
        y -= row_height
        for i, field in enumerate(FielTrial._meta.fields):
            value = str(getattr(fielTrial, field.name))
            # Truncar el texto si es necesario y centrar en la celda
            text_width = pdf.stringWidth(value[:15], 'Helvetica', 10)
            text_x = x + sum(col_widths[:i]) + (col_widths[i] - text_width) / 2
            pdf.drawString(text_x, y, value[:15])

    pdf.showPage()
    pdf.save()

    return response

def export_pdf_report_labo(request):
    # Mapeo de nombres de campos en inglés a español
    field_names = {
        "id": "ID",
        "laboratory_name": "Nombre del Laboratorista",
        "date": "Fecha de Prueba",
        "cylinder_number": "Número de Cilindro",
        "test_number": "Número de Prueba",
        "name_client": "Nombre del Cliente",
        "air_content": "Contenido de Aire",
        "contraction_drying": "Contracción al Secar",
        "analysis_petrographics": "Análisis Petrográfico",
        "elasticity_extensometer": "Elasticidad del Extensómetro",
        "petrographic_study": "Estudio Petrográfico",
        "concrete_flexion": "Flexión de Concreto",
        "compression": "Compresión",
        "granulometry": "Granulometría",
        "permeability_testing": "Pruebas de Permeabilidad",
        "type_trial": "Tipo de Prueba",
        "profile": "Perfil",
        "approval_status": "Estado de Aprobación",
    }

    # Crear la respuesta HTTP y el objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="laboratory_trial_report.pdf"'

    # Obtener los datos de los LaboratoryTrial
    laboratory_trials = LaboratoryTrial.objects.all()

    # Crear el documento PDF
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle("Informe de Prueba de Laboratorio")

    # Logo
    image_path = 'static/Imagenes/logito.jpg'
    pdf.drawImage(image_path, x=50, y=750, width=200, height=50)

    # Título
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 700, "Resultado de Laboratorio")

    # Separador
    pdf.line(50, 690, 550, 690)

    # Coordenadas iniciales
    x = 50
    y = 650

    # Espacio entre líneas
    line_height = 20

    # Encabezados de tabla
    headers = ["Campo", "Resultado"]

    # Color de fondo para los encabezados
    pdf.setFillColor(colors.HexColor('#2d7da5'))  # Azul
    pdf.rect(x, y, 150, line_height, fill=True)
    pdf.rect(x + 150, y, 150, line_height, fill=True)

    # Color de texto para los encabezados
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 12)

    # Dibujar encabezados
    pdf.drawString(x + 20, y + 4, headers[0])
    pdf.drawString(x + 150 + 20, y + 4, headers[1])

    # Restaurar color de texto
    pdf.setFillColor(colors.black)

    # Datos
    pdf.setFont("Helvetica", 10)

    for trial in laboratory_trials:
        for field in field_names.keys():
            # Obtener el valor del campo
            field_value = str(getattr(trial, field))

            # Calcular la altura necesaria para el texto
            text_height = pdf.stringWidth(field_value, "Helvetica", 10)
            num_lines = max(1, int(math.ceil(text_height / (150 - 20))))  # 150 es el ancho del cuadro

            # Ajustar la posición Y si se necesita más espacio
            if y - num_lines * line_height < 50:  # 50 es la posición Y mínima
                pdf.showPage()  # Cambiar de página
                y = 750  # Restablecer la posición Y inicial

            # Dibujar cuadro alrededor del campo
            pdf.rect(x, y - num_lines * line_height, 150, num_lines * line_height, stroke=True)
            pdf.rect(x + 150, y - num_lines * line_height, 150, num_lines * line_height, stroke=True)

            # Escribir el nombre del campo
            pdf.drawString(x + 5, y - 10 - (num_lines - 1) * line_height, field_names[field])

            # Establecer el color del fondo solo para el campo de Estado de Aprobación
            if field == 'approval_status':
                # Determinar el color del fondo basado en el estado de aprobación
                if field_value == 'Aprobado':
                    pdf.setFillColorRGB(0, 1, 0)  # Verde
                else:
                    pdf.setFillColorRGB(1, 0, 0)  # Rojo

                # Dibujar cuadro de fondo solo para el campo de Estado de Aprobación
                pdf.rect(x + 150, y - num_lines * line_height, 150, num_lines * line_height, fill=True)

            # Restaurar color de relleno a negro para el texto
            pdf.setFillColor(colors.black)

            # Escribir el valor del campo
            pdf.drawString(x + 150 + 5, y - 10 - (num_lines - 1) * line_height, field_value)

            # Actualizar la posición Y
            y -= num_lines * line_height

    # Guardar el PDF y devolver la respuesta
    pdf.save()

    return response

def export_pdf_report_inve(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Inventory_report.pdf"'
    pdf = canvas.Canvas(response, pagesize=landscape(letter))
    image_path = 'static/Imagenes/logito.jpg'   
    pdf.drawImage(image_path, x=20, y=550, width=200, height=50)
    col_widths = [pdf.stringWidth(field.verbose_name, 'Helvetica', 10) + 35 for field in Inventory._meta.fields]
    row_height = 16  
    table_width = sum(col_widths)
    table_height = row_height * 2
    x = 50
    y = pdf._pagesize[1] - 120  
    text_y = y + (row_height / 2) - 4
    pdf.setFillColor(colors.HexColor('#2d7da5'))  # Azul
    pdf.setStrokeColor(colors.black)
    pdf.setLineWidth(1)
    pdf.rect(x, y, table_width, row_height, fill=True)
    pdf.setFont("Helvetica-Bold", 10) 
    for i, width in enumerate(col_widths, start=1):
        pdf.line(x + sum(col_widths[:i]), y, x + sum(col_widths[:i]), y - table_height)
    for i, field in enumerate(Inventory._meta.fields):
        pdf.setFillColor(colors.white)
        text_width = pdf.stringWidth(field.verbose_name, 'Helvetica', 10)
        text_x = x + sum(col_widths[:i]) + (col_widths[i] - text_width) / 2
        pdf.drawString(text_x, text_y, field.verbose_name)
        pdf.setFillColor(colors.black) 

    for i, width in enumerate(col_widths, start=1):
        pdf.line(x + sum(col_widths[:i]), y, x + sum(col_widths[:i]), y - table_height)
    inventorys = Inventory.objects.all()
    pdf.setFont("Helvetica", 10) 
    for inventory in inventorys:
        y -= row_height
        for i, field in enumerate(Inventory._meta.fields):
            value = str(getattr(inventory, field.name))
            text_width = pdf.stringWidth(value[:15], 'Helvetica', 10)
            text_x = x + sum(col_widths[:i]) + (col_widths[i] - text_width) / 2
            pdf.drawString(text_x, y, value[:15])  
    pdf.showPage()
    pdf.save()
    return response

def export_pdf_report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="client_report.pdf"'
    pdf = canvas.Canvas(response, pagesize=landscape(letter))
    image_path = 'static/Imagenes/logito.jpg'   
    pdf.drawImage(image_path, x=20, y=550, width=200, height=50)
    col_widths = [pdf.stringWidth(field.verbose_name, 'Helvetica', 10) + 35 for field in Client._meta.fields]
    row_height = 16  
    table_width = sum(col_widths)
    table_height = row_height * 2
    x = 50
    y = pdf._pagesize[1] - 120  
    text_y = y + (row_height / 2) - 4
    pdf.setFillColor(colors.HexColor('#2d7da5'))  # Azul
    pdf.setStrokeColor(colors.black)
    pdf.setLineWidth(1)
    pdf.rect(x, y, table_width, row_height, fill=True)
    pdf.setFont("Helvetica-Bold", 10) 
    for i, width in enumerate(col_widths, start=1):
        pdf.line(x + sum(col_widths[:i]), y, x + sum(col_widths[:i]), y - table_height)
    for i, field in enumerate(Client._meta.fields):
        pdf.setFillColor(colors.white)
        text_width = pdf.stringWidth(field.verbose_name, 'Helvetica', 10)
        text_x = x + sum(col_widths[:i]) + (col_widths[i] - text_width) / 2
        pdf.drawString(text_x, text_y, field.verbose_name)
        pdf.setFillColor(colors.black) 

    for i, width in enumerate(col_widths, start=1):
        pdf.line(x + sum(col_widths[:i]), y, x + sum(col_widths[:i]), y - table_height)
    clients = Client.objects.all()
    pdf.setFont("Helvetica", 10) 
    for client in clients:
        y -= row_height
        for i, field in enumerate(Client._meta.fields):
            value = str(getattr(client, field.name))
            text_width = pdf.stringWidth(value[:15], 'Helvetica', 10)
            text_x = x + sum(col_widths[:i]) + (col_widths[i] - text_width) / 2
            pdf.drawString(text_x, y, value[:15])  
    pdf.showPage()
    pdf.save()
    return response

def store_cliente(request):
    if request.method == "POST":
        # Obtén los datos del formulario POST
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        numero = request.POST.get("numero")
        direccion = request.POST.get("direccion")
        fecha = request.POST.get("fecha")
        email = request.POST.get("email")

        # Crea una nueva instancia de Client con los datos recibidos
        nuevo_cliente = Client(
            name_client=nombre,
            last_name_client=apellido,
            cell_number=numero,
            address=direccion,
            date=fecha,
            email=email,
        )
        # Guarda el nuevo cliente en la base de datos
        nuevo_cliente.save()

        # Envío del correo de confirmación
        subject = 'Confirmación de Cita'
        message = f'Gracias por confirmar su cita. Su cita está programada para el {fecha}. Esperamos verte pronto.\nFecha de la cita y hora:{fecha}'
        from_email = settings.EMAIL_HOST_USER
        to_email = email  # Utiliza el correo del cliente como destinatario

        # Puedes usar un template de correo HTML para un formato más sofisticado
        html_message = render_to_string('confirmar_cita_email.html', {'message': message})

        send_mail(subject, message, from_email, [to_email], html_message=html_message)


        # Redirige a una página de éxito o a donde desees
        return HttpResponseRedirect("/servicios/")

    # Si no es una solicitud POST, renderiza la página del formulario
    return render(request, "servicios.html")

def store_cliente_juridica(request):
    if request.method == "POST":
        # Obtén los datos del formulario POST
        razonSocial = request.POST.get("razonSocial")
        nit = request.POST.get("nit")
        numero = request.POST.get("numero")
        direccion = request.POST.get("direccion")
        fecha = request.POST.get("fecha")
        email = request.POST.get("email")

        # Crea una nueva instancia de Client con los datos recibidos
        nuevo_cliente = LegalClient(
            registered_name=razonSocial,
            nit=nit,
            cell_number=numero,
            address=direccion,
            date=fecha,
            email=email,
        
           
        )

        # Guarda el nuevo cliente en la base de datos
        nuevo_cliente.save()
        # Envío del correo de confirmación
        subject = 'Confirmación de Cita'
        message = f'Gracias por confirmar su cita. Su cita está programada para el {fecha}. Esperamos verte pronto.\nFecha de la cita y hora:{fecha}'
        from_email = settings.EMAIL_HOST_USER
        to_email = email  # Utiliza el correo del cliente como destinatario

        # Puedes usar un template de correo HTML para un formato más sofisticado
        html_message = render_to_string('confirmar_cita_email.html', {'message': message})

        send_mail(subject, message, from_email, [to_email], html_message=html_message)

        # Redirige a una página de éxito o a donde desees
        return HttpResponseRedirect("/servicios/")

    # Si no es una solicitud POST, renderiza la página del formulario
    return render(request, "servicios.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Bienvenido {}".format(user.username))
            return redirect("admin:index")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "inicio.html", {})

def logout_view(request):
    logout(request)
    messages.success(request, "Sesión finalizada")
    return redirect("inicio")

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inicio")
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, "crearCuenta.html", {"form": form})


