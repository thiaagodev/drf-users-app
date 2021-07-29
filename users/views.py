from secrets import token_urlsafe
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.serializers import *
from users.models import User, VerifyEmailToken, PasswordResetToken
from users import tasks


# Users views

class CreateUserView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            data = dict(request.data)
            data.pop('password')

            return Response(data, status=status.HTTP_201_CREATED)


class ListUserView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        pk = self.request.user.id
        queryset = User.objects.all().filter(pk=pk)

        return queryset


@api_view(['POST'])
def activate_user_account(request):
    """ Recebe um token que foi enviado por email, e caso seja válido, ativa a conta do usuário """

    received_token = request.data.get('token', None)

    if received_token is None:
        return Response({"details": "Por favor, informe um token!"}, status=status.HTTP_400_BAD_REQUEST)

    token_exists = VerifyEmailToken.objects.all().filter(token=received_token).exists()
    if not token_exists:
        return Response({"details": "Token is invalid"}, status.HTTP_404_NOT_FOUND)

    token = VerifyEmailToken.objects.get(token=received_token)
    user = get_object_or_404(User, pk=token.user_id)
    user.is_active = True
    user.save()
    token.delete()

    return Response(status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def update_user(request):
    """ Utilizada para atualizar dados pessoais do usuário """

    pk = request.user.id
    user = get_object_or_404(User, pk=pk)
    serializer = UserUpdateSerializer(user, request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def update_user_password(request):
    """ Recebe a senha atual e a nova senha, e após ser confirmado a senha atual, atualiza a senha do usuário """

    pk = request.user.id
    user = get_object_or_404(User, pk=pk)
    actual_password = request.data.get('actual_password', None)
    new_password = request.data.get('new_password', None)

    if actual_password is None or new_password is None:
        return Response({"details": "Por favor, informe a antiga e nova senha!"}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(actual_password):
        return Response({"details": "Senha atual não coincide!"}, status=status.HTTP_401_UNAUTHORIZED)

    user.set_password(new_password)
    user.save()

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def forget_password(request):
    """ Recebe um email e gera um token para que possa a senha possa ser recuperada """

    email = request.data.get('email', None)

    if email is None:
        return Response({"details": "Por favor, informe o email de usuário"}, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(User, email=email)

    if PasswordResetToken.objects.all().filter(user=user).exists():
        old_token = PasswordResetToken.objects.get(user=user)
        old_token.delete()

    token = token_urlsafe(64)
    PasswordResetToken.objects.create(user=user, token=token)

    tasks.send_mail_to_reset_user_password.delay(user_email=user.email, first_name=user.first_name, token=token)

    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def reset_password(request):
    """ Recebe um token e uma nova senha para realizar o reset """

    received_token = request.data.get('token', None)
    new_password = request.data.get('new_password', None)

    if received_token is None:
        return Response({"details": "Por favor, informe um token!"}, status=status.HTTP_400_BAD_REQUEST)

    if new_password is None:
        return Response({"details": "Por favor, informe uma nova senha!"}, status=status.HTTP_400_BAD_REQUEST)

    if len(new_password) < 6:
        return Response({"details": "Senha inválida!"}, status=status.HTTP_400_BAD_REQUEST)

    token_exists = PasswordResetToken.objects.all().filter(token=received_token).exists()
    if not token_exists:
        return Response({"details": "Token is invalid"}, status.HTTP_404_NOT_FOUND)

    token = PasswordResetToken.objects.get(token=received_token)
    user = get_object_or_404(User, pk=token.user_id)
    user.set_password(new_password)
    user.save()
    token.delete()

    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_user_account(request):
    pk = request.user.id
    user = get_object_or_404(User, pk=pk)
    user.delete()

    return Response(status=status.HTTP_200_OK)

# Address views


class IsAddressOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an address to edit it.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class AddressViewSet(ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated, IsAddressOwner)

    def get_queryset(self):
        owner_queryset = Address.objects.all().filter(owner=self.request.user)
        return owner_queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)
