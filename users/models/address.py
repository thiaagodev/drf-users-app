from django.db import models
from users.models import User
from localflavor.br.models import BRPostalCodeField, BRStateField


class Address(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Usuário dono do endereço")
    country = models.CharField("País", max_length=100, blank=False, null=False)
    state = BRStateField("Estado", blank=False, null=False)
    postal_code = BRPostalCodeField("CEP", blank=False, null=False)
    city = models.CharField("Cidade", max_length=100, blank=False, null=False)
    district = models.CharField("Bairro", max_length=100, blank=False, null=False)
    street = models.CharField("Rua", max_length=100, blank=False, null=False)
    number = models.IntegerField("Número", blank=False, null=False)
    complement = models.CharField("Complemento", max_length=100, blank=True, null=True)

    def __str__(self):
        return f'Endereço {self.id} do usuário {self.owner.email}'

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"
