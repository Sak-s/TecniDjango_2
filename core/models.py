from django.db import models
from datetime import datetime, timedelta
from django.utils.html import format_html
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.core.validators import EmailValidator
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.validators import FileExtensionValidator





class Client(models.Model):
    name_client = models.TextField(max_length=100, verbose_name="Nombre Cliente")
    last_name_client = models.TextField(max_length=100, verbose_name="Apellido Cliente")
    cell_number = models.BigIntegerField(verbose_name="Celular Cliente")
    address = models.TextField(max_length=200,verbose_name="Direccion Cliente")
    date = models.DateTimeField(default=datetime.now, verbose_name='Fecha Cita')
    email = models.EmailField(max_length=200,verbose_name="Correo Cliente")
    
    
    
    def __str__(self):
        return self.name_client
    
    class Meta:
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        db_table = "cliente_natural"
        ordering = ['id']

    
class LegalClient(models.Model):
    registered_name = models.TextField(max_length=100, verbose_name="Nombre Cliente")
    nit = models.BigIntegerField( verbose_name="NIT Cliente")
    cell_number = models.BigIntegerField(verbose_name="Celular Cliente")
    address = models.TextField(max_length=200,verbose_name="Direccion Cliente")
    date = models.DateTimeField(default=datetime.now, verbose_name='Fecha Cita')
    email = models.EmailField(max_length=200,verbose_name="Correo Cliente")
    
    
    
    def __str__(self):
        return self.registered_name
    
    class Meta:
        verbose_name = "ClienteJuridico"
        verbose_name_plural = "Clientes Juridicos"
        db_table = "cliente_juridico"
        ordering = ['id']

class Engineer(models.Model):

    ENGINEER_CAMPO = 'CA'
    ENGINEER_AUXILIAR = 'AX'
    
    ENGINEER_CHOICES = [
        (ENGINEER_CAMPO, 'Ingeniero de Campo'),
        (ENGINEER_AUXILIAR, 'Ingeniero Auxialiar'),  
    ]
    
    engineer_na = models.CharField(max_length=100, verbose_name="Nombre Ingeniero")
    email = models.EmailField(verbose_name="Correo Electrónico", unique=True, validators=[EmailValidator(message="Debe ingresar un correo electrónico válido.")])
    cell_number = models.CharField(max_length=20, verbose_name="Número de Teléfono", validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El número de celular debe tener más de 10 dígitos")])
    nit = models.CharField(max_length=20, verbose_name="Nit", unique=True, validators=[RegexValidator(regex=r'^\d{9,15}$', message="El nit debe contener entre 9 y 15 dígitos.")])
    role = models.CharField(max_length=3, choices=ENGINEER_CHOICES, verbose_name="Tipo de Ingeniero")

    def __str__(self):
        return self.engineer_na

    class Meta:
        verbose_name = "Ingeniero"
        verbose_name_plural = "Ingenieros"
        db_table = "ingenieros"
        ordering = ['id']

class Escarificacion(models.Model):
    PROFUNDIDAD_CHOICES = [
        ('cm', 'Centímetros'),
        ('m', 'Metros'),
    ]
    TEXTURA_CHOICES = [
        ('limosa', 'Limosa'),
        ('sólida', 'Sólida'),
        ('arcilla_húmeda', 'Arcilla Húmeda'),
        ('arena', 'Arena'),
    ]

    PH_CHOICES = [
        ('acido', 'Ácido'),
        ('lig_acido', 'Ligeramente Ácido'),
        ('neutro', 'Neutro'),
    ]
    NU_CHOICES = [
        ('nitrogeno', 'Nitrógeno'),
        ('fosforo', 'Fósforo'),
        ('potasio', 'Potasio'),
    ]
    COLORS_CHOICES = [
        ('marron_oscuro', 'Marrón oscuro'),
        ('marron_claro', 'Marrón claro'),
        ('negro', 'Negro'),
        ('gris', 'Gris'),
    ]

    ES_CHOICES = [
        ('agregados_granulares', 'Agregados granulares'),
        ('agregados_bien_definidos', 'Agregados bien definidos'),
        ('agregados_estables', 'Agregados estables'),
        ('agregados_angulares', 'A gregados angulares'),
        ('agregados_moderadamente_estables', 'Agregados moderadamente estables'),
    ]

    COLOMBIAN_CITIES = [
        ('Bogotá', 'Bogotá'),
        ('Medellín', 'Medellín'),
        ('Cartagena', 'Cartagena'),
        ('Cali', 'Cali'),
        ('Santa Marta', 'Santa Marta'),
        ('Barranquilla', 'Barranquilla'),
        ('Villavicencio', 'Villavicencio'),
        ('San Gil', 'San Gil'),
        ('Bucaramanga', 'Bucaramanga'),
    ]
    APPROVAL_STATUS_CHOICES = [
        ('Aprobado', 'Aprobado'),
        ('No Aprobado', 'No Aprobado'),
    ]

    natural_client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente Natural', blank=True, null=True)
    legal_client = models.ForeignKey("LegalClient", verbose_name="Cliente Legal", on_delete=models.CASCADE, blank=True, null=True)
    test_number = models.IntegerField(verbose_name="Numero Prueba", unique=True)
    city = models.CharField(max_length=100, choices=COLOMBIAN_CITIES, verbose_name="Ciudad", default=COLOMBIAN_CITIES[0][0])
    engineer_name = models.ForeignKey(Engineer, on_delete=models.CASCADE, verbose_name="Nombre Ingeniero")
    location = models.CharField(max_length=100, verbose_name="Ubicación")
    sampling_date = models.DateField(verbose_name="Fecha de Muestreo",default=datetime.now)  
    depth_1 = models.CharField(max_length=10, verbose_name="Numero de profundidad (Muestra 1)")
    depth_sample_1 = models.CharField(max_length=10, choices=PROFUNDIDAD_CHOICES, verbose_name="Tipo de profundidad (Muestra 1)")
    color = models.CharField(max_length=50,choices=COLORS_CHOICES, verbose_name="Color")
    texture_sample_1 = models.CharField(max_length=20, choices=TEXTURA_CHOICES, verbose_name="Textura del Suelo - Muestra 1")
    sample_1_structure = models.CharField(max_length=100, choices=ES_CHOICES, verbose_name="Estructura de la Muestra 1")
    sample_1_porosity = models.FloatField(verbose_name="Porosidad de la Muestra 1 (%)")
    sample_1_apparent_density = models.FloatField(verbose_name="Densidad Aparente de la Muestra 1 ( g/cm³)")
    ph_sample_1 = models.CharField(max_length=20, choices=PH_CHOICES, verbose_name="pH Muestra 1")
    sample_1_organic_matter = models.FloatField(verbose_name="Materia Orgánica de la Muestra 1 (%)")
    
    depth_2 = models.CharField(max_length=10, verbose_name="Numero de profundidad (Muestra 2)")
    depth_sample_2 = models.CharField(max_length=10, choices=PROFUNDIDAD_CHOICES, verbose_name="Tipo de profundidad (Muestra 2)")
    texture_sample_2 = models.CharField(max_length=20, choices=TEXTURA_CHOICES, verbose_name="Textura del Suelo - Muestra 2")
    sample_2_structure = models.CharField(max_length=100, choices=ES_CHOICES, verbose_name="Estructura de la Muestra 2")
    sample_2_porosity = models.FloatField(verbose_name="Porosidad de la Muestra 2 (%)")
    sample_2_apparent_density = models.FloatField(verbose_name="Densidad Aparente de la Muestra 2 ( g/cm³)")
    ph_sample_2 = models.CharField(max_length=20, choices=PH_CHOICES, verbose_name="pH Muestra 2")
    sample_2_organic_matter = models.FloatField(verbose_name="Materia Orgánica de la Muestra 2 (%)")
    sample_nu = models.CharField(max_length=20, choices=NU_CHOICES, verbose_name="Análisis de Nutrientes (mg/kg)")
    conclusions_recommendations = models.TextField(verbose_name="Conclusiones y Recomendaciones")
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, verbose_name="Estado de Aprobación")

    def clean(self):
        super().clean()
        depth_1 = self.depth_1
        sampling_date = self.sampling_date
        depth_2 = self.depth_2

        # Validar el formato del valor de profundidad
        if not self.is_valid_depth(depth_1):
            raise ValidationError({'depth_1': "El formato de la profundidad no es válido. Utilice el formato '0-30', '30-60', etc."})
        
        if not self.is_valid_depth(depth_2):
            raise ValidationError({'depth_2': "El formato de la profundidad no es válido. Utilice el formato '0-30', '30-60', etc."})

        # Validar la fecha de muestreo
        if sampling_date and sampling_date < timezone.now().date():
            raise ValidationError({'sampling_date': "La fecha de muestreo no puede ser anterior a la fecha actual."})

        
        if self.test_number < 0:
            raise ValidationError("El número de prueba no puede ser negativo.")
        
        six_months_later = timezone.now() + timedelta(days=6*30)
        
        # Validar que la fecha de muestreo no esté programada para más de 6 meses en el futuro
        if self.sampling_date > six_months_later.date():
            raise ValidationError({'sampling_date': "La fecha de muestreo no puede ser más de 6 meses en el futuro."})


        if not self.is_valid_depth(depth_1):
            raise ValidationError({'depth_1': "El formato de la profundidad no es válido. Utilice el formato '0-30', '30-60', etc."})
        
        if not self.is_valid_depth(depth_2):
            raise ValidationError({'depth_2': "El formato de la profundidad no es válido. Utilice el formato '0-30', '30-60', etc."})

        if Escarificacion.objects.filter(sampling_date=self.sampling_date).exists():
            raise ValidationError({'sampling_date': "Ya existe una prueba para esta fecha."})
        
        if Escarificacion.objects.filter(test_number=self.test_number, natural_client=self.natural_client).exists():
            raise ValidationError({'test_number': "Ya existe un registro con este número de prueba para este cliente."})
        
        def is_valid_depth(self, value):
            try:
                depth = int(value.split('-')[0])  # Tomar solo el primer valor antes del guion
                assert depth >= 0, "El valor de profundidad debe ser un número entero positivo."
                return True
            except (ValueError, AssertionError):
                return False
            
        if self.legal_client and self.natural_client:
            raise ValidationError('Debe ingresar solo un cliente jurídico o natural, no ambos.')
        elif self.legal_client is None and self.natural_client is None:
            raise ValidationError('Debe ingresar al menos un cliente jurídico o natural.')



    @staticmethod
    def is_valid_depth(value):
    # Verificar si el valor tiene el formato adecuado (por ejemplo, '0-30')
        if '-' not in value:
            return False
        parts = value.split('-')
        if len(parts) != 2:
            return False
        try:
            start = int(parts[0])
            end = int(parts[1])
            # Verificar que los valores sean enteros positivos
            if start < 0 or end < 0:
                return False
            # Verificar que el rango sea válido
            if start >= end:
                return False
        except ValueError:
            return False
        return True

    def __str__(self):
        return f"Escarificación - {self.sampling_date}"

    class Meta:
        verbose_name = "Escarificación"
        verbose_name_plural = "Escarificaciones"
        db_table = "escarificacion"
        ordering = ['sampling_date']

