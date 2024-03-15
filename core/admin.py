from django.contrib import admin, messages
from import_export import resources
from core.forms import FielTrialForm
from reportlab.lib import colors
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from import_export.admin import ImportExportModelAdmin
from . models import Escarificacion, Client, FielTrial, LaboratoryTrial, Inventory, LegalClient,LaboratoryWorker, Category, Engineer, SoilAnalysis, SoilCompactionTest, ResistanceTest, TestPermeability, PetrographicAnalysis
import math

# admin.site.register(Client)
# admin.site.register(FielTrial)
# admin.site.register(LaboratoryTrial)
# admin.site.register(Inventory)
# admin.site.register(Payments)

@admin.register(Client)
class ClientAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name_client', 'cell_number', 'date', 'email') 

class ClientResource(resources.ModelResource):
    class Meta:
        model = Client
        fields = ('name_client', 'cell_number', 'date', 'email')  
        export_order = ('name_client', 'cell_number', 'date', 'email')



@admin.register(LegalClient)
class LegalClientAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('registered_name', 'nit', 'cell_number', 'date', 'email')  

class LegalClientResource(resources.ModelResource):
    class Meta:
        model = LegalClient
        fields = ('registered_name', 'nit', 'cell_number', 'date', 'email')  
        export_order = ('registered_name', 'nit', 'cell_number', 'date', 'email')


@admin.register(FielTrial)
class FielTrialAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    form = FielTrialForm
    list_display= ('engineer_name', 'engineer_name', 'get_client_with_type', 'TypeOfTest_es', 'date')
    list_display_links= ('engineer_name', 'engineer_name', 'get_client_with_type', 'TypeOfTest_es', 'date') 
    search_fields= ('engineer_name',)
    list_per_page = 5

    def response_add(self, request, obj, post_url_continue=None):
        self.message_user(request, "El correo electrónico ha sido enviado exitosamente al cliente.", level=messages.SUCCESS)
        return super().response_add(request, obj, post_url_continue)
    
    def get_client(self, obj):
        if obj.natural_client:
            return obj.natural_client
        elif obj.legal_client:
            return obj.legal_client
        else:
            return None
        
    def get_client_with_type(self, obj):
        client = self.get_client(obj)
        if obj.natural_client:
            return f'{client} (N)'
        elif obj.legal_client:
            return f'{client} (J)'
        else:
            return None
        
    get_client_with_type.short_description = 'Cliente'


class FielTrialResource(resources.ModelResource):
     class Meta:
          model = FielTrial
          fields = ('engineer_name', 'client_name')
          export_order = ('engineer_name', 'TypeOfTest_es', 'client_name')
     

@admin.register(Inventory)
class InventoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('product_name_invent','amount_invent', 'category_name', 'image_invent')
    list_display_links = ('product_name_invent',)


class InventoryResource(resources.ModelResource):
    class Meta:
        model = Inventory
        fields = ('amount_invent','category_name', 'product_name_invent')
        export_order = ('amount_invent', 'category_name', 'description_invent', 'product_name_invent')


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('category_name', 'category_description')
    list_display_links = ('category_name',)


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('category_name','category_description')
        export_order = ('category_name')




# @admin.register(Resource)
# class ResourceAdmin(admin.ModelAdmin):
#      list_display = ('resource_name', 'resource_description', 'resource_amount', 'type',)
#      list_display_links= ('type',) 
#      search_fields = ('type',)
#      list_filter = ('resource_name',)

# @admin.register(Machinery)
# class MachineryAdmin(admin.ModelAdmin):
#      list_display = ('machine_name', 'machine_description', 'machine_state', 'type',)
#      list_display_links= ('machine_name',) 
#      search_fields = ('machine_name',)
#      list_filter = ('machine_name',)

# @admin.register(Material)
# class MaterialAdmin(admin.ModelAdmin):
#      list_display = ('material_name', 'material_description', 'material_amount', 'type',)
#      list_display_links= ('material_name',) 
#      search_fields = ('material_name',)
#      list_filter = ('material_name',)


@admin.register(Engineer)
class EngineerAdmin(admin.ModelAdmin):
    list_display = ('engineer_na', 'role',)
    list_display_links = ('engineer_na',) 
    search_fields = ('role', 'engineer_na',)
    list_filter = ('engineer_na',)

