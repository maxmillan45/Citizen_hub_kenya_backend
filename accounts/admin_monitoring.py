from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from .models import CrimeReport, FAQ, MP, PublicEvent, MpesaTransaction
from .serializers import UserSerializer, CrimeReportSerializer, FAQSerializer

User = get_user_model()

class DashboardStatsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        
        total_users = User.objects.count()
        new_users_week = User.objects.filter(date_joined__gte=week_ago).count()
        
        total_crimes = CrimeReport.objects.count()
        pending_crimes = CrimeReport.objects.filter(status='pending').count()
        
        total_faqs = FAQ.objects.count()
        total_mps = MP.objects.count()
        total_events = PublicEvent.objects.count()
        
        stats = {
            'users': {
                'total': total_users,
                'new_this_week': new_users_week,
            },
            'crime_reports': {
                'total': total_crimes,
                'pending': pending_crimes,
            },
            'faqs': {
                'total': total_faqs,
            },
            'mps': {
                'total': total_mps,
            },
            'events': {
                'total': total_events,
            },
            'timestamp': now.isoformat(),
        }
        
        return Response(stats)


class UserManagementView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        users = User.objects.all().order_by('-date_joined')
        
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        start = (page - 1) * page_size
        end = start + page_size
        
        search = request.query_params.get('search')
        if search:
            users = users.filter(
                Q(phone_number__icontains=search) |
                Q(email__icontains=search)
            )
        
        total = users.count()
        paginated_users = users[start:end]
        
        data = [{
            'id': user.id,
            'phone_number': user.phone_number,
            'email': user.email,
            'civic_score': user.civic_score,
            'account_type': user.account_type,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
        } for user in paginated_users]
        
        return Response({
            'users': data,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        })
    
    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        if 'is_active' in data:
            user.is_active = data['is_active']
        if 'account_type' in data:
            user.account_type = data['account_type']
        if 'civic_score' in data:
            user.civic_score = data['civic_score']
        
        user.save()
        return Response({'message': 'User updated successfully'})


class CrimeReportManagementView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        reports = CrimeReport.objects.all().order_by('-created_at')
        
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        start = (page - 1) * page_size
        end = start + page_size
        
        status_filter = request.query_params.get('status')
        if status_filter:
            reports = reports.filter(status=status_filter)
        
        total = reports.count()
        paginated_reports = reports[start:end]
        
        data = [{
            'id': report.id,
            'category': report.category,
            'description': report.description,
            'location': report.location,
            'status': report.status,
            'reported_by': report.reported_by.phone_number if report.reported_by else None,
            'created_at': report.created_at,
        } for report in paginated_reports]
        
        return Response({
            'reports': data,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        })
    
    def patch(self, request, report_id):
        try:
            report = CrimeReport.objects.get(id=report_id)
        except CrimeReport.DoesNotExist:
            return Response({'error': 'Report not found'}, status=status.HTTP_404_NOT_FOUND)
        
        status_value = request.data.get('status')
        if status_value in ['pending', 'investigating', 'resolved', 'dismissed']:
            report.status = status_value
            report.save()
            return Response({'message': 'Report status updated'})
        
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)


class FAQManagementView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        faqs = FAQ.objects.all().order_by('-created_at')
        
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        start = (page - 1) * page_size
        end = start + page_size
        
        total = faqs.count()
        paginated_faqs = faqs[start:end]
        
        data = [{
            'id': faq.id,
            'question': faq.question,
            'answer': faq.answer,
            'category': faq.category,
            'views': faq.views,
            'helpful_count': faq.helpful_count,
            'not_helpful_count': faq.not_helpful_count,
            'created_at': faq.created_at,
        } for faq in paginated_faqs]
        
        return Response({
            'faqs': data,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        })
    
    def post(self, request):
        serializer = FAQSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentMonitoringView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        payments = MpesaTransaction.objects.all().order_by('-created_at')
        
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        start = (page - 1) * page_size
        end = start + page_size
        
        total = payments.count()
        paginated_payments = payments[start:end]
        
        data = [{
            'id': payment.id,
            'phone_number': payment.phone_number,
            'amount': str(payment.amount),
            'account_reference': payment.account_reference,
            'is_completed': payment.is_completed,
            'mpesa_receipt_number': payment.mpesa_receipt_number,
            'created_at': payment.created_at,
        } for payment in paginated_payments]
        
        total_amount = payments.filter(is_completed=True).aggregate(Sum('amount'))['amount__sum'] or 0
        
        return Response({
            'payments': data,
            'total': total,
            'total_amount': total_amount,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        })


class SystemSettingsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        from django.conf import settings
        
        return Response({
            'debug': settings.DEBUG,
            'allowed_hosts': settings.ALLOWED_HOSTS,
            'cors_allowed_origins': settings.CORS_ALLOWED_ORIGINS,
            'api_version': 'v1',
            'maintenance_mode': getattr(settings, 'MAINTENANCE_MODE', False),
        })
    
    def post(self, request):
        maintenance_mode = request.data.get('maintenance_mode')
        if maintenance_mode is not None:
            from django.conf import settings
            settings.MAINTENANCE_MODE = maintenance_mode
            return Response({'message': f'Maintenance mode set to {maintenance_mode}'})
        
        return Response({'error': 'Invalid setting'}, status=status.HTTP_400_BAD_REQUEST)
