import secrets

from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import User, Address, VerifyEmailToken
from users import tasks


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'cpf', 'birth_date',
                  'phone_number', 'receive_future_promotional_emails', 'provide_data_to_improve_user_exp')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'cpf', 'birth_date', 'phone_number',
                  'receive_future_promotional_emails', 'provide_data_to_improve_user_exp')

    def create(self, validated_data):
        """ Cria um usuário, e juntamente cria o token para verificação do email """

        email = validated_data.get('email', None)
        validated_data.pop('email')

        password = validated_data.get('password', None)
        validated_data.pop('password')

        first_name = validated_data.get('first_name', None)
        validated_data.pop('first_name')

        last_name = validated_data.get('last_name', None)
        validated_data.pop('last_name')

        cpf = validated_data.get('cpf', None)
        validated_data.pop('cpf')

        user = User.objects.create_user(email=email, password=password, first_name=first_name,
                                        last_name=last_name, cpf=cpf, **validated_data)

        token = secrets.token_urlsafe(64)
        VerifyEmailToken.objects.create(user=user, token=token)

        tasks.send_mail_to_verify_account.delay(user_email=user.email, first_name=user.first_name, token=token)

        return user

    def validate(self, data):
        first_name = data['first_name']
        last_name = data['last_name']

        if not first_name.isalpha() or not last_name.isalpha():
            raise ValidationError('Nome e sobrenome devem conter apenas letras!')

        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'cpf', 'birth_date', 'phone_number',
                  'receive_future_promotional_emails', 'provide_data_to_improve_user_exp')

    def validate(self, data):
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)

        if first_name is not None:
            if not first_name.isalpha():
                raise ValidationError('Nome e sobrenome devem conter apenas letras!')

        if last_name is not None:
            if not last_name.isalpha():
                raise ValidationError('Nome e sobrenome devem conter apenas letras!')

        return data


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        extra_kwargs = {"owner": {"required": False, "allow_null": True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['state'] = instance.get_state_display()

        return representation
