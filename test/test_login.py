import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.fixture
def superadmin_user():
    return User.objects.create_superuser(username='superadmin', email='superadmin@example.com', password='password')

@pytest.mark.django_db
def test_superuser_login(client, superadmin_user):
    # URL de inicio de sesión
    login_url = reverse('inicio')

    # Iniciar sesión como superadmin
    client.login(username='superadmin', password='password')

    # Realizar la solicitud GET para iniciar sesión
    response = client.get(login_url)

    # Verificar que se haya redirigido correctamente después de iniciar sesión
    assert response.status_code == 200  # Cambia 200 al código de estado correcto esperado
