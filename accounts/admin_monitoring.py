from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from .models import CrimeReport, FAQ, MP, PublicEvent, MpesaTransaction
from chatbot.models import Conversation
from constitution.models import Article

User = get_user_model()

class DashboardStatsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        now = timezone.now()
        today = now.date()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        # User statistics
        total_users = User.objects.count()
        new_users_today = User.objects.filter(date_joined__date=today).count()
        new_users_week = User.objects.filter(date_joined__gte=week_ago).count()
        new_users_month = User.objects.filter(date_joined__gte=month_ago).count()
        active_users = User.objects.filter(last_login__gte=week_ago).count()
        
        # Crime reports
        total_crimes = CrimeReport.objects.count()
        pending_crimes = CrimeReport.objects.filter(status='pending').count()
        resolved_crimes = CrimeReport.objects.filter(status='resolved').count()
        crimes_this_week = CrimeReport.objects.filter(created_at__gte=week_ago).count()
        crimes_by_category = CrimeReport.objects.values('category').annotate(count=Count('id'))
        
        # FAQ statistics
        total_faqs = FAQ.objects.count()
        most_viewed_faqs = FAQ.objects.order_by('-views')[:5].values('question', 'views')
        
        # Chatbot statistics
        total_conversations = Conversation.objects.count()
        conversations_this_week = Conversation.objects.filter(created_at__gte=week_ago).count()
        avg_response_time = Conversation.objects.aggregate(avg=Avg('response_time')) if hasattr(Conversation, 'response_time') else {'avg': 0}
        
        # Payment statistics
        total_payments = MpesaTransaction.objects.filter(is_completed=True).aggregate(
            total=Sum('amount'),
            count=Count('id')
        )
        payments_this_week = MpesaTransaction.objects.filter(
            created_at__gte=week_ago,
            is_completed=True
        ).aggregate(total=Sum('amount'), count=Count('id'))
        
        # Constitution articles
        total_articles = Article.objects.count()
        most_viewed_articles = Article.objects.order_by('-view_count')[:5].values('article_number', 'title', 'view_count')
        
        # System health
        recent_errors = Conversation.objects.filter(
            created_at__gte=week_ago,
            answer__contains='error'
        ).count() if hasattr(Conversation, 'answer') else 0
        
        data = {
            'users': {
                'total': total_users,
                'new_today': new_users_today,
                'new_this_week': new_users_week,
                'new_this_month': new_users_month,
                'active_this_week': active_users,
            },
            'crime_reports': {
                'total': total_crimes,
                'pending': pending_crimes,
                'resolved': resolved_crimes,
                'this_week': crimes_this_week,
                'by_category': crimes_by_category,
            },
            'faqs': {
                'total': total_faqs,
                'most_viewed': most_viewed_faqs,
            },
            'chatbot': {
                'total_conversations': total_conversations,
                'this_week': conversations_this_week,
                'avg_response_time': avg_response_time['avg'],
            },
            'payments': {
                'total_amount': total_payments['total'] or 0,
                'total_count': total_payments['count'] or 0,
                'weekly_amount': payments_this_week['total'] or 0,
                'weekly_count': payments_this_week['count'] or 0,
            },
            'constitution': {
                'total_articles': total_articles,
                'most_viewed': most_viewed_articles,
            },
            'system': {
                'recent_errors': recent_errors,
                'last_updated': now.isoformat(),
            }
        }
        
        return Response(data)


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
        
        status_filter = request.query_params.get('status')
        if status_filter == 'active':
            users = users.filter(is_active=True)
        elif status_filter == 'inactive':
            users = users.filter(is_active=False)
        
        total = users.count()
        paginated_users = users[start:end]
        
        data = [{
            'id': user.id,
            'phone_number': user.phone_number,
            'email': user.email,
            'civic_score': user.civic_score,
            'account_type': user.account_type,
            'is_active': user.is_active,
            'is_id_verified': user.is_id_verified,
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
        if 'is_id_verified' in data:
            user.is_id_verified = data['is_id_verified']
        
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
        
        category_filter = request.query_params.get('category')
        if category_filter:
            reports = reports.filter(category=category_filter)
        
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
        
        category_filter = request.query_params.get('category')
        if category_filter:
            faqs = faqs.filter(category=category_filter)
        
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
            'amount': payment.amount,
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
