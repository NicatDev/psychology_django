from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from authApp.models import Plan
from payments.models import Payment
from payments.services.paypal import create_order
from .serializers import PaymentSerializer

class BuyPlanAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plan_id = request.data.get("plan_id")

        plan = get_object_or_404(Plan, id=plan_id, is_active=True)

        order = create_order(plan.price)

        Payment.objects.create(
            user=request.user,
            plan=plan,
            amount=plan.price,
            currency=plan.currency,
            paypal_order_id=order["id"],
            status="CREATED",
        )

        approve_url = next(
            link["href"] for link in order["links"]
            if link["rel"] == "approve"
        )

        return Response({
            "order_id": order["id"],
            "approve_url": approve_url
        })


from django.shortcuts import redirect
from payments.services.paypal import capture_order
from rest_framework import status

class PaypalSuccessView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order_id = request.GET.get("token")
        payment = get_object_or_404(
            Payment,
            paypal_order_id=order_id,
            status="CREATED"
        )
        if payment.status == "COMPLETED":
            # Artıq ödəniş tamamlanıb, ikinci dəfə capture etməyə ehtiyac yoxdur
            return Response(
                {"detail": "Payment has already been processed."},
                status=200
            )

        if payment.status != "CREATED":
            # Əgər status CREATED deyilsə, başqa bir problem ola bilər
            return Response(
                {"detail": "Payment cannot be processed."},
                status=400
            )
        capture = capture_order(order_id)
        if capture["status"] == "COMPLETED":
            payment.status = "COMPLETED"
            payment.save()

            user = payment.user
            user.active_test_count += payment.plan.tests_count
            user.save()
            return Response(
                {"order_id": order_id, "detail": "Payment completed successfully!"},
                status=status.HTTP_200_OK
            )
        return Response(
            {"order_id": order_id, "detail": "Payment failed."},
            status=status.HTTP_400_BAD_REQUEST
        )

class MyPaymentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(user=request.user).order_by('-created_at')
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)