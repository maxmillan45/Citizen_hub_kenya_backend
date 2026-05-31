from django.conf import settings
from django.core.cache import cache
from mpesakit import MpesaGateway

class MPesaAuth:
    def __init__(self):
        self.environment = getattr(settings, 'MPESA_ENVIRONMENT', 'sandbox')
        
        # Initialize Mpesa Gateway
        self.mpesa = MpesaGateway(
            environment=self.environment,
            consumer_key=settings.MPESA_CONSUMER_KEY,
            consumer_secret=settings.MPESA_CONSUMER_SECRET,
            shortcode=settings.MPESA_SHORTCODE,
            passkey=settings.MPESA_PASSKEY,
            callback_url=settings.MPESA_CALLBACK_URL
        )
    
    def stk_push(self, phone_number):
        """
        Send STK push for KES 0 authentication
        Returns checkout_request_id
        """
        # Format phone number: 254712345678 (no leading 0 or +)
        formatted_number = phone_number
        if formatted_number.startswith('0'):
            formatted_number = '254' + formatted_number[1:]
        elif formatted_number.startswith('+'):
            formatted_number = formatted_number[1:]
        
        # Send STK push with amount 0
        response = self.mpesa.stk_push(
            phone_number=formatted_number,
            amount=0,
            account_reference="CITIZEN_HUB_AUTH",
            transaction_desc="Identity Verification"
        )
        
        if response.get('ResponseCode') == '0':
            return {
                'success': True,
                'checkout_request_id': response.get('CheckoutRequestID'),
                'response_description': response.get('ResponseDescription')
            }
        else:
            return {
                'success': False,
                'error': response.get('ResponseDescription', 'Unknown error')
            }
    
    def query_status(self, checkout_request_id):
        """Query status of STK push"""
        response = self.mpesa.stk_query(checkout_request_id=checkout_request_id)
        
        return response
