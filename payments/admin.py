from django.contrib import admin
from .models import Payment
# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "user_email",
        "plan",
        "amount",
        "currency",
        "status",
        "created_at",
    )

    list_filter = ("status", "currency", "created_at")
    search_fields = ("user__email", "paypal_order_id")
    ordering = ("-created_at",)

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "User Email"