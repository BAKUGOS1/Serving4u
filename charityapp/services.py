import razorpay
from django.conf import settings
from .models import login_table, detail_table, event_table, volunteer_applications

class AuthService:
    @staticmethod
    def authenticate_user(email, password):
        try:
            user = login_table.objects.get(email=email)
            if user.check_password(password):
                # If password was stored as plain text, upgrade it to secure hash transparently
                if user.password == password:
                    user.set_password(password)
                    user.save(update_fields=['password'])
                return user
        except login_table.DoesNotExist:
            return None
        return None

    @staticmethod
    def register_user(name, email, password, phone, role):
        user = login_table(
            name=name,
            email=email,
            phone_no=phone,
            role=role,
            status="0" if role == "NGO" else "1"
        )
        user.set_password(password)
        user.save()
        return user

class PaymentService:
    @staticmethod
    def create_razorpay_order(amount_in_rupees):
        try:
            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )
            amount_in_paise = int(float(amount_in_rupees) * 100)
            payment = client.order.create({
                'amount': amount_in_paise,
                'currency': 'INR',
                'payment_capture': '1'
            })
            return payment
        except Exception:
            return None

class ContextService:
    @staticmethod
    def get_user_session_context(request):
        ngo = False
        profiledata = None
        user = None
        try:
            uid = request.session.get('log_id')
            if uid:
                user = login_table.objects.filter(id=uid).first()
                if user and user.role == "NGO":
                    ngo = True
                if uid:
                    profiledata = detail_table.objects.filter(login_id=uid).first()
        except Exception:
            pass
        return {'ngo': ngo, 'profiledata': profiledata, 'user': user}