@admin.register(Escarificacion)
class EscarificacionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('get_client_with_type', 'sampling_date', 'location', 'approval_status')
    list_display_links = ('get_client_with_type',)
    search_fields = ('location', 'natural_client',)
    list_filter = ('natural_client',)
    list_per_page = 10
    actions = ['generate_pdf']

    fieldsets = (
        ('Información del Cliente', {
            'fields': ('natural_client', 'legal_client', 'engineer_name', 'test_number', 'sampling_date', 'location', 'city')
        }),
        ('Profundidad Muestra 1', {
            'fields': ('depth_1', 'depth_sample_1', 'color', 'texture_sample_1', 'sample_1_structure', 'sample_1_porosity', 'sample_1_apparent_density', 'ph_sample_1', 'sample_1_organic_matter'),
        }),
        ('Profundidad Muestra 2', {
            'fields': ('depth_2', 'depth_sample_2', 'texture_sample_2', 'sample_2_structure', 'sample_2_porosity', 'sample_2_apparent_density', 'ph_sample_2', 'sample_2_organic_matter'),
        }),
        ('Análisis de Nutrientes', {
            'fields': ('sample_nu',),
        }),
        ('Conclusiones y Recomendaciones', {
            'fields': ('conclusions_recommendations', 'approval_status'),
        }),
    )

    def get_client(self, obj):
        if obj.natural_client:
            return obj.natural_client
        elif obj.legal_client:
            return obj.legal_client
        else:
            return None

    def get_client_with_type(self, obj):
        client = self.get_client(obj)
        if obj.natural_client:
            return f'{client} (N)'
        elif obj.legal_client:
            return f'{client} (J)'
        else:
            return None

    get_client_with_type.short_description = 'Cliente'

    def generate_pdf(self, request, queryset):
        # Definir el nombre de los campos en español
        field_names = {
            "test_number": "Número de Prueba",
            "natural_client": "Cliente Natural",
            "legal_client": "Cliente Jurídico",
            "location": "Ubicación del Sitio",
            "sampling_date": "Fecha de Muestreo",
            "depth_1": "Numero de profundidad",
            "depth_sample_1": "Tipo de profundidad",
            "color": "Color",
            "texture_sample_1": "Textura del Suelo",
            "sample_1_structure": "Estructura de la Muestra 1",
            "sample_1_porosity": "Porosidad de la Muestra 1 (%)",
            "sample_1_apparent_density": "Densidad Aparente de la Muestra 1",
            "ph_sample_1": "pH Muestra 1",
            "sample_1_organic_matter": "Materia Orgánica de la Muestra 1",
            "depth_2": "Numero de profundidad",
            "depth_sample_2": "Tipo de profundidad",
            "texture_sample_2": "Textura del Suelo",
            "sample_2_structure": "Estructura de la Muestra",
            "sample_2_porosity": "Porosidad de la Muestra 2",
            "sample_2_apparent_density": "Densidad Aparente de la Muestra 2",
            "ph_sample_2": "pH Muestra 2",
            "sample_2_organic_matter": "Materia Orgánica de la Muestra 2",
            "sample_nu": "Análisis de Nutrientes",
            "conclusions_recommendations": "Conclusiones y Recomendaciones",
            "approval_status": "Estado de Aprobación"
        }

        # Crear la respuesta HTTP y el objeto PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="escarificacion.pdf"'

        # Crear el documento PDF
        pdf = canvas.Canvas(response, pagesize=letter)
        pdf.setTitle("Informe de Escarificacion")

        # Logo
        image_path = 'static/Imagenes/logito.jpg'
        pdf.drawImage(image_path, x=50, y=750, width=200, height=50)

        # Título
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, 700, "Pruebas de Escarificacion")

        # Separador
        pdf.line(50, 690, 550, 690)

        # Coordenadas iniciales
        x = 50
        y = 650

        # Espacio entre líneas
        line_height = 20

        # Encabezados de tabla
        headers = ["Campo", "Valor"]

        # Color de fondo para los encabezados
        pdf.setFillColor(colors.HexColor('#2d7da5'))  # Azul
        pdf.rect(x, y, 200, line_height, fill=True)
        pdf.rect(x + 200, y, 350, line_height, fill=True)

        # Color de texto para los encabezados
        pdf.setFillColor(colors.white)
        pdf.setFont("Helvetica-Bold", 12)

        # Dibujar encabezados
        pdf.drawString(x + 20, y + 4, headers[0])
        pdf.drawString(x + 200 + 20, y + 4, headers[1])

        # Restaurar color de texto
        pdf.setFillColor(colors.black)

        # Datos
        pdf.setFont("Helvetica", 10)

        for obj in queryset:
            for field, name in field_names.items():
                # Obtener el valor del campo
                field_value = str(getattr(obj, field))

                # Calcular la altura necesaria para el texto
                text_height = pdf.stringWidth(field_value, "Helvetica", 10)
                num_lines = max(1, int(math.ceil(text_height / (350 - 20))))  # 350 es el ancho del cuadro

                # Ajustar la posición Y si se necesita más espacio
                if y - num_lines * line_height < 50:  # 50 es la posición Y mínima
                    pdf.showPage()  # Cambiar de página
                    y = 750  # Restablecer la posición Y inicial

                # Dibujar cuadro alrededor del campo
                pdf.rect(x, y - num_lines * line_height, 200, num_lines * line_height, stroke=True)
                pdf.rect(x + 200, y - num_lines * line_height, 350, num_lines * line_height, stroke=True)

                # Escribir el nombre del campo
                pdf.drawString(x + 5, y - 10 - (num_lines - 1) * line_height, name)
                
                # Establecer el color de fondo dependiendo del campo
                if field == 'approval_status':
                    # Obtener el valor de visualización
                    field_value_display = dict(Escarificacion._meta.get_field(field).flatchoices).get(field_value)
                    field_value = field_value_display or field_value
                    
                    # Establecer el color de fondo de acuerdo al estado de aprobación
                    if field_value == 'Aprobado':
                        pdf.setFillColor(colors.green)
                    else:
                        pdf.setFillColor(colors.red)
                        
                    # Dibujar el color de fondo en el cuadro del texto
                    pdf.rect(x + 200, y - num_lines * line_height, 350, num_lines * line_height, fill=True)
                
                # Restaurar color de relleno a negro para el texto
                pdf.setFillColor(colors.black)
                
                # Escribir el valor del campo
                pdf.drawString(x + 200 + 5, y - 10 - (num_lines - 1) * line_height, field_value)

                # Actualizar la posición Y
                y -= num_lines * line_height

        # Guardar el PDF y devolver la respuesta
        pdf.save()

        return response

    generate_pdf.short_description = "Generar PDF"

