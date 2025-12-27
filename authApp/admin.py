from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, About, Contact, ContactInfo, Plan, Tag, Blog

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',) # Formda yalnız email görünsün

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields['username'].label = "Email (Username)" # Adını dəyişirik
            self.fields['username'].help_text = "Sistemə giriş üçün email ünvanınızı daxil edin."

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm # Yeni user yaradanda bu form işləsin
    
    model = CustomUser
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'active_test_count')
    
    # Redaktə səhifəsi (Change view)
    fieldsets = (
        ("General", {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "phone_number")}),
        ("Tests info", {"fields": ("active_test_count",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    
    readonly_fields = ('last_login', 'date_joined')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Contact)
admin.site.register(ContactInfo)
admin.site.register(About)
admin.site.register(Plan)
admin.site.register(Tag)
admin.site.register(Blog)