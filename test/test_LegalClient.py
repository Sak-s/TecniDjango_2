import pytest
from django.utils import timezone
from core.models import LegalClient

@pytest.mark.django_db
def test_create_legal_client():
    # Crear un nuevo cliente legal
    legal_client_data = {
        "registered_name": "Legal Solutions Inc.",
        "nit": 1234567890,
        "cell_number": 9876543210,
        "address": "123 Legal St",
        "date": timezone.now(),
        "email": "legal@example.com"
    }
    assert validate_legal_client_data(legal_client_data)  # Agregar validación
    LegalClient.objects.create(**legal_client_data)
    # Verificar que el cliente se ha creado correctamente
    assert LegalClient.objects.count() == 1

@pytest.mark.django_db
def test_read_legal_client():
    # Crear un cliente legal
    legal_client = LegalClient.objects.create(
        registered_name="Legal Associates",
        nit=9876543210,
        cell_number=1234567890,
        address="456 Law St",
        date=timezone.now(),
        email="associates@example.com"
    )
    # Leer el cliente legal creado
    assert LegalClient.objects.get(id=legal_client.id).registered_name == "Legal Associates"

# Puedes continuar con pruebas similares para actualizar y eliminar clientes legales si lo deseas

def validate_legal_client_data(legal_client_data):
    """
    Función para validar los datos del cliente legal.
    Verifica si el número de celular tiene 10 dígitos y si el correo electrónico contiene el carácter "@".
    """
    if len(str(legal_client_data.get('cell_number'))) != 10:
        raise ValueError("Número de celular debe tener 10 dígitos")
    if '@' not in legal_client_data.get('email'):
        raise ValueError("El correo electrónico debe contener el carácter '@'")
    return True