class SoilAnalysis(models.Model):
    TEXTURE_CHOICES = [
        ('Franco-arcilloso', 'Franco-arcilloso'),
        ('Arcilloso', 'Arcilloso'),
        ('Arenoso', 'Arenoso'),
        ('Limoso', 'Limoso'),
    ]

    PH_CHOICES = [
        ('6.2', '6.2 unidades pH'),
        ('6.5', '6.5 unidades pH'),
        ('7.0', '7.0 unidades pH'),
    ]

    NU_CHOICES = [
        ('Nitrógeno', 'Nitrógeno'),
        ('Fósforo', 'Fósforo'),
        ('Potasio', 'Potasio'),
    ]

    APPROVAL_STATUS_CHOICES = [
        ('Aprobado', 'Aprobado'),
        ('No Aprobado', 'No Aprobado'),
    ]

    natural_client = models.ForeignKey("Client", verbose_name="Cliente Natural", on_delete=models.CASCADE, blank=True, null=True)
    legal_client = models.ForeignKey("LegalClient", verbose_name="Cliente Legal", on_delete=models.CASCADE, blank=True, null=True)
    test_number = models.IntegerField(verbose_name="Número Prueba", unique=True)
    location = models.CharField(max_length=100, verbose_name="Ubicación")
    sampling_date = models.DateField(verbose_name="Fecha de Muestreo", default=datetime.now)
    engineer_name = models.ForeignKey(Engineer, on_delete=models.CASCADE, verbose_name="Nombre Ingeniero")
    depth = models.CharField(max_length=10, verbose_name="Profundidad")
    texture = models.CharField(max_length=20, choices=TEXTURE_CHOICES, verbose_name="Textura del Suelo")
    ph = models.CharField(max_length=20, choices=PH_CHOICES, verbose_name="pH del Suelo")
    organic_matter = models.FloatField(verbose_name="Materia Orgánica (%)")
    cation_exchange_capacity = models.FloatField(verbose_name="Capacidad de Intercambio Catiónico (cmol/kg)")
    total_nitrogen = models.FloatField(verbose_name="Nitrógeno Total (kg/ha)")
    available_phosphorus = models.FloatField(verbose_name="Fósforo Disponible (ppm)")
    available_potassium = models.FloatField(verbose_name="Potasio Disponible (ppm)")
    iron = models.FloatField(verbose_name="Hierro (Fe) (ppm)")
    manganese = models.FloatField(verbose_name="Manganeso (Mn) (ppm)")
    zinc = models.FloatField(verbose_name="Zinc (Zn) (ppm)")
    conclusions_recommendations = models.TextField(verbose_name="Conclusiones y Recomendaciones")
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, verbose_name="Estado de Aprobación")


    def clean(self):
        super().clean()
        depth = self.depth


        if any(field_value < 0 for field_name, field_value in self.__dict__.items() if isinstance(field_value, (int, float))):
            raise ValidationError("Ningún campo de número puede ser negativo.")

        
        if SoilAnalysis.objects.filter(sampling_date=self.sampling_date).exists():
            raise ValidationError({'sampling_date': "Ya existe una prueba para esta fecha."})
        
        if SoilAnalysis.objects.filter(test_number=self.test_number, natural_client=self.natural_client).exists():
            raise ValidationError({'test_number': "Ya existe un registro con este número de prueba para este cliente."})
        
        if self.sampling_date and self.sampling_date < timezone.now().date():
            raise ValidationError({'sampling_date': "La fecha de muestreo no puede ser anterior a la fecha actual."})

        six_months_later = timezone.now() + timedelta(days=6*30)
        
        # Validar que la fecha de muestreo no esté programada para más de 6 meses en el futuro
        if self.sampling_date > six_months_later.date():
            raise ValidationError({'sampling_date': "La fecha de muestreo no puede ser más de 6 meses en el futuro."})
        
        if not SoilAnalysis.is_valid_depth(depth):
            raise ValidationError({'depth': "El formato de la profundidad no es válido. Utilice el formato '0-30', '30-60', etc."})
        
        def is_valid_depth(self, value):
            try:
                depth = int(value.split('-')[0])  # Tomar solo el primer valor antes del guion
                assert depth >= 0, "El valor de profundidad debe ser un número entero positivo."
                return True
            except (ValueError, AssertionError):
                return False
            
        if self.legal_client and self.natural_client:
            raise ValidationError('Debe ingresar solo un cliente jurídico o natural, no ambos.')
        elif self.legal_client is None and self.natural_client is None:
            raise ValidationError('Debe ingresar al menos un cliente jurídico o natural.')
        
    @staticmethod
    def is_valid_depth(value):
    # Verificar si el valor tiene el formato adecuado (por ejemplo, '0-30')
        if '-' not in value:
            return False
        parts = value.split('-')
        if len(parts) != 2:
            return False
        try:
            start = int(parts[0])
            end = int(parts[1])
            # Verificar que los valores sean enteros positivos
            if start < 0 or end < 0:
                return False
            # Verificar que el rango sea válido
            if start >= end:
                return False
        except ValueError:
            return False
        return True
    

    def __str__(self):
        return f"SoilAnalysis - {self.sampling_date}"

    class Meta:
        verbose_name = 'Análisis de Suelo'
        verbose_name_plural = 'Análisis de Suelo'
        db_table = "analisisdesuelo"
        ordering = ['sampling_date']

