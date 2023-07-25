import pytest
from django.contrib.auth import get_user_model
from users.choices import *
from users.serializers import *

User = get_user_model()


class TestUserCreation:

    @pytest.mark.django_db
    def test_create_user(self):
        serializer = CustomUserCreateSerializer(data={
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '+254712345673',
            'sex': SexChoices.MALE,
            'password': 'testpassword'
        })
        if serializer.is_valid():
            user = serializer.save()
            print(user)

            assert user.username == 'testuser'
            assert user.first_name == 'John'
            assert user.last_name == 'Doe'
            assert user.phone_number == '+254712345673'
            assert user.sex == SexChoices.MALE
            assert user.check_password('testpassword')
            assert not user.is_staff
            assert not user.is_superuser
            assert user.is_active
        else:
            print(serializer.errors)

    @pytest.mark.django_db
    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            username='admin',
            first_name='Admin',
            last_name='User',
            phone_number='+254712345678',
            sex=SexChoices.FEMALE,
            password='adminpassword'
        )
        assert superuser.username == 'admin'
        assert superuser.first_name == 'Admin'
        assert superuser.last_name == 'User'
        assert superuser.phone_number == '+254712345678'
        assert superuser.sex == SexChoices.FEMALE
        assert superuser.check_password('adminpassword')
        assert superuser.is_staff
        assert superuser.is_superuser
        assert superuser.is_active