class EscarificacionResource(resources.ModelResource):
    class Meta:
        model = Escarificacion
        fields = ('client_name', 'sampling_date', 'location', 'approval_status')
        export_order = ('client_name', 'sampling_date', 'location', 'approval_status')



@admin.register(SoilAnalysis)
class SoilAnalysisAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('get_client_with_type', 'sampling_date', 'location',)
    list_display_links = ('get_client_with_type',) 
    search_fields = ('location', 'natural_client',)
    list_filter = ('natural_client', 'legal_client',)
    list_per_page = 10
    actions = ['generate_pdf']

    fieldsets = (
        ('Información del Cliente', {
            'fields': ('natural_client', 'legal_client', 'engineer_name' , 'test_number', 'sampling_date', 'location')
        }),
        ('Propiedades del Suelo', {
            'fields': ('depth', 'texture', 'ph', 'organic_matter', 'cation_exchange_capacity')
        }),
        ('Análisis de Nutrientes', {
            'fields': ('total_nitrogen', 'available_phosphorus', 'available_potassium', 'iron', 'manganese', 'zinc')
        }),
        ('Conclusiones y Recomendaciones', {
            'fields': ('conclusions_recommendations', 'approval_status')
        }),
    )

    def get_client(self, obj):
        if obj.natural_client:
            return obj.natural_client
        elif obj.legal_client:
            return obj.legal_client
        else:
            return None

    def get_client_with_type(self, obj):
        client = self.get_client(obj)
        if obj.natural_client:
            return f'{client} (N)'
        elif obj.legal_client:
            return f'{client} (J)'
        else:
            return None
        
    get_client_with_type.short_description = 'Cliente'

    def generate_pdf(self, request, queryset):
        # Definir el nombre de los campos en español
        field_names = {
            "test_number": "Número de Prueba",
            "natural_client": "Cliente Natural",
            "legal_client": "Cliente Jurídico",
            "location": "Ubicación del Sitio",
            "sampling_date": "Fecha de la Prueba",
            "engineer_name": "Nombre Ingeniero",
            "depth": "Profundidad",
            "texture": "Tipo de Suelo",
            "ph": "pH del Suelo",
            "organic_matter": "Contenido de Humedad Natural",
            "cation_exchange_capacity": "Capacidad de Intercambio Catiónico",
            "total_nitrogen": "Nitrógeno Total",
            "available_phosphorus": "Fósforo Disponible",
            "available_potassium": "Potasio Disponible",
            "iron": "Hierro",
            "manganese": "Manganeso",
            "zinc": "Zinc",
            "conclusions_recommendations": "Conclusiones y Recomendaciones",
            "approval_status": "Estado de Aprobación"
        }

        # Crear la respuesta HTTP y el objeto PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="soil_analysis.pdf"'

        # Crear el documento PDF
        pdf = canvas.Canvas(response, pagesize=letter)
        pdf.setTitle("Informe de Analisis de Suelo")

        # Logo
        image_path = 'static/Imagenes/logito.jpg'
        pdf.drawImage(image_path, x=50, y=750, width=200, height=50)

        # Título
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, 700, "Anlisis de Suelo")

        # Separador
        pdf.line(50, 690, 550, 690)

        # Coordenadas iniciales
        x = 50
        y = 650

        # Espacio entre líneas
        line_height = 20

        # Encabezados de tabla
        headers = ["Campo", "Valor"]

        # Color de fondo para los encabezados
        pdf.setFillColor(colors.HexColor('#2d7da5'))  # Azul
        pdf.rect(x, y, 200, line_height, fill=True)
        pdf.rect(x + 200, y, 350, line_height, fill=True)

        # Color de texto para los encabezados
        pdf.setFillColor(colors.white)
        pdf.setFont("Helvetica-Bold", 12)

        # Dibujar encabezados
        pdf.drawString(x + 20, y + 4, headers[0])
        pdf.drawString(x + 200 + 20, y + 4, headers[1])

        # Restaurar color de texto
        pdf.setFillColor(colors.black)

        # Datos
        pdf.setFont("Helvetica", 10)

        for obj in queryset:
            for field, name in field_names.items():
                # Obtener el valor del campo
                field_value = str(getattr(obj, field))

                # Calcular la altura necesaria para el texto
                text_height = pdf.stringWidth(field_value, "Helvetica", 10)
                num_lines = max(1, int(math.ceil(text_height / (350 - 20))))  # 350 es el ancho del cuadro

                # Ajustar la posición Y si se necesita más espacio
                if y - num_lines * line_height < 50:  # 50 es la posición Y mínima
                    pdf.showPage()  # Cambiar de página
                    y = 750  # Restablecer la posición Y inicial

                # Dibujar cuadro alrededor del campo
                pdf.rect(x, y - num_lines * line_height, 200, num_lines * line_height, stroke=True)
                pdf.rect(x + 200, y - num_lines * line_height, 350, num_lines * line_height, stroke=True)

                # Escribir el nombre del campo
                pdf.drawString(x + 5, y - 10 - (num_lines - 1) * line_height, name)
                
                # Establecer el color de fondo dependiendo del campo
                if field == 'approval_status':
                    # Obtener el valor de visualización
                    field_value_display = dict(SoilAnalysis._meta.get_field(field).flatchoices).get(field_value)
                    field_value = field_value_display or field_value
                    
                    # Establecer el color de fondo de acuerdo al estado de aprobación
                    if field_value == 'Aprobado':
                        pdf.setFillColor(colors.green)
                    else:
                        pdf.setFillColor(colors.red)
                        
                    # Dibujar el color de fondo en el cuadro del texto
                    pdf.rect(x + 200, y - num_lines * line_height, 350, num_lines * line_height, fill=True)
                
                # Restaurar color de relleno a negro para el texto
                pdf.setFillColor(colors.black)
                
                # Escribir el valor del campo
                pdf.drawString(x + 200 + 5, y - 10 - (num_lines - 1) * line_height, field_value)

                # Actualizar la posición Y
                y -= num_lines * line_height

        # Guardar el PDF y devolver la respuesta
        pdf.save()

        return response

    generate_pdf.short_description = "Generar PDF"

