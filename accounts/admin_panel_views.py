from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta, datetime
from django.contrib.auth import get_user_model
from .models import CrimeReport, FAQ, MP, PublicEvent, MpesaTransaction
from chatbot.models import Conversation
from constitution.models import Article
from scraper.models import ScrapingLog
import json

User = get_user_model()

class AdminDashboardStatsView(APIView):
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
        investigating_crimes = CrimeReport.objects.filter(status='investigating').count()
        resolved_crimes = CrimeReport.objects.filter(status='resolved').count()
        dismissed_crimes = CrimeReport.objects.filter(status='dismissed').count()
        crimes_week = CrimeReport.objects.filter(created_at__gte=week_ago).count()
        crimes_by_category = CrimeReport.objects.values('category').annotate(count=Count('id'))
        
        # FAQ statistics
        total_faqs = FAQ.objects.count()
        most_viewed_faqs = FAQ.objects.order_by('-views')[:5].values('question', 'views', 'helpful_count')
        
        # Chatbot statistics
        total_conversations = Conversation.objects.count()
        conversations_week = Conversation.objects.filter(created_at__gte=week_ago).count()
        
        # Constitution
        total_articles = Article.objects.count()
        
        # MPs
        total_mps = MP.objects.count()
        
        # Events
        total_events = PublicEvent.objects.count()
        upcoming_events = PublicEvent.objects.filter(date__gte=now).count()
        
        # Payments
        total_payments = MpesaTransaction.objects.filter(is_completed=True).count()
        total_payment_amount = MpesaTransaction.objects.filter(is_completed=True).aggregate(Sum('amount'))['amount__sum'] or 0
        payments_week = MpesaTransaction.objects.filter(created_at__gte=week_ago, is_completed=True).count()
        
        # Scraping stats
        last_scrape = ScrapingLog.objects.filter(status='success').order_by('-completed_at').first()
        
        # Recent activity
        recent_users = User.objects.order_by('-date_joined')[:5].values('phone_number', 'date_joined')
        recent_crimes = CrimeReport.objects.order_by('-created_at')[:5].values('category', 'status', 'created_at')
        recent_conversations = Conversation.objects.order_by('-created_at')[:5].values('question', 'created_at')
        
        stats = {
            'users': {
                'total': total_users,
                'new_today': new_users_today,
                'new_week': new_users_week,
                'new_month': new_users_month,
                'active_week': active_users,
            },
            'crime_reports': {
                'total': total_crimes,
                'pending': pending_crimes,
                'investigating': investigating_crimes,
                'resolved': resolved_crimes,
                'dismissed': dismissed_crimes,
                'this_week': crimes_week,
                'by_category': crimes_by_category,
            },
            'faqs': {
                'total': total_faqs,
                'most_viewed': most_viewed_faqs,
            },
            'chatbot': {
                'total_conversations': total_conversations,
                'this_week': conversations_week,
            },
            'constitution': {
                'total_articles': total_articles,
            },
            'mps': {
                'total': total_mps,
            },
            'events': {
                'total': total_events,
                'upcoming': upcoming_events,
            },
            'payments': {
                'total': total_payments,
                'total_amount': float(total_payment_amount),
                'this_week': payments_week,
            },
            'scraping': {
                'last_scrape': last_scrape.completed_at.isoformat() if last_scrape else None,
                'last_scrape_status': last_scrape.status if last_scrape else 'never',
            },
            'recent_activity': {
                'new_users': recent_users,
                'recent_crimes': recent_crimes,
                'recent_chatbot': recent_conversations,
            },
            'timestamp': now.isoformat(),
        }
        
        return Response(stats)


