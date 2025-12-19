class TokenObtainingError(Exception):
    """Raised when OAuth token cannot be obtained from PayPal"""

    def __init__(self, message: str = "Token obtaining failed", status_code: int = 401):
        self.message = message
        super().__init__(message)


class OrderCreationFailed(Exception):
    """Raised when order cannot be created on PayPal"""

    def __init__(self, message: str = "Order creation failed", status_code: int = 400):
        self.message = message
        super().__init__(message)


class CaptureOrderFailed(Exception):
    """Raised when order cannot be captured on PayPal"""
    def __init__(self, message: str = "Order capture failed", status_code: int = 400):
        self.message = message
        super().__init__(message)