@admin.register(SoilCompactionTest)
class SoilCompactionTestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('get_client_with_type', 'location', 'test_date', 'test_number')
    list_display_links = ('get_client_with_type',) 
    search_fields = ['location', 'engineer_name__name']
    list_filter = ['test_date']  # Aquí es donde se produjo el error
    list_per_page = 10
    actions = ['generate_pdf']

    fieldsets = (
        ('Información del Cliente', {
            'fields': ('natural_client', 'legal_client', 'engineer_name', 'test_number', 'test_date', 'location')
        }),
        ('Propiedades del Suelo', {
            'fields': ('soil_type', 'natural_moisture_content', 'compaction_equipment', 'number_of_passes', 'compaction_energy', 'adjustments_calibrations', 'max_dry_density', 'optimal_moisture_content', 'field_dry_density')
        }),
        ('Perfil de Compactación', {
            'fields': ('compaction_profile',)
        }),
        ('Resultados y Conclusiones', {
            'fields': ('results_conclusions', 'approval_status')
        }),
    )


    def get_client(self, obj):
        if obj.natural_client:
            return obj.natural_client
        elif obj.legal_client:
            return obj.legal_client
        else:
            return None

    def get_client_with_type(self, obj):
        client = self.get_client(obj)
        if obj.natural_client:
            return f'{client} (N)'
        elif obj.legal_client:
            return f'{client} (J)'
        else:
            return None
        
    get_client_with_type.short_description = 'Cliente'


    def generate_pdf(self, request, queryset):
        # Definir el nombre de los campos en español
        field_names = {
            "test_number": "Número de Prueba",
            "natural_client": "Cliente Natural",
            "legal_client": "Cliente Juridico",
            "location": "Ubicación del Sitio",
            "test_date": "Fecha de la Prueba",
            "engineer_name": "Nombre Ingeniero",
            "soil_type": "Tipo de Suelo",
            "natural_moisture_content": "Contenido de Humedad Natural (%)",
            "compaction_equipment": "Equipo Utilizado",
            "number_of_passes": "Número de Pasadas",
            "compaction_energy": "Energía de Compactación (%)",
            "adjustments_calibrations": "Ajustes/Calibraciones",
            "max_dry_density": "Densidad Seca Máxima (g/cm³)",
            "optimal_moisture_content": "Contenido de Humedad Óptimo (%)",
            "field_dry_density": "Densidad Seca en Campo (g/cm³)",
            "compaction_profile": "Perfil de Compactación",
            "results_conclusions": "Resultados y Conclusiones",
            "approval_status": "Estado de Aprobación"
        }

        # Crear la respuesta HTTP y el objeto PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="soil_compaction_test.pdf"'

        # Crear el documento PDF
        pdf = canvas.Canvas(response, pagesize=letter)
        pdf.setTitle("Informe de Pruebas de Compactacion")

        # Logo
        image_path = 'static/Imagenes/logito.jpg'
        pdf.drawImage(image_path, x=50, y=750, width=200, height=50)

        # Título
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, 700, "Pruebas de Compactacion")

        # Separador
        pdf.line(50, 690, 550, 690)

        # Coordenadas iniciales
        x = 50
        y = 650

        # Espacio entre líneas
        line_height = 20

        # Encabezados de tabla
        headers = ["Campo", "Valor"]

        # Color de fondo para los encabezados
        pdf.setFillColor(colors.HexColor('#2d7da5'))  # Azul
        pdf.rect(x, y, 200, line_height, fill=True)
        pdf.rect(x + 200, y, 350, line_height, fill=True)

        # Color de texto para los encabezados
        pdf.setFillColor(colors.white)
        pdf.setFont("Helvetica-Bold", 12)

        # Dibujar encabezados
        pdf.drawString(x + 20, y + 4, headers[0])
        pdf.drawString(x + 200 + 20, y + 4, headers[1])

        # Restaurar color de texto
        pdf.setFillColor(colors.black)

        # Datos
        pdf.setFont("Helvetica", 10)

        for obj in queryset:
            for field, name in field_names.items():
                # Obtener el valor del campo
                field_value = str(getattr(obj, field))

                # Calcular la altura necesaria para el texto
                text_height = pdf.stringWidth(field_value, "Helvetica", 10)
                num_lines = max(1, int(math.ceil(text_height / (350 - 20))))  # 350 es el ancho del cuadro

                # Ajustar la posición Y si se necesita más espacio
                if y - num_lines * line_height < 50:  # 50 es la posición Y mínima
                    pdf.showPage()  # Cambiar de página
                    y = 750  # Restablecer la posición Y inicial

                # Dibujar cuadro alrededor del campo
                pdf.rect(x, y - num_lines * line_height, 200, num_lines * line_height, stroke=True)
                pdf.rect(x + 200, y - num_lines * line_height, 350, num_lines * line_height, stroke=True)

                # Escribir el nombre del campo
                pdf.drawString(x + 5, y - 10 - (num_lines - 1) * line_height, name)
                
                # Establecer el color de fondo dependiendo del campo
                if field == 'approval_status':
                    # Obtener el valor de visualización
                    field_value_display = dict(SoilCompactionTest._meta.get_field(field).flatchoices).get(field_value)
                    field_value = field_value_display or field_value
                    
                    # Establecer el color de fondo de acuerdo al estado de aprobación
                    if field_value == 'Aprobado':
                        pdf.setFillColor(colors.green)
                    else:
                        pdf.setFillColor(colors.red)
                        
                    # Dibujar el color de fondo en el cuadro del texto
                    pdf.rect(x + 200, y - num_lines * line_height, 350, num_lines * line_height, fill=True)
                
                # Restaurar color de relleno a negro para el texto
                pdf.setFillColor(colors.black)
                
                # Escribir el valor del campo
                pdf.drawString(x + 200 + 5, y - 10 - (num_lines - 1) * line_height, field_value)

                # Actualizar la posición Y
                y -= num_lines * line_height

        # Guardar el PDF y devolver la respuesta
        pdf.save()

        return response

    generate_pdf.short_description = "Generar PDF"


     


#ADMIN LABORATORISTAAAA (5/5)
#
#
#
#
#
#PRUEBAS DE LABORATORIO
@admin.register(LaboratoryTrial)
class LaboratoryTrialAdmin(admin.ModelAdmin):
    list_display = ('laboratory_name', 'test_date', 'city', 'address')
    list_display_links = ('test_date',)
    search_fields = ('laboratory_name',)
    list_per_page = 5

    def response_add(self, request, obj, post_url_continue=None):
        self.message_user(request, "El correo electrónico ha sido enviado exitosamente al cliente.", level=messages.SUCCESS)
        return super().response_add(request, obj, post_url_continue)
    


#LABORATORISTAS
@admin.register(LaboratoryWorker)
class LaboratoryWorkerAdmin(admin.ModelAdmin):
     list_display = ('laboratory_name', 'rol',)
     list_display_links= ('laboratory_name',) 
     search_fields = ('rol', 'laboratory_name',)
     list_filter = ('laboratory_name',)
    

#PRUEBA DE RESISTENCIA #1
@admin.register(ResistanceTest)
class ResistanceTestAdmin(ImportExportModelAdmin):
    list_display = ('get_client_with_type', 'test_date', 'location_longitude',)
    list_display_links = ('get_client_with_type',) 
    search_fields = ('location_longitude', 'natural_client',)
    actions = ['generate_pdf']

    fieldsets = (
        ('Cliente', {
            'fields': ('natural_client', 'legal_client', 'NameLaboratory', 'test_number'),
        }),
        ('Detalles de la Prueba', {
            'fields': ('soil_type', 'sample_depth', 'location_latitude', 'location_longitude', 'test_date', 'test_method', 'procedure', 'permeability', 'hydraulic_conductivity', 'additional_comments', 'approval_status'),
        }),
    )

    def get_client(self, obj):
        if obj.natural_client:
            return obj.natural_client
        elif obj.legal_client:
            return obj.legal_client
        else:
            return None

    def get_client_with_type(self, obj):
        client = self.get_client(obj)
        if obj.natural_client:
            return f'{client} (N)'
        elif obj.legal_client:
            return f'{client} (J)'
        else:
            return None

    get_client_with_type.short_description = 'Cliente'

    def generate_pdf(self, request, queryset):
        # Definir el nombre de los campos en español
        field_names = {
            "test_number": "Numero de Prueba",
            "natural_client": "Cliente Natural",
            "legal_client": "Cliente Jurídico",
            "NameLaboratory": "Nombre Laboratorista",
            "soil_type": "Tipo de Suelo",
            "sample_depth": "Profundidad de la Muestra",
            "location_latitude": "Latitud",
            "location_longitude": "Longitud",
            "test_date": "Fecha de Prueba",
            "test_method": "Método de Prueba",
            "procedure": "Procedimiento",
            "permeability": "Permeabilidad",
            "hydraulic_conductivity": "Conductividad Hidráulica",
            "additional_comments": "Comentarios Adicionales",
            "approval_status": "Estado de Aprobación"
        }

        # Crear la respuesta HTTP y el objeto PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="resistance_tests.pdf"'

        # Crear el documento PDF
        pdf = canvas.Canvas(response, pagesize=letter)
        pdf.setTitle("Informe de Pruebas de Resistencia")

        # Logo
        image_path = 'static/Imagenes/logito.jpg'
        pdf.drawImage(image_path, x=50, y=750, width=200, height=50)

        # Título
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, 700, "Pruebas de Resistencia")

        # Separador
        pdf.line(50, 690, 550, 690)

        # Coordenadas iniciales
        x = 50
        y = 650

        # Espacio entre líneas
        line_height = 20

        # Encabezados de tabla
        headers = ["Campo", "Valor"]

        # Color de fondo para los encabezados
        pdf.setFillColor(colors.HexColor('#2d7da5'))  # Azul
        pdf.rect(x, y, 200, line_height, fill=True)
        pdf.rect(x + 200, y, 350, line_height, fill=True)

        # Color de texto para los encabezados
        pdf.setFillColor(colors.white)
        pdf.setFont("Helvetica-Bold", 12)

        # Dibujar encabezados
        pdf.drawString(x + 20, y + 4, headers[0])
        pdf.drawString(x + 200 + 20, y + 4, headers[1])

        # Restaurar color de texto
        pdf.setFillColor(colors.black)

        # Datos
        pdf.setFont("Helvetica", 10)

        for obj in queryset:
            for field, name in field_names.items():
                # Obtener el valor del campo
                field_value = str(getattr(obj, field))

                # Calcular la altura necesaria para el texto
                text_height = pdf.stringWidth(field_value, "Helvetica", 10)
                num_lines = max(1, int(math.ceil(text_height / (350 - 20))))  # 350 es el ancho del cuadro

                # Ajustar la posición Y si se necesita más espacio
                if y - num_lines * line_height < 50:  # 50 es la posición Y mínima
                    pdf.showPage()  # Cambiar de página
                    y = 750  # Restablecer la posición Y inicial

                # Dibujar cuadro alrededor del campo
                pdf.rect(x, y - num_lines * line_height, 200, num_lines * line_height, stroke=True)
                pdf.rect(x + 200, y - num_lines * line_height, 350, num_lines * line_height, stroke=True)

                # Escribir el nombre del campo
                pdf.drawString(x + 5, y - 10 - (num_lines - 1) * line_height, name)
                
                # Establecer el color de fondo dependiendo del campo
                if field == 'approval_status':
                    # Obtener el valor de visualización
                    field_value_display = dict(ResistanceTest._meta.get_field(field).flatchoices).get(field_value)
                    field_value = field_value_display or field_value
                    
                    # Establecer el color de fondo de acuerdo al estado de aprobación
                    if field_value == 'Aprobado':
                        pdf.setFillColor(colors.green)
                    else:
                        pdf.setFillColor(colors.red)
                        
                    # Dibujar el color de fondo en el cuadro del texto
                    pdf.rect(x + 200, y - num_lines * line_height, 350, num_lines * line_height, fill=True)
                
                # Restaurar color de relleno a negro para el texto
                pdf.setFillColor(colors.black)
                
                # Escribir el valor del campo
                pdf.drawString(x + 200 + 5, y - 10 - (num_lines - 1) * line_height, field_value)

                # Actualizar la posición Y
                y -= num_lines * line_height

        # Guardar el PDF y devolver la respuesta
        pdf.save()

        return response

    generate_pdf.short_description = "Generar PDF"
#
#
#
#
#
#
#PRUEBA DE PERMEABILIAD 2
    
@admin.register(TestPermeability)
class TestPermeabilityAdmin(ImportExportModelAdmin):
    list_display = ('get_client_with_type', 'test_number', 'test_date')
    search_fields = ('get_client_with_type', 'test_number',)
    list_filter = ('test_date',)
    actions = ['generate_pdf']

    fieldsets = (
        ('Información General', {
            'fields': ('natural_client', 'legal_client', 'test_number', 'test_date', 'NameLaboratory'),
        }),
        ('Características del Suelo', {
            'fields': ('soil_type', 'grain_size', 'soil_porosity', 'soil_compaction'),
        }),
        ('Condiciones de Prueba', {
            'fields': ('soil_temperature', 'soil_moisture_content', 'hydrostatic_pressure', 'loading_conditions', 'drainage_conditions', 'soil_chemistry'),
        }),
        ('Resultados de la Prueba', {
            'fields': ('permeability_velocity', 'intrinsic_permeability', 'permeability_coefficient'),
        }),
        ('Observaciones y Conclusiones', {
            'fields': ('observations', 'conclusions', 'approval_status'),
        }),
    )


    def get_client(self, obj):
        if obj.natural_client:
            return obj.natural_client
        elif obj.legal_client:
            return obj.legal_client
        else:
            return None
        
    def get_client_with_type(self, obj):
        client = self.get_client(obj)
        if obj.natural_client:
            return f'{client} (N)'
        elif obj.legal_client:
            return f'{client} (J)'
        else:
            return None
        
    get_client_with_type.short_description = 'Cliente'

    def generate_pdf(self, request, queryset):
    # Definir el nombre de los campos en español
        field_names = {
            "natural_client": "Cliente Natural",
            "legal_client": "Cliente Jurídico",
            "test_number": "Número de Prueba",
            "test_date": "Fecha de Prueba",
            "NameLaboratory": "Nombre del Laboratorista",
            "soil_type": "Tipo de Suelo",
            "grain_size": "Tamaño de Grano",
            "soil_porosity": "Porosidad del Suelo",
            "soil_compaction": "Compactación del Suelo",
            "soil_temperature": "Temperatura del Suelo",
            "soil_moisture_content": "Contenido de Humedad del Suelo",
            "hydrostatic_pressure": "Presión Hidrostática",
            "loading_conditions": "Condiciones de Carga",
            "drainage_conditions": "Condiciones de Drenaje",
            "soil_chemistry": "Química del Suelo",
            "permeability_velocity": "Velocidad de Permeabilidad",
            "intrinsic_permeability": "Permeabilidad Intrínseca",
            "permeability_coefficient": "Coeficiente de Permeabilidad",
            "observations": "Observaciones",
            "conclusions": "Conclusiones",
            "approval_status": "Estado de Aprobación"
        }

        # Crear la respuesta HTTP y el objeto PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="resistance_tests.pdf"'

        # Crear el documento PDF
        pdf = canvas.Canvas(response, pagesize=letter)
        pdf.setTitle("Informe de Pruebas de Permeabilidad")

        # Logo
        image_path = 'static/Imagenes/logito.jpg'
        pdf.drawImage(image_path, x=50, y=750, width=200, height=50)

        # Título
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, 700, "Pruebas de Permeabilidad")

        # Separador
        pdf.line(50, 690, 550, 690)

        # Coordenadas iniciales
        x = 50
        y = 650

        # Espacio entre líneas
        line_height = 20

        # Encabezados de tabla
        headers = ["Campo", "Valor"]

        # Color de fondo para los encabezados
        pdf.setFillColor(colors.HexColor('#2d7da5'))  # Azul
        pdf.rect(x, y, 200, line_height, fill=True)
        pdf.rect(x + 200, y, 350, line_height, fill=True)

        # Color de texto para los encabezados
        pdf.setFillColor(colors.white)
        pdf.setFont("Helvetica-Bold", 12)

        # Dibujar encabezados
        pdf.drawString(x + 20, y + 4, headers[0])
        pdf.drawString(x + 200 + 20, y + 4, headers[1])

        # Restaurar color de texto
        pdf.setFillColor(colors.black)

        # Datos
        pdf.setFont("Helvetica", 10)

        for obj in queryset:
            for field, name in field_names.items():
                # Obtener el valor del campo
                field_value = str(getattr(obj, field))

                # Calcular la altura necesaria para el texto
                text_height = pdf.stringWidth(field_value, "Helvetica", 10)
                num_lines = max(1, int(math.ceil(text_height / (350 - 20))))  # 350 es el ancho del cuadro

                # Ajustar la posición Y si se necesita más espacio
                if y - num_lines * line_height < 50:  # 50 es la posición Y mínima
                    pdf.showPage()  # Cambiar de página
                    y = 750  # Restablecer la posición Y inicial

                # Dibujar cuadro alrededor del campo
                pdf.rect(x, y - num_lines * line_height, 200, num_lines * line_height, stroke=True)
                pdf.rect(x + 200, y - num_lines * line_height, 350, num_lines * line_height, stroke=True)

                # Escribir el nombre del campo
                pdf.drawString(x + 5, y - 10 - (num_lines - 1) * line_height, name)
                
                # Establecer el color de fondo dependiendo del campo
                if field == 'approval_status':
                    # Establecer el color de fondo de acuerdo al estado de aprobación
                    if field_value == 'Aprobado':
                        pdf.setFillColor(colors.green)
                    else:
                        pdf.setFillColor(colors.red)
                    # Dibujar el color de fondo en el cuadro del texto
                    pdf.rect(x + 200, y - num_lines * line_height, 350, num_lines * line_height, fill=True)
                
                # Restaurar color de relleno a negro para el texto
                pdf.setFillColor(colors.black)
                
                # Escribir el valor del campo
                pdf.drawString(x + 200 + 5, y - 10 - (num_lines - 1) * line_height, field_value)

                # Actualizar la posición Y
                y -= num_lines * line_height

        # Guardar el PDF y devolver la respuesta
        pdf.save()

        return response

    generate_pdf.short_description = "Generar PDF"