class SoilCompactionTest(models.Model):

    TEXTURE_CHOICES = [
        ('Franco-arcilloso', 'Franco-arcilloso'),
        ('Arcilloso', 'Arcilloso'),
        ('Arenoso', 'Arenoso'),
        ('Limoso', 'Limoso'),
        ('Mixto', 'Mixto'),
    ]
    EQUIPMENT_USED_CHOICES = [
        ('Rodillo vibratorio', 'Rodillo vibratorio'),
        ('Placa Vibratoria', 'Placa Vibratoria'),
        ('Compactador de Ruedas', 'Compactador de Ruedas'),
        ('Compactador de Pison', 'Compactador de Pison'),
        ('Penetrómetro Dinámico', 'Penetrómetro Dinámico'),
    ]
    ADJUSTMENTS_CHOICES = [
        ('No se realizaron ajustes durante el proceso', 'No se realizaron ajustes durante el proceso'),
        ('Se realizaron 2 ajustes al proceso', 'Se realizaron 2 ajustes al proceso'),
        ('Se realizaron 3 ajustes al proceso', 'Se realizaron 3 ajustes al proceso'),
        ('Se realizaron 4 o mas ajustes al proceso', 'Se realizaron 4 o mas ajustes al proceso'),
    ]
    APPROVAL_STATUS_CHOICES = [
        ('Aprobado', 'Aprobado'),
        ('No Aprobado', 'No Aprobado'),
    ]

    natural_client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente Natural', blank=True, null=True)
    legal_client = models.ForeignKey("LegalClient", verbose_name="Cliente Legal", on_delete=models.CASCADE, blank=True, null=True)
    location = models.CharField(max_length=100, verbose_name="Ubicación del Sitio")
    test_date = models.DateField(verbose_name="Fecha de la Prueba", default=datetime.now)
    test_number = models.IntegerField(verbose_name="Número Prueba", unique=True)
    engineer_name = models.ForeignKey(Engineer, on_delete=models.CASCADE, related_name='soil_compaction_tests', verbose_name="Nombre Ingeniero")
    # Datos de Identificación
    soil_type = models.CharField(max_length=50, choices=TEXTURE_CHOICES, verbose_name="Tipo de Suelo")
    natural_moisture_content = models.FloatField(verbose_name="Contenido de Humedad Natural (%)")

    compaction_equipment = models.CharField(max_length=50, choices=EQUIPMENT_USED_CHOICES, verbose_name="Equipo Utilizado")
    number_of_passes = models.IntegerField(verbose_name="Número de Pasadas")
    compaction_energy = models.FloatField(verbose_name="Energía de Compactación (%)")
    adjustments_calibrations = models.CharField(max_length=50, choices=ADJUSTMENTS_CHOICES, verbose_name="Ajustes/Calibraciones")

    max_dry_density = models.FloatField(verbose_name="Densidad Seca Máxima (g/cm³)")
    optimal_moisture_content = models.FloatField(verbose_name="Contenido de Humedad Óptimo (%)")
    field_dry_density = models.FloatField(verbose_name="Densidad Seca en Campo (g/cm³)")

    compaction_profile = models.TextField(verbose_name="Perfil de Compactación")
    results_conclusions = models.TextField(verbose_name="Resultados y Conclusiones")
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, verbose_name="Estado de Aprobación")

    def __str__(self):
        return f"Informe de Pruebas de Compactación del Suelo - Ubicación: {self.location}, Fecha: {self.test_date}"
    
    def clean(self):
        super().clean()
        # Validación para evitar fechas anteriores a hoy o posteriores a 6 meses
        if self.test_date < timezone.now().date():
            raise ValidationError("La fecha de la prueba no puede ser anterior a hoy.")
        if self.test_date > timezone.now().date() + timezone.timedelta(days=6*30):
            raise ValidationError("La fecha de la prueba no puede ser posterior a 6 meses.")
        
        if SoilCompactionTest.objects.filter(test_date=self.test_date).exists():
            raise ValidationError({'test_date': "Ya existe una prueba para esta fecha."})

        # Validación para número de prueba único para cada cliente
        if SoilCompactionTest.objects.filter(natural_client=self.natural_client, test_number=self.test_number).exists():
            raise ValidationError("El número de prueba debe ser único para cada cliente.")

        # Validación para evitar números negativos en campos numéricos
        if any(value is not None and value < 0 for value in [
            self.natural_moisture_content,
            self.compaction_energy,
            self.max_dry_density,
            self.optimal_moisture_content,
            self.field_dry_density
        ]):
            raise ValidationError("Los valores no pueden ser negativos.")
        
        if self.legal_client and self.natural_client:
            raise ValidationError('Debe ingresar solo un cliente jurídico o natural, no ambos.')
        elif self.legal_client is None and self.natural_client is None:
            raise ValidationError('Debe ingresar al menos un cliente jurídico o natural.')
    
    class Meta:
        verbose_name = "Prueba De Compactacion"
        verbose_name_plural = "Prueba De Compactacion"
        db_table = "prueba_de_compactacion"
        ordering = ['id']


class FielTrial(models.Model):

    COLOMBIAN_CITIES = [
    ('Bogotá', 'Bogotá'),
    ('Medellín', 'Medellín'),
    ('Cartagena', 'Cartagena'),
    ('Cali', 'Cali'),
    ('Santa Marta', 'Santa Marta'),
    ('Barranquilla', 'Barranquilla'),
    ('Villavicencio', 'Villavicencio'),
    ('San Gil', 'San Gil'),
    ('Bucaramanga', 'Bucaramanga'),
]
   
 

    def validate_at_least_one_file(value):
        if not any(value):
            raise ValidationError('Al menos un archivo debe ser cargado.')
    

    pdf_file = models.FileField(upload_to='pdfs/', verbose_name='PDF 1', blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    pdf_file_1 = models.FileField(upload_to='pdfs/', verbose_name='PDF 2', blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    pdf_file_2 = models.FileField(upload_to='pdfs/', verbose_name='PDF 3', blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    engineer_name = models.ForeignKey(Engineer, on_delete=models.CASCADE, related_name='engineer_trial', verbose_name="Nombre Ingeniero")
    natural_client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente Natural', blank=True, null=True)
    legal_client = models.ForeignKey("LegalClient", verbose_name="Cliente Legal", on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(default=datetime.now, verbose_name='Fecha')
    TypeOfTest_es = models.ForeignKey(Escarificacion, on_delete=models.CASCADE, verbose_name='Tipo Prueba (Escarificaciones)', blank=True, null=True)
    TypeOfTest_soi = models.ForeignKey(SoilAnalysis, on_delete=models.CASCADE, verbose_name='Tipo Prueba (Análisis de suelo)', blank=True, null=True)
    TypeOfTest_comp = models.ForeignKey(SoilCompactionTest, on_delete=models.CASCADE, verbose_name='Tipo Prueba (Prueba de Compactación)', blank=True, null=True)
    city = models.CharField(max_length=100, choices=COLOMBIAN_CITIES, verbose_name="Ciudad", default=COLOMBIAN_CITIES[0][0])
    address = models.CharField(max_length=100, verbose_name="Direccion")

    def __str__(self):
        return f"Resultado de Prueba de campo para {self.natural_client}"
    
    def clean(self):

        # Validar que al menos un campo de tipo de prueba esté completado
        if not any([self.TypeOfTest_es, self.TypeOfTest_soi, self.TypeOfTest_comp]):
            raise ValidationError({'test_type_1': 'Debe completar al menos un campo de tipo de prueba.'})
        
        # Validar que el número de archivos PDF subidos coincida con el número de pruebas seleccionadas
        selected_pdf_files = [self.pdf_file, self.pdf_file_1, self.pdf_file_2]
        selected_tests_count = sum([1 for test in [self.TypeOfTest_es, self.TypeOfTest_soi, self.TypeOfTest_comp] if test is not None])
        uploaded_pdf_files_count = sum([1 for pdf_file in selected_pdf_files if pdf_file])
        
        if selected_tests_count != uploaded_pdf_files_count:
            raise ValidationError('El número de archivos PDF subidos debe coincidir con el número de pruebas seleccionadas.')

        if self.legal_client and self.natural_client:
            raise ValidationError('Debe ingresar solo un cliente jurídico o natural, no ambos.')
        elif self.legal_client is None and self.natural_client is None:
            raise ValidationError('Debe ingresar al menos un cliente jurídico o natural.')

        # Validación para garantizar que la fecha de envío de resultados sea la fecha actual o anterior
        if self.date > timezone.now().date():
            raise ValidationError({'date': "La fecha de envío de resultados no puede ser en el futuro."})

    def save(self, *args, **kwargs):
        if not self.pk:  # Solo si es un nuevo objeto
            super().save(*args, **kwargs)
            
            # Enviar correo electrónico al cliente
            subject = 'Resultado de Laboratorio Disponible'
            email_addresses = []

            if self.natural_client:
                email_addresses.append(self.natural_client.email)
                message = render_to_string('resultado_laboratorio_email.html', {'result': self, 'client_name': self.natural_client})
            if self.legal_client:
                email_addresses.append(self.legal_client.email)
                message = render_to_string('resultado_laboratorio_email.html', {'result': self, 'client_name': self.legal_client})

            email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, email_addresses)

            if self.pdf_file:
                email.attach_file(self.pdf_file.path)
            if self.pdf_file_1:
                email.attach_file(self.pdf_file_1.path)
            if self.pdf_file_2:
                email.attach_file(self.pdf_file_2.path)

            email.send()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Prueba De Campo"
        verbose_name_plural = "PruebasDeCampo"
        db_table = "prueba_de_campo"
        ordering = ['id']
#
#
#
#
#
#LABORATORISTAA (LABORATORISTA-AUX LABORATORISTA)
class LaboratoryWorker(models.Model):

    LABORATORISTA = 'LAB'
    AUXILIAR_LABORATORISTA = 'AUX'
    
    WORKER_CHOICES = [
        (LABORATORISTA, 'Laboratorista'),
        (AUXILIAR_LABORATORISTA, 'Auxiliar Laboratorista'),
    ]
    laboratory_name = models.CharField(max_length=100, verbose_name="Nombre Laboratorista")
    email = models.EmailField(verbose_name="Correo Electrónico",unique=True,validators=[EmailValidator(message="Debe ingresar un correo electrónico válido."),])
    cell_number = models.CharField(max_length=20,verbose_name="Número de Teléfono",validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$',message="El número de celular debe tener mas de 10 digitos")])
    nit = models.CharField(max_length=20,verbose_name="Nit",unique=True,validators=[RegexValidator(regex=r'^\d{9,15}$',message="El nit debe contener entre 9 y 15 dígitos.")])
    rol = models.CharField(max_length=3, choices=WORKER_CHOICES, verbose_name="Tipo de Laboratorista")

    def __str__(self):
        return self.laboratory_name

    class Meta:
        verbose_name = "Laboratorista"
        verbose_name_plural = "Laboratoristas"
        db_table = "laboratoristas"
        ordering = ['id']
#
#
#
#
#
#PRUEBA DE RESISTENCIA
class ResistanceTest(models.Model):

    APPROVAL_CHOICES = [
        ('Aprobado', 'Aprobado'),
        ('No Aprobado', 'No Aprobado'),
    ]

    TIPO_SUELO_CHOICES = [
        ('arcilla', 'Arcilla'),
        ('arena', 'Arena'),
        ('limo', 'Limo'),
        ('suelo_orgánico', 'Suelo Orgánico'),
        ('roca', 'Roca'),
        ('otros', 'Otros'),
    ]

    LONGITUD_CHOICES = [
        (-180, '180° W'),
        (-170, '170° W'),
        (0, '0°'),
        (170, '170° E'),
        (180, '180° E'),
    ]
    
    LATITUD_CHOICES = [
        (-90, '90° S'),
        (0, '0°'),
        (90, '90° N'),
    ]
    
    PROFUNDIDAD_CHOICES = [
        (0.5, 'Menos de 0.5 m'),
        (1.0, '0.5 - 1.0 m'),
        (1.5, '1.0 - 1.5 m'),
        (2.0, '1.5 - 2.0 m'),
    ]

    TEST_METHOD_CHOICES = [
        ('ensayo_permeabilidad_constante', 'Ensayo de Permeabilidad Constante'),
        ('ensayo_piezoconometro', 'Ensayo de Piezoconómetro'),
        ('ensayo_laboratorio', 'Ensayo de Laboratorio'),
    ]


    PERMEABILITY_CHOICES = [
    (0.001, 'Baja (0.001 m/s)'),
    (0.01, 'Media (0.01 m/s)'),
    (0.1, 'Alta (0.1 m/s)'),
    ]

    HYDRAULIC_CONDUCTIVITY_CHOICES = [
    (0.0001, 'Baja (0.0001 m/s)'),
    (0.001, 'Media (0.001 m/s)'),
    (0.01, 'Alta (0.01 m/s)'),
    ]
    NameLaboratory = models.ForeignKey(LaboratoryWorker, on_delete=models.CASCADE, verbose_name='Nombre Laboratorista')
    natural_client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente Natural', blank=True, null=True)
    legal_client = models.ForeignKey(LegalClient, on_delete=models.CASCADE, verbose_name='Cliente Juridico', blank=True, null=True)
    test_number = models.IntegerField(verbose_name='Número de Prueba',validators=[MinValueValidator(0), MaxValueValidator(9999)],unique=True,help_text='Máximo 4 dígitos, no se permiten números negativos')
    
    soil_type = models.CharField(max_length=50, choices=TIPO_SUELO_CHOICES, verbose_name='Tipo de Suelo')
    sample_depth = models.DecimalField(max_digits=5, decimal_places=2, help_text="Profundidad de la muestra en metros", verbose_name='Profundidad de la Muestra', choices=PROFUNDIDAD_CHOICES)
    location_latitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Latitud de la ubicación", verbose_name='Latitud de la Ubicación', choices=LATITUD_CHOICES)
    location_longitude = models.DecimalField(max_digits=9, decimal_places=6, choices=LONGITUD_CHOICES, help_text="Longitud de la ubicación", verbose_name='Longitud de la Ubicación')
    test_date = models.DateField(verbose_name="Fecha de Prueba",default=timezone.now)
    test_method = models.CharField(max_length=100, choices=TEST_METHOD_CHOICES, verbose_name='Método de Prueba')
    procedure = models.TextField(verbose_name='Procedimiento')
    permeability = models.DecimalField(max_digits=10,decimal_places=6,verbose_name='Permeabilidad (m/s)',blank=True,null=True,validators=[MinValueValidator(0)],help_text='Ingrese el valor de permeabilidad en metros por segundo (m/s). Por ejemplo, 0.005.')
    hydraulic_conductivity = models.DecimalField(max_digits=10,decimal_places=6,verbose_name='Conductividad Hidráulica (m/s)',blank=True,null=True,validators=[MinValueValidator(0)],help_text='Ingrese el valor de conductividad hidráulica en metros por segundo (m/s). Por ejemplo, 0.008.')
    additional_comments = models.TextField(verbose_name='Comentarios Adicionales', blank=True, null=True)
    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES, verbose_name="Estado de la Prueba")

    def __str__(self):
        return f"Prueba de Resistencia del Suelo - {self.id}"
    
    def clean(self):
        super().clean()
        if self.test_date < timezone.now().date():
            raise ValidationError({'test_date': 'La fecha de la prueba no puede ser anterior a la fecha actual.'})

        if self.legal_client and self.natural_client:
            raise ValidationError('Debe ingresar solo un cliente jurídico o natural, no ambos.')
        elif self.legal_client is None and self.natural_client is None:
            raise ValidationError('Debe ingresar al menos un cliente jurídico o natural.')
        
        if ResistanceTest.objects.exclude(id=self.id).filter(test_number=self.test_number).exists():
            raise ValidationError({'test_number': 'Ya existe una prueba con este número.'})
        
        if len(self.procedure) < 10:
            raise ValidationError('El procedimiento debe contener al menos 10 caracteres.')
        
        if len(self.additional_comments) < 4:
            raise ValidationError('Debe haber almenos un comentario.')
    
    class Meta:
        verbose_name = "Prueba de Resistencia"
        verbose_name_plural = "Pruebas de Resistencia"
        db_table = "prueba_resistencia"
        ordering = ['id']
#
#
#
#
#
#
#PRUEBA DE PERMEABILIDAD
class TestPermeability(models.Model):

    APPROVAL_CHOICES = [
        ('Aprobado', 'Aprobado'),
        ('No Aprobado', 'No Aprobado'),
    ]

    SOIL_TYPE_CHOICES = [
        ('arcilloso', 'Arcilloso'),
        ('arenoso', 'Arenoso'),
        ('limoso', 'Limoso'),
        # Agrega más opciones según sea necesario
    ]
    
    GRAIN_SIZE_CHOICES = [
        ('fino', 'Fino'),
        ('medio', 'Medio'),
        ('grueso', 'Grueso'),
        # Agrega más opciones según sea necesario
    ]

    SOIL_POROSITY_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        # Agrega más opciones según sea necesario
    ]

    SOIL_COMPACTION_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        # Agrega más opciones según sea necesario
    ]

    LOADING_CONDITIONS_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
        ('otros', 'Otros'),  # Agrega más opciones según sea necesario
    ]

    DRAINAGE_CONDITIONS_CHOICES = [
        ('buena', 'Buena'),
        ('regular', 'Regular'),
        ('mala', 'Mala'),
        ('otros', 'Otros'),  # Agrega más opciones según sea necesario
    ]

    SOIL_TEMPERATURE_CHOICES = [
        (15.2, '15.2'),
        (18.9, '18.9'),
        (22.3, '22.3'),
        (25.6, '25.6'),
        (28.1, '28.1'),
        (30.7, '30.7'),
        (33.4, '33.4'),
        (36.2, '36.2'),
        (39.8, '39.8'),
        (42.5, '42.5'),
    ]

    SOIL_CHEMISTRY_CHOICES = [
        ('PH: 7.2, Nitrógeno: 0.08%', 'PH: 7.2, Nitrógeno: 0.08%'),
        ('PH: 6.8, Nitrógeno: 0.06%', 'PH: 6.8, Nitrógeno: 0.06%'),
        ('PH: 5.9, Nitrógeno: 0.04%', 'PH: 5.9, Nitrógeno: 0.04%'),
        ('PH: 7.5, Nitrógeno: 0.09%', 'PH: 7.5, Nitrógeno: 0.09%'),
        ('PH: 6.2, Nitrógeno: 0.07%', 'PH: 6.2, Nitrógeno: 0.07%'),
        ('PH: 7.0, Nitrógeno: 0.05%', 'PH: 7.0, Nitrógeno: 0.05%'),
        ('PH: 6.5, Nitrógeno: 0.03%', 'PH: 6.5, Nitrógeno: 0.03%'),
        ('PH: 7.8, Nitrógeno: 0.11%', 'PH: 7.8, Nitrógeno: 0.11%'),
        ('PH: 6.0, Nitrógeno: 0.02%', 'PH: 6.0, Nitrógeno: 0.02%'),
        ('PH: 7.3, Nitrógeno: 0.1%', 'PH: 7.3, Nitrógeno: 0.1%'),
    ]


    # Información General
    natural_client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente Natural', blank=True, null=True)

    legal_client = models.ForeignKey(LegalClient, on_delete=models.CASCADE, verbose_name='Cliente Juridico', blank=True, null=True)

    test_number = models.IntegerField(verbose_name='Número de Prueba',validators=[MinValueValidator(0), MaxValueValidator(9999)],unique=True,help_text='Máximo 4 dígitos, no se permiten números negativos')
    test_date = models.DateField(verbose_name="Fecha de Prueba",default=timezone.now)
    NameLaboratory = models.ForeignKey(LaboratoryWorker, on_delete=models.CASCADE, verbose_name='Nombre Laboratorista')

    # Características del Suelo
    soil_type = models.CharField(max_length=100, choices=SOIL_TYPE_CHOICES, verbose_name='Tipo de Suelo')
    grain_size = models.CharField(max_length=100, choices=GRAIN_SIZE_CHOICES, verbose_name='Tamaño de Grano')
    soil_porosity = models.CharField(max_length=100, choices=SOIL_POROSITY_CHOICES, verbose_name='Porosidad del Suelo')
    soil_compaction = models.CharField(max_length=100, choices=SOIL_COMPACTION_CHOICES, verbose_name='Compactación del Suelo')

    # Condiciones de Prueba
    soil_temperature = models.FloatField(verbose_name='Temperatura del Suelo', choices=SOIL_TEMPERATURE_CHOICES)
    soil_moisture_content = models.FloatField(verbose_name='Contenido de Humedad del Suelo',validators=[MinValueValidator(0)],help_text='Ingrese el contenido de humedad del suelo en porcentaje. Debe ser un número positivo. Por ejemplo, 0.15.')
    hydrostatic_pressure = models.FloatField(verbose_name='Presión Hidrostática',validators=[MinValueValidator(0)],help_text='Ingrese la presión hidrostática en unidades específicas. Debe ser un número positivo. Por ejemplo, 100.0.')
    loading_conditions = models.CharField(max_length=100, choices=LOADING_CONDITIONS_CHOICES, verbose_name='Condiciones de Carga')
    drainage_conditions = models.CharField(max_length=100, choices=DRAINAGE_CONDITIONS_CHOICES, verbose_name='Condiciones de Drenaje')
    soil_chemistry = models.CharField(max_length=100, verbose_name='Química del Suelo', choices=SOIL_CHEMISTRY_CHOICES)

        # Resultados de la Prueba
    permeability_velocity = models.FloatField(verbose_name='Velocidad de Permeabilidad',validators=[MinValueValidator(0)],help_text='Ingrese la velocidad de permeabilidad en cm/s. Debe ser un número positivo. Por ejemplo, 0.25.')
    intrinsic_permeability = models.FloatField(verbose_name='Permeabilidad Intrínseca',validators=[MinValueValidator(0)],help_text='Ingrese la permeabilidad intrínseca en unidades específicas. Debe ser un número positivo. Por ejemplo, 0.003.')
    permeability_coefficient = models.FloatField(verbose_name='Coeficiente de Permeabilidad',validators=[MinValueValidator(0)],help_text='Ingrese el coeficiente de permeabilidad en unidades específicas. Debe ser un número positivo. Por ejemplo, 2.5.')

        # Observaciones
    observations = models.TextField(verbose_name='Observaciones')

        # Conclusiones
    conclusions = models.TextField(verbose_name='Conclusiones')

    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES, verbose_name="Estado de la Prueba")

    def __str__(self):
            return str(self.test_number)
    
    def clean(self):
        super().clean()
        if self.test_date < timezone.now().date():
            raise ValidationError({'test_date': 'La fecha de la prueba no puede ser anterior a la fecha actual.'})
        
        if TestPermeability.objects.exclude(id=self.id).filter(test_number=self.test_number).exists():
            raise ValidationError({'test_number': 'Ya existe una prueba con este número.'})
        
        if self.legal_client and self.natural_client:
            raise ValidationError('Debe ingresar solo un cliente jurídico o natural, no ambos.')
        elif self.legal_client is None and self.natural_client is None:
            raise ValidationError('Debe ingresar al menos un cliente jurídico o natural.')
        
    class Meta:
            verbose_name = "Prueba de Permeabilidad"
            verbose_name_plural = "Pruebas de Permeabilidad"
            db_table = "prueba_permeabilidad"
            ordering = ['id']
