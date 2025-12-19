"# psychology_django" 

## PayPal İnteqrasiyası

PayPal inteqrasiyası `payments/` modulunda Command pattern ilə implement edilib. Clean architecture prinsiplərinə əsasən qurulub - yeni endpoint əlavə etmək asandır, hər şey aydın strukturdadır.

### Necə işləyir?

3 əsas komanda var:

- **GetToken** - PayPal OAuth token alır (amma bu sənə lazım olmayacaq, avtomatik işləyir)
- **CreateOrder** - Ödəniş sifarişi yaradır, user'ə link qaytarır
- **CaptureOrder** - User ödədikdən sonra pulu çəkir

Token managementini düşünməyə ehtiyac yoxdur. Django cache'də saxlanılır, avtomatik expire olur və yenilənir.

### Setup

`.env` faylı yarat (`.env.example`'a bax):

```env
PAYPAL_MODE=sandbox
PAYPAL_SANDBOX_CLIENT_ID=your_client_id_here
PAYPAL_SANDBOX_CLIENT_SECRET=your_secret_here
PAYPAL_RETURN_URL=http://localhost:8000/payment/success
PAYPAL_CANCEL_URL=http://localhost:8000/payment/cancel
```

Production'da `PAYPAL_MODE=live` et və live credentials ver.

### Praktiki istifadə

Məsələn, View'da belə istifadə edirsən:

```python
from payments.paypal.commands import CreateOrder, CaptureOrder
from payments.paypal.utils import gen_idempotency_key

# Sifariş yarat
order = CreateOrder.instance(
    amount=29.99,
    idempotency_key=gen_idempotency_key(("user_123", "plan_5"))
).execute()

# User'i bu URL'ə redirect et
# order.payer_action_link
# yaxud front app response üçün order.to_json() et

# PayPal'dan geri qayıdanda (PAYPAL_RETURN_URL yanında "token" query param ilə birlikdə gəlir)
token = request.query("token")
captured = CaptureOrder.instance(order_id=token).execute()
# CaptureOrderFailed exception'ı gözlə

# captured.status == "COMPLETED"
# captured.capture_id - bu transaction ID'dir, DB'də saxla
```

### Idempotency

Write əməliyyatlarını (sifariş yaratmaq və s.) race condition və s. digər səbəblərə görə birdən çox dəfə etməmək 
üçün idempotency key istifadə et:

```python
from payments.paypal.utils import gen_idempotency_key

# User ID və plan ID'dən unique key yaradır
# "prefix" vacib deyil, sadəcə etiket mahiyyəti daşıyır
key = gen_idempotency_key(("user_123", "plan_premium"), prefix="order")

order = CreateOrder.instance(amount=29.99, idempotency_key=key).execute()
```

Eyni key ilə 2-ci dəfə CreateOrder çağırsan - PayPal eyni sifarişi qaytaracaq, yeni yaratmayacaq.

### Arxitektura

Command pattern var:
- `payments/paypal/interfaces.py` - Interface'lər (Command, NeedsAuthorization, HasBody, Idempotent)
- `payments/paypal/executor.py` - HTTP request göndərir, token inject edir
- `payments/paypal/commands.py` - Konkret komandalar (GetToken, CreateOrder, CaptureOrder)
- `payments/paypal/dto.py` - Response'ları Pydantic modellərinə map edir
- `payments/paypal/utils.py` - Token cache, idempotency key generator

Yeni endpoint lazım olsa - command yaz, execute et. Executor avtomatik header'ləri, authorization'ı, body'ni düzəldəcək.

### Yeni endpoint əlavə etmək

1. DTO əlavə et (`payments/paypal/dto.py`):
```python
class RefundResponse(DTO):
    refund_id: str
    status: str

    @classmethod
    def from_response(cls, response: dict):
        return cls(refund_id=response['id'], status=response['status'])
```

2. Command yaz (`payments/paypal/commands.py`):
```python
class RefundPayment(Command, NeedsAuthorization, HasBody):
    pass
```

3. İstifadə et:
```python
result = RefundPayment.instance(capture_id="xxx", amount=29.99).execute()
```

### Sandbox mode

Development'də sandbox mode var:
- Proxy enabled (localhost:8080) - Burp Suite və s. üçün
- SSL verification disabled
- Test kredit kartları işləyir

`PAYPAL_CLIENT_PROXY_ENABLED=False` edə bilərsən `.env`'də.

---

**TL;DR**: CreateOrder.instance().execute() et, user'i linkə göndər, geri qayıdanda CaptureOrder.instance().execute() et. Bu qədər.
Unutma ki, CreateOrder'dan alıb yönləndirdiyin `payer_action_link`də istifadəçi ödəniş etmir, "sifarişi qəbul edir".
Qısaca, "qəbul"dan sonra CaptureOrder etməsən, istifadəçi hesabında bloklanmış ödəniş satıcının hesabına transfer olmaz.
