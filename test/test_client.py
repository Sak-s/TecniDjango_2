import pytest
from django.utils import timezone
from core.models import Client

@pytest.mark.django_db
def test_create_client():
    # Crear un nuevo cliente
    client_data = {
        "name_client": "John",
        "last_name_client": "Doe",
        "cell_number": 1234567890,
        "address": "123 Main St",
        "date": timezone.now(),
        "email": "john@example.com"
    }
    assert validate_client_data(client_data)  # Agregar validación
    Client.objects.create(**client_data)
    # Verificar que el cliente se ha creado correctamente
    assert Client.objects.count() == 1

@pytest.mark.django_db
def test_read_client():
    # Crear un cliente
    client = Client.objects.create(
        name_client="Jane",
        last_name_client="Doe",
        cell_number=9876543210,
        address="456 Elm St",
        date=timezone.now(),
        email="jane@example.com"
    )
    # Leer el cliente creado
    assert Client.objects.get(id=client.id).name_client == "Jane"

@pytest.mark.django_db
def test_update_client():
    # Crear un cliente
    client = Client.objects.create(
        name_client="Alex",
        last_name_client="Smith",
        cell_number=5555555555,
        address="789 Oak St",
        date=timezone.now(),
        email="alex@example.com"
    )
    # Actualizar la información del cliente
    client.name_client = "Alexander"
    client.save()
    # Verificar que la información se ha actualizado correctamente
    assert Client.objects.get(id=client.id).name_client == "Alexander"

@pytest.mark.django_db
def test_delete_client():
    # Crear un cliente
    client = Client.objects.create(
        name_client="Mary",
        last_name_client="Johnson",
        cell_number=9999999999,
        address="101 Pine St",
        date=timezone.now(),
        email="mary@example.com"
    )
    # Eliminar el cliente
    client.delete()
    # Verificar que el cliente se ha eliminado correctamente
    assert Client.objects.count() == 0

def validate_client_data(client_data):
    """
    Función para validar los datos del cliente.
    Verifica si el número de celular tiene 10 dígitos y si el correo electrónico contiene el carácter "@".
    """
    if len(str(client_data.get('cell_number'))) != 10:
        raise ValueError("Número de celular debe tener 10 dígitos")
    if '@' not in client_data.get('email'):
        raise ValueError("El correo electrónico debe contener el carácter '@'")
    return True


