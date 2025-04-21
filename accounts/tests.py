import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


@pytest.mark.django_db
def test_user_creation():
    User = get_user_model()
    user = User.objects.create_user(
        email='test@example.com',
        full_name='Test User',
        phone_number='1234567890',
        password='testpass'
    )
    assert user.email == 'test@example.com'
    assert user.check_password('testpass')
    assert user.is_active
    assert not user.is_admin

    @pytest.mark.django_db
    def test_user_login(client, django_user_model):
        django_user_model.objects.create_user(email='user@example.com', full_name='Test', phone_number='123',
                                              password='password')
        response = client.post(reverse('accounts:login'), {
            'email': 'user@example.com',
            'password': 'password'
        })
        assert response.status_code == 302