class AdminUsersListView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        search = request.query_params.get('search', '')
        status_filter = request.query_params.get('status', '')
        
        users = User.objects.all().order_by('-date_joined')
        
        if search:
            users = users.filter(
                Q(phone_number__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        if status_filter == 'active':
            users = users.filter(is_active=True)
        elif status_filter == 'inactive':
            users = users.filter(is_active=False)
        
        total = users.count()
        start = (page - 1) * page_size
        end = start + page_size
        
        data = []
        for user in users[start:end]:
            data.append({
                'id': user.id,
                'phone_number': user.phone_number,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'civic_score': user.civic_score,
                'account_type': user.account_type,
                'language': user.language,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'date_joined': user.date_joined.isoformat(),
                'last_login': user.last_login.isoformat() if user.last_login else None,
            })
        
        return Response({
            'users': data,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        })
    
    def patch(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'User ID required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        updates = {}
        if 'is_active' in request.data:
            user.is_active = request.data['is_active']
            updates['is_active'] = user.is_active
        if 'account_type' in request.data:
            user.account_type = request.data['account_type']
            updates['account_type'] = user.account_type
        if 'civic_score' in request.data:
            user.civic_score = request.data['civic_score']
            updates['civic_score'] = user.civic_score
        if 'is_staff' in request.data:
            user.is_staff = request.data['is_staff']
            updates['is_staff'] = user.is_staff
        if 'is_superuser' in request.data:
            user.is_superuser = request.data['is_superuser']
            updates['is_superuser'] = user.is_superuser
        
        user.save()
        
        return Response({
            'message': 'User updated successfully',
            'updates': updates
        })
    
    def delete(self, request):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'User ID required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        return Response({'message': 'User deleted successfully'})


class AdminCrimeReportsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        status_filter = request.query_params.get('status', '')
        category_filter = request.query_params.get('category', '')
        
        reports = CrimeReport.objects.all().order_by('-created_at')
        
        if status_filter:
            reports = reports.filter(status=status_filter)
        if category_filter:
            reports = reports.filter(category=category_filter)
        
        total = reports.count()
        start = (page - 1) * page_size
        end = start + page_size
        
        data = []
        for report in reports[start:end]:
            data.append({
                'id': report.id,
                'category': report.category,
                'description': report.description,
                'location': report.location,
                'status': report.status,
                'reported_by': {
                    'id': report.reported_by.id,
                    'phone_number': report.reported_by.phone_number,
                } if report.reported_by else None,
                'created_at': report.created_at.isoformat(),
                'updated_at': report.updated_at.isoformat(),
            })
        
        return Response({
            'reports': data,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        })
    
    def patch(self, request):
        report_id = request.data.get('report_id')
        if not report_id:
            return Response({'error': 'Report ID required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            report = CrimeReport.objects.get(id=report_id)
        except CrimeReport.DoesNotExist:
            return Response({'error': 'Report not found'}, status=status.HTTP_404_NOT_FOUND)
        
        status_value = request.data.get('status')
        if status_value and status_value in ['pending', 'investigating', 'resolved', 'dismissed']:
            report.status = status_value
            report.save()
            return Response({
                'message': 'Report status updated',
                'new_status': report.status
            })
        
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)


class AdminFAQsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        category_filter = request.query_params.get('category', '')
        
        faqs = FAQ.objects.all().order_by('-created_at')
        
        if category_filter:
            faqs = faqs.filter(category=category_filter)
        
        total = faqs.count()
        start = (page - 1) * page_size
        end = start + page_size
        
        data = []
        for faq in faqs[start:end]:
            data.append({
                'id': faq.id,
                'question': faq.question,
                'answer': faq.answer,
                'category': faq.category,
                'views': faq.views,
                'helpful_count': faq.helpful_count,
                'not_helpful_count': faq.not_helpful_count,
                'created_at': faq.created_at.isoformat(),
            })
        
        return Response({
            'faqs': data,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        })


class AdminPaymentsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        status_filter = request.query_params.get('status', '')
        
        payments = MpesaTransaction.objects.all().order_by('-created_at')
        
        if status_filter == 'completed':
            payments = payments.filter(is_completed=True)
        elif status_filter == 'pending':
            payments = payments.filter(is_completed=False)
        
        total = payments.count()
        start = (page - 1) * page_size
        end = start + page_size
        
        data = []
        for payment in payments[start:end]:
            data.append({
                'id': payment.id,
                'phone_number': payment.phone_number,
                'amount': float(payment.amount),
                'account_reference': payment.account_reference,
                'is_completed': payment.is_completed,
                'mpesa_receipt_number': payment.mpesa_receipt_number,
                'response_code': payment.response_code,
                'response_description': payment.response_description,
                'created_at': payment.created_at.isoformat(),
            })
        
        total_amount = payments.filter(is_completed=True).aggregate(Sum('amount'))['amount__sum'] or 0
        
        return Response({
            'payments': data,
            'total': total,
            'total_amount': float(total_amount),
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        })


class AdminChatbotView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        
        conversations = Conversation.objects.all().order_by('-created_at')
        total = conversations.count()
        start = (page - 1) * page_size
        end = start + page_size
        
        data = []
        for conv in conversations[start:end]:
            data.append({
                'id': conv.id,
                'user': {
                    'id': conv.user.id,
                    'phone_number': conv.user.phone_number,
                } if conv.user else None,
                'question': conv.question,
                'answer': conv.answer[:500] + '...' if len(conv.answer) > 500 else conv.answer,
                'language': conv.language,
                'sources': conv.sources,
                'helpful': conv.helpful,
                'created_at': conv.created_at.isoformat(),
            })
        
        return Response({
            'conversations': data,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size
        })


class AdminScrapingView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        logs = ScrapingLog.objects.all().order_by('-started_at')
        
        data = []
        for log in logs[:50]:
            data.append({
                'id': log.id,
                'source': log.source,
                'status': log.status,
                'items_scraped': log.items_scraped,
                'error_message': log.error_message,
                'started_at': log.started_at.isoformat(),
                'completed_at': log.completed_at.isoformat() if log.completed_at else None,
            })
        
        return Response({
            'logs': data,
            'total': logs.count()
        })
    
    def post(self, request):
        source = request.data.get('source', 'all')
        
        from django.core.management import call_command
        from io import StringIO
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            call_command('scrape_data', source=source)
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            return Response({
                'message': 'Scraping triggered successfully',
                'output': output,
                'source': source
            })
        except Exception as e:
            sys.stdout = old_stdout
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminSystemSettingsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        from django.conf import settings
        
        return Response({
            'debug': settings.DEBUG,
            'allowed_hosts': settings.ALLOWED_HOSTS,
            'cors_allowed_origins': getattr(settings, 'CORS_ALLOWED_ORIGINS', []),
            'api_version': 'v1',
            'maintenance_mode': getattr(settings, 'MAINTENANCE_MODE', False),
            'timezone': settings.TIME_ZONE,
            'db_engine': settings.DATABASES['default']['ENGINE'],
        })
    
    def post(self, request):
        maintenance_mode = request.data.get('maintenance_mode')
        if maintenance_mode is not None:
            from django.conf import settings
            settings.MAINTENANCE_MODE = maintenance_mode
            return Response({'message': f'Maintenance mode set to {maintenance_mode}'})
        
        return Response({'error': 'Invalid setting'}, status=status.HTTP_400_BAD_REQUEST)
