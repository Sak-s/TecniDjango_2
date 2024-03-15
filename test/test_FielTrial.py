import pytest
from django.utils import timezone
from core.models import Client, FielTrial

@pytest.mark.django_db
def test_create_fiel_trial():
    # Crear un nuevo cliente primero
    client = Client.objects.create(
        name_client="Nombre Cliente Ejemplo",
        last_name_client="Apellido Cliente Ejemplo",
        cell_number=1234567890,
        address="Dirección Ejemplo",
        date=timezone.now(),
        email="cliente@example.com"
    )

    # Crear un nuevo FielTrial que dependa del cliente creado
    fiel_trial_data = {
        "name_employee": "Empleado Ejemplo",
        "date": timezone.now(),
        "cylinder_number": 1,
        "test_number": 1,
        "type": client,  # Usar el cliente creado anteriormente
        "location": "Ubicación Ejemplo",
        "revenence": "Revenimiento Ejemplo",
        "ultrasonic": "Ultrasonido Ejemplo",
        "sclerometry": 1,
        "analysis_petrographics": "Análisis Petrográfico Ejemplo",
        "elaboration": "Elaboración Ejemplo",
        "reactivity": "Reactividad Ejemplo",
        "compression": "Compresión Ejemplo"
    }
    FielTrial.objects.create(**fiel_trial_data)

    # Verificar que el FielTrial se haya creado correctamente
    assert FielTrial.objects.count() == 1
