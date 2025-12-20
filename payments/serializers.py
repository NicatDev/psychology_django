from rest_framework import serializers
from authApp.serializers import PlanListSerializer
from .models import Payment

class BuyPlanSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()


class PaymentSerializer(serializers.ModelSerializer):
    plan = PlanListSerializer()  # Nested serializer, plan haqqında məlumat verir

    class Meta:
        model = Payment
        fields = ['id', 'plan', 'amount', 'currency', 'paypal_order_id', 'status', 'created_at']