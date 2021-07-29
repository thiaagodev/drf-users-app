from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User, Address


class AddressInline(admin.TabularInline):
    model = Address
    can_delete = False
    readonly_fields = ('id', 'owner', 'country', 'state', 'postal_code', 'city', 'district', 'street', 'number', 'complement')

    def has_add_permission(self, request, obj):
        return False


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """ Definindo um modelo de admin personalizado pro modelo de usuário """

    readonly_fields = ('date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password',
                           'receive_future_promotional_emails', 'provide_data_to_improve_user_exp')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'cpf', 'birth_date', 'phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'cpf'),
        }),
    )
    list_display = ('id', 'email', 'first_name', 'last_name', 'cpf',
                    'is_staff', 'receive_future_promotional_emails', 'provide_data_to_improve_user_exp')
    list_display_links = ('id', 'email')
    search_fields = ('email', 'first_name', 'last_name', 'cpf')
    ordering = ('email',)
    inlines = [AddressInline]
    list_per_page = 10


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'country', 'state', 'postal_code', 'city', 'district',
                    'street', 'number', 'complement')
    list_display_links = ('id', 'owner')
    list_per_page = 10
    search_fields = ('id', 'owner', 'owner_email', 'city', 'street', 'state')

    list_filter = ('country', 'state')

