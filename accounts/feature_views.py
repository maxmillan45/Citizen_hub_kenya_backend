from django.utils import timezone
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import DidYouKnowFact, FAQ, MP, PublicEvent, CrimeReport, VotingRecord
from .serializers import (
    DidYouKnowFactSerializer, FAQSerializer, MPSerializer, 
    PublicEventSerializer, CrimeReportSerializer, VotingRecordSerializer
)

class DidYouKnowListView(generics.ListAPIView):
    queryset = DidYouKnowFact.objects.all()
    serializer_class = DidYouKnowFactSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'year']
    search_fields = ['title', 'content']
    ordering_fields = ['year', 'created_at']
    ordering = ['-year']

class FAQListView(generics.ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['question', 'answer']
    ordering_fields = ['created_at', 'question', 'views']
    ordering = ['-created_at']

class MPListView(generics.ListAPIView):
    queryset = MP.objects.all()
    serializer_class = MPSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['party', 'constituency']
    search_fields = ['name', 'constituency', 'party']
    ordering_fields = ['name', 'party', 'constituency']
    ordering = ['name']

class EventListView(generics.ListAPIView):
    queryset = PublicEvent.objects.all()
    serializer_class = PublicEventSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'location', 'is_free']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['date', 'created_at']
    ordering = ['date']

class CrimeReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = CrimeReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reported_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def get(self, request):
        reports = CrimeReport.objects.filter(reported_by=request.user)
        serializer = CrimeReportSerializer(reports, many=True)
        return Response(serializer.data)

class VotingStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        voting_records = VotingRecord.objects.filter(user=request.user)
        serializer = VotingRecordSerializer(voting_records, many=True)
        return Response(serializer.data)