#
#
#
#
#
#
#PRUEBA DE ANALISIS PETROGRAFICO
class PetrographicAnalysis(models.Model):

    APPROVAL_CHOICES = [
        ('Aprobado', 'Aprobado'),
        ('No Aprobado', 'No Aprobado'),
    ]

    # Información General
    natural_client = models.ForeignKey("Client", verbose_name="Cliente Natural", on_delete=models.CASCADE, blank=True, null=True)
    legal_client = models.ForeignKey("LegalClient", verbose_name="Cliente Legal", on_delete=models.CASCADE, blank=True, null=True)
    test_number = models.IntegerField(verbose_name="Número de Prueba", validators=[MinValueValidator(0), MaxValueValidator(9999)], unique=True, help_text="Máximo 4 dígitos, no se permiten números negativos")
    test_date = models.DateField(verbose_name="Fecha de Prueba", default=timezone.now)
    name_laboratory = models.ForeignKey("LaboratoryWorker", on_delete=models.CASCADE, verbose_name="Nombre Laboratorista")

    # Descripción de la Muestra
    sample_description = models.TextField(verbose_name="Descripción de la Muestra")

    # Características Petrográficas
    mineral_composition = models.TextField(verbose_name="Composición Mineral")
    grain_size_distribution = models.TextField(verbose_name="Distribución del Tamaño de Grano")
    texture = models.TextField(verbose_name="Textura")
    porosity = models.TextField(verbose_name="Porosidad")
    cementation = models.TextField(verbose_name="Cementación")

    # Resultados de Análisis
    mineral_identification = models.TextField(verbose_name="Identificación Mineral")
    mineral_quantification = models.TextField(verbose_name="Cuantificación Mineral")
    rock_type = models.CharField(max_length=100, verbose_name="Tipo de Roca")
    color = models.CharField(max_length=50, verbose_name="Color")

    # Conclusiones
    conclusions = models.TextField(verbose_name="Conclusiones")
    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES, verbose_name="Estado de la Prueba")

    def __str__(self):
            return str(self.test_number)
    
    def clean(self):
        super().clean()
        if self.test_date < timezone.now().date():
            raise ValidationError({'test_date': 'La fecha de la prueba no puede ser anterior a la fecha actual.'})
        
        if PetrographicAnalysis.objects.exclude(id=self.id).filter(test_number=self.test_number).exists():
            raise ValidationError({'test_number': 'Ya existe una prueba con este número.'})
        
        if self.legal_client and self.natural_client:
            raise ValidationError('Debe ingresar solo un cliente jurídico o natural, no ambos.')
        elif self.legal_client is None and self.natural_client is None:
            raise ValidationError('Debe ingresar al menos un cliente jurídico o natural.')

    class Meta:
        verbose_name = "Análisis Petrográfico"
        verbose_name_plural = "Análisis Petrográficos"
        db_table = "analisis_petrograficos"
        ordering = ['id']
#
#
#
#
#
#
#PRUEBAS DE LABORATORIO
class LaboratoryTrial(models.Model):
    TEST_TYPE_CHOICES = [
        ('Análisis Petrográfico', 'Análisis Petrográfico'),
        ('Prueba de Permeabilidad', 'Prueba de Permeabilidad'),
        ('Prueba de Resistencia', 'Prueba de Resistencia'),
    ]

    COLOMBIAN_CITIES = [
        ('Bogotá', 'Bogotá'),
        ('Medellín', 'Medellín'),
        ('Cartagena', 'Cartagena'),
        ('Cali', 'Cali'),
        ('Santa Marta', 'Santa Marta'),
        ('Barranquilla', 'Barranquilla'),
        ('Villavicencio', 'Villavicencio'),
        ('San Gil', 'San Gil'),
        ('Bucaramanga', 'Bucaramanga'),
    ]

    pdf_file_1 = models.FileField(upload_to='pdfs/', verbose_name='PDF 1', blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    pdf_file_2 = models.FileField(upload_to='pdfs/', verbose_name='PDF 2', blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    pdf_file_3 = models.FileField(upload_to='pdfs/', verbose_name='PDF 3', blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    laboratory_name = models.ForeignKey("LaboratoryWorker", on_delete=models.CASCADE, verbose_name="Nombre Laboratorista")
    natural_client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente Natural', blank=True, null=True)
    legal_client = models.ForeignKey("LegalClient", verbose_name="Cliente Legal", on_delete=models.CASCADE, blank=True, null=True)
    test_date = models.DateField(verbose_name="Fecha de Prueba", default=timezone.now)
    test_type_1 = models.ForeignKey(PetrographicAnalysis, on_delete=models.CASCADE, verbose_name='Tipo Prueba (Análisis Petrográfico)', blank=True, null=True)
    test_type_2 = models.ForeignKey(TestPermeability, on_delete=models.CASCADE, verbose_name='Tipo Prueba (Prueba de Permeabilidad)', blank=True, null=True)
    test_type_3 = models.ForeignKey(ResistanceTest, on_delete=models.CASCADE, verbose_name='Tipo Prueba (Prueba de Resistencia)', blank=True, null=True)
    city = models.CharField(max_length=100, choices=COLOMBIAN_CITIES, verbose_name="Ciudad", default=COLOMBIAN_CITIES[0][0])
    address = models.CharField(max_length=100, verbose_name="Dirección")

    def clean(self):
        super().clean()
        
        # Validar que al menos un campo de tipo de prueba esté completado
        if not any([self.test_type_1, self.test_type_2, self.test_type_3]):
            raise ValidationError({'test_type_1': 'Debe completar al menos un campo de tipo de prueba.'})
        
        # Validar que el número de archivos PDF subidos coincida con el número de pruebas seleccionadas
        selected_pdf_files = [self.pdf_file_1, self.pdf_file_2, self.pdf_file_3]
        selected_tests_count = sum([1 for test in [self.test_type_1, self.test_type_2, self.test_type_3] if test is not None])
        uploaded_pdf_files_count = sum([1 for pdf_file in selected_pdf_files if pdf_file])
        
        if selected_tests_count != uploaded_pdf_files_count:
            raise ValidationError('El número de archivos PDF subidos debe coincidir con el número de pruebas seleccionadas.')

        # Validar la fecha de la prueba
        if self.test_date < timezone.now().date():
            raise ValidationError({'test_date': 'La fecha de la prueba no puede ser anterior a la fecha actual.'})

        # Validar la selección de cliente
        if self.legal_client and self.natural_client:
            raise ValidationError('Debe ingresar solo un cliente jurídico o natural, no ambos.')
        elif self.legal_client is None and self.natural_client is None:
            raise ValidationError('Debe ingresar al menos un cliente jurídico o natural.')

    def __str__(self):
        return str(self.laboratory_name)

    def save(self, *args, **kwargs):
        if not self.pk:  # Solo si es un nuevo objeto
            super().save(*args, **kwargs)
            
            # Enviar correo electrónico al cliente
            subject = 'Resultado de Laboratorio Disponible'
            email_addresses = []

            if self.natural_client:
                email_addresses.append(self.natural_client.email)
                message = render_to_string('resultado_laboratorio_email.html', {'result': self, 'client_name': self.natural_client})
            if self.legal_client:
                email_addresses.append(self.legal_client.email)
                message = render_to_string('resultado_laboratorio_email.html', {'result': self, 'client_name': self.legal_client})

            email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, email_addresses)

            if self.pdf_file_1:
                email.attach_file(self.pdf_file_1.path)
            if self.pdf_file_2:
                email.attach_file(self.pdf_file_2.path)
            if self.pdf_file_3:
                email.attach_file(self.pdf_file_3.path)

            email.send()

        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "PruebaLaboratorio"
        verbose_name_plural = "PruebasLaboratorio"
        db_table = "pruebas_laboratorio"
        ordering = ['id']



class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name="Nombre Categoria")
    category_description = models.TextField(max_length=300, verbose_name="Descripcion Categoria")


    
    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name = "categoria"
        verbose_name_plural = "categorias"
        db_table = "categoria"
        ordering = ['id']


class Inventory(models.Model):
    product_name_invent = models.CharField(max_length=200, verbose_name="Nombre Articulo")
    amount_invent = models.CharField(max_length=100, verbose_name="Cantidad Articulo")
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoria")
    # category_name = models.ForeignKey(Category, on_delete=models.CASCADE,  verbose_name='Nombre Categoria')
    description_invent = models.TextField(max_length=300,verbose_name="Descripcion Articulo")
    # image_invent = models.ImageField(upload_to='photo/%Y/%m/%d', null=True, blank=True)
    image_invent = models.ImageField(upload_to='media', null=True, blank=True,verbose_name="Imagen")


    def show_image_invent(self):
        return format_html('<img src={} width="100" /> ', self.image_invent.url)

    def __str__(self):
        return self.amount_invent
    
    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        db_table = "inventario"
        ordering = ['id']





# class Machinery(models.Model):
#     machine_name = models.CharField(max_length=100, verbose_name="Nombre Maquina")
#     machine_description = models.TextField(max_length=300, verbose_name="Descripcion Maquina")
#     machine_state = models.CharField(max_length=100, verbose_name="Estado Maquina")
#     type = models.ForeignKey(Resource, on_delete=models.CASCADE)
    


#     def __str__(self):
#         return self.machine_name
    
#     class Meta:
#         verbose_name = "Maquinaria"
#         verbose_name_plural = "Maquinarias"
#         db_table = "maquinaria"
#         ordering = ['id']


# class Material(models.Model):
#     material_name = models.CharField(max_length=100, verbose_name="Nombre Material")
#     material_description = models.TextField(max_length=300, verbose_name="Descripcion Material")
#     material_amount = models.IntegerField( verbose_name="Cantidad Material")
#     type = models.ForeignKey(Resource, on_delete=models.CASCADE)


#     def __str__(self):
#         return self.material_name
    
#     class Meta:
#         verbose_name = "Material"
#         verbose_name_plural = "Materiales"
#         db_table = "material"
#         ordering = ['id']





# Create your models here.
