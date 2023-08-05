from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User, OTPCode


@admin.register(OTPCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'valid_to')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('min_profile_img', 'first_name', 'phone_number', 'email', 'is_admin', 'is_superuser')
    empty_value_display = '-'
    list_filter = ('is_admin',)
    readonly_fields = ('last_login',)

    fieldsets = (
        ('Main', {'fields':
            (
                'profile_img',
                ('first_name', 'last_name'),
                ('phone_number', 'email')
                , 'password'
            )}),
        ('Permissions',
         {'fields': ('is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {'fields': ('profile_img', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')}),
    )

    search_fields = ('email', 'phone_number')
    ordering = ('first_name', 'last_name')
    filter_horizontal = ('groups', 'user_permissions')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form