#
#
#
#
#
#
#PRUEBA DE ANALISIS PETROGRAFICO 3

@admin.register(PetrographicAnalysis)
class PetrographicAnalysisAdmin(ImportExportModelAdmin):
    list_display = ('get_client_with_type', 'test_number', 'test_date')
    search_fields = ('get_client_with_type', 'test_number',)
    list_filter = ('test_date',)
    actions = ['generate_pdf']

    fieldsets = (
        ('Información General', {
            'fields': ('natural_client', 'legal_client', 'test_number', 'test_date', 'name_laboratory'),
        }),
        ('Descripción de la Muestra', {
            'fields': ('sample_description',),
        }),
        ('Características Petrográficas', {
            'fields': ('mineral_composition', 'grain_size_distribution', 'texture', 'porosity', 'cementation'),
        }),
        ('Resultados de Análisis', {
            'fields': ('mineral_identification', 'mineral_quantification', 'rock_type', 'color'),
        }),
        ('Conclusiones', {
            'fields': ('conclusions', 'approval_status'),
        }),
    )

    def get_client(self, obj):
        if obj.natural_client:
            return obj.natural_client
        elif obj.legal_client:
            return obj.legal_client
        else:
            return None
        
    def get_client_with_type(self, obj):
        client = self.get_client(obj)
        if obj.natural_client:
            return f'{client} (N)'
        elif obj.legal_client:
            return f'{client} (J)'
        else:
            return None
        
    get_client_with_type.short_description = 'Cliente'

    def generate_pdf(self, request, queryset):
    # Definir el nombre de los campos en español
        field_names = {
            "natural_client": "Cliente Natural",
            "legal_client": "Cliente Jurídico",
            "test_number": "Número de Prueba",
            "test_date": "Fecha de Prueba",
            "name_laboratory": "Nombre del Laboratorista",
            "sample_description": "Descripción de la Muestra",
            "mineral_composition": "Composición Mineral",
            "grain_size_distribution": "Distribución del Tamaño de Grano",
            "texture": "Textura",
            "porosity": "Porosidad",
            "cementation": "Cementación",
            "mineral_identification": "Identificación Mineral",
            "mineral_quantification": "Cuantificación Mineral",
            "rock_type": "Tipo de Roca",
            "color": "Color",
            "conclusions": "Conclusiones",
            "approval_status": "Estado de Aprobación"
        }

        # Crear la respuesta HTTP y el objeto PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="petrographic_analysis.pdf"'

        # Crear el documento PDF
        pdf = canvas.Canvas(response, pagesize=letter)
        pdf.setTitle("Informe Analisis Petrografico")

        # Logo
        image_path = 'static/Imagenes/logito.jpg'
        pdf.drawImage(image_path, x=50, y=750, width=200, height=50)

        # Título
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, 700, "Analisis Petrografico")

        # Separador
        pdf.line(50, 690, 550, 690)

        # Coordenadas iniciales
        x = 50
        y = 650

        # Espacio entre líneas
        line_height = 20

        # Encabezados de tabla
        headers = ["Campo", "Valor"]

        # Color de fondo para los encabezados
        pdf.setFillColor(colors.HexColor('#2d7da5'))  # Azul
        pdf.rect(x, y, 200, line_height, fill=True)
        pdf.rect(x + 200, y, 350, line_height, fill=True)

        # Color de texto para los encabezados
        pdf.setFillColor(colors.white)
        pdf.setFont("Helvetica-Bold", 12)

        # Dibujar encabezados
        pdf.drawString(x + 20, y + 4, headers[0])
        pdf.drawString(x + 200 + 20, y + 4, headers[1])

        # Restaurar color de texto
        pdf.setFillColor(colors.black)

        # Datos
        pdf.setFont("Helvetica", 10)

        for obj in queryset:
            for field, name in field_names.items():
                # Obtener el valor del campo
                field_value = str(getattr(obj, field))

                # Calcular la altura necesaria para el texto
                text_height = pdf.stringWidth(field_value, "Helvetica", 10)
                num_lines = max(1, int(math.ceil(text_height / (350 - 20))))  # 350 es el ancho del cuadro

                # Ajustar la posición Y si se necesita más espacio
                if y - num_lines * line_height < 50:  # 50 es la posición Y mínima
                    pdf.showPage()  # Cambiar de página
                    y = 750  # Restablecer la posición Y inicial

                # Dibujar cuadro alrededor del campo
                pdf.rect(x, y - num_lines * line_height, 200, num_lines * line_height, stroke=True)
                pdf.rect(x + 200, y - num_lines * line_height, 350, num_lines * line_height, stroke=True)

                # Escribir el nombre del campo
                pdf.drawString(x + 5, y - 10 - (num_lines - 1) * line_height, name)
                
                # Establecer el color de fondo dependiendo del campo
                if field == 'approval_status':
                    # Establecer el color de fondo de acuerdo al estado de aprobación
                    if field_value == 'Aprobado':
                        pdf.setFillColor(colors.green)
                    else:
                        pdf.setFillColor(colors.red)
                    # Dibujar el color de fondo en el cuadro del texto
                    pdf.rect(x + 200, y - num_lines * line_height, 350, num_lines * line_height, fill=True)
                
                # Restaurar color de relleno a negro para el texto
                pdf.setFillColor(colors.black)
                
                # Escribir el valor del campo
                pdf.drawString(x + 200 + 5, y - 10 - (num_lines - 1) * line_height, field_value)

                # Actualizar la posición Y
                y -= num_lines * line_height

        # Guardar el PDF y devolver la respuesta
        pdf.save()

        return response

    generate_pdf.short_description = "Generar PDF"
