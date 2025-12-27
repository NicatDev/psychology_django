from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, About, Contact, ContactInfo, Plan, Tag, Blog

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        widgets = {
            'password': forms.PasswordInput(), # Şifrə nöqtə-nöqtə görünsün
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"]) # Şifrəni təhlükəsiz kodlaşdırır
        if commit:
            user.save()
        return user

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm # Yeni user əlavə edəndə bu sadə form çıxsın
    model = CustomUser
    
    list_display = ('email', 'username', 'is_staff', 'active_test_count')
    
    # Yeni istifadəçi əlavə etmə səhifəsində görünəcək sahələr
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password'),
        }),
    )

    # Mövcud istifadəçini redaktə etmə səhifəsi
    fieldsets = (
        ("General", {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "phone_number")}),
        ("Tests info", {"fields": ("active_test_count",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    readonly_fields = ('last_login', 'date_joined', 'username')
    ordering = ('email',)

admin.site.register(Contact)
admin.site.register(ContactInfo)
admin.site.register(About)
admin.site.register(Plan)
admin.site.register(Tag)
admin.site.register(Blog)