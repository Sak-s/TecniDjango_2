import pytest
from django.utils import timezone
from core.models import FielTrial, LaboratoryTrial, Client

@pytest.fixture
def create_client():
    return Client.objects.create(
        name_client="John",
        last_name_client="Doe",
        cell_number="123456789",
        address="123 Main St",
        date=timezone.now(),
        email="john@example.com"
    )

@pytest.mark.django_db
def test_create_fiel_trial(create_client):
    client = create_client
    fiel_trial = FielTrial.objects.create(
        name_employee="Empleado Ejemplo",
        date=timezone.now(),
        cylinder_number=1,
        test_number=1,
        type=client,
        location="Ubicación Ejemplo",
        revenence="Revenimiento Ejemplo",
        ultrasonic="Ultrasonico Ejemplo",
        sclerometry=1,
        analysis_petrographics="Análisis Petrográfico Ejemplo",
        elaboration="Elaboración Ejemplo",
        reactivity="Reactividad Ejemplo",
        compression="Compresión Ejemplo"
    )
    assert FielTrial.objects.count() == 1

@pytest.mark.django_db
def test_create_laboratory_trial(create_client):
    client = create_client
    fiel_trial = FielTrial.objects.create(
        name_employee="Empleado Ejemplo",
        date=timezone.now(),
        cylinder_number=1,
        test_number=1,
        type=client,
        location="Ubicación Ejemplo",
        revenence="Revenimiento Ejemplo",
        ultrasonic="Ultrasonico Ejemplo",
        sclerometry=1,
        analysis_petrographics="Análisis Petrográfico Ejemplo",
        elaboration="Elaboración Ejemplo",
        reactivity="Reactividad Ejemplo",
        compression="Compresión Ejemplo"
    )
    laboratory_trial = LaboratoryTrial.objects.create(
        name_employee="Empleado Ejemplo",
        date=timezone.now(),
        cylinder_number=1,
        test_number=1,
        name_client="Cliente Ejemplo",
        air_content="Contenido de Aire Ejemplo",
        contraction_drying="Contracción de Secado Ejemplo",
        analysis_petrographics="Análisis Petrográfico Ejemplo",
        elasticity_extensometer="Elasticidad del Extensómetro Ejemplo",
        petrographic_study="Estudio Petrográfico Ejemplo",
        concrete_flexion="Flexión de Concreto Ejemplo",
        compression="Compresión Ejemplo",
        granulometry="Granulometría Ejemplo",
        permeability_testing="Pruebas de Permeabilidad Ejemplo",
        type_trial="Tipo de Prueba Ejemplo",
        profile=fiel_trial
    )
    assert LaboratoryTrial.objects.count() == 1
