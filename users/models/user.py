from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from localflavor.br.models import BRCPFField


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """ Cria e salva um usuário, dado seu email e senha """
        if not email:
            raise ValueError('O email é um campo obrigatório!')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """ Cria e salva um usuário comum da aplicação """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """ Cria e salva um super usuário, com todas as permissões do admin """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = None
    first_name = models.CharField("Nome", max_length=30)
    last_name = models.CharField("Sobrenome", max_length=100)
    email = models.EmailField("E-mail", max_length=255, unique=True)
    cpf = BRCPFField("CPF")
    birth_date = models.DateField("Data de nascimento", blank=True, null=True)
    phone_number = models.CharField("Número de celular", max_length=15, blank=True, null=True)

    receive_future_promotional_emails = models.BooleanField("Receber promoções futuras por email", default=False,
                                                            help_text='Caso seja falso, não enviar emails pro usuário')
    provide_data_to_improve_user_exp = models.BooleanField("Fornecer dados para melhorar a experiência", default=False,
                                                           help_text='Caso seja falso, não usar dados do usuário')

    is_staff = models.BooleanField("Membro da equipe", default=False,
                                   help_text='Define se o usuário tem acesso ao admin')
    is_active = models.BooleanField("Ativo", default=False, help_text='Define se o usuário ativou a conta no email')

    date_joined = models.DateTimeField("Criação", auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'cpf']

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name


class PasswordResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)


class VerifyEmailToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
