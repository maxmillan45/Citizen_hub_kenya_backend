from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Phone number is required')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=15, unique=True)
    national_id_hash = models.CharField(max_length=255, blank=True, null=True)
    is_id_verified = models.BooleanField(default=False)
    civic_score = models.IntegerField(default=0)
    account_type = models.CharField(max_length=20, default='free')
    language = models.CharField(max_length=5, default='en')
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return self.phone_number

class MpesaTransaction(models.Model):
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account_reference = models.CharField(max_length=50)
    transaction_desc = models.CharField(max_length=100)
    checkout_request_id = models.CharField(max_length=100, unique=True)
    response_code = models.CharField(max_length=10)
    response_description = models.CharField(max_length=200)
    result_code = models.CharField(max_length=10, blank=True, null=True)
    result_description = models.CharField(max_length=200, blank=True, null=True)
    mpesa_receipt_number = models.CharField(max_length=50, blank=True, null=True)
    transaction_date = models.CharField(max_length=20, blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.phone_number} - {self.amount} - {self.checkout_request_id}"

class DidYouKnowFact(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50)
    year = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('arrest', 'Arrest & Police'),
        ('land', 'Land & Property'),
        ('employment', 'Employment'),
        ('health', 'Health'),
        ('education', 'Education'),
        ('family', 'Family'),
        ('corruption', 'Corruption'),
        ('voting', 'Voting'),
        ('technology', 'Technology'),
        ('other', 'Other'),
    ]
    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    views = models.IntegerField(default=0)
    helpful_count = models.IntegerField(default=0)
    not_helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question[:50]

class MP(models.Model):
    name = models.CharField(max_length=200)
    constituency = models.CharField(max_length=200)
    party = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    photo_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class MPPerformance(models.Model):
    mp = models.ForeignKey(MP, on_delete=models.CASCADE)
    year = models.IntegerField()
    attendance = models.FloatField(default=0)
    questions_asked = models.IntegerField(default=0)
    motions_sponsored = models.IntegerField(default=0)
    bills_sponsored = models.IntegerField(default=0)
    projects_completed = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.mp.name} - {self.year}"

class CrimeReport(models.Model):
    CATEGORY_CHOICES = [
        ('theft', 'Theft'),
        ('assault', 'Assault'),
        ('corruption', 'Corruption'),
        ('land_dispute', 'Land Dispute'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.category} - {self.location}"

class VotingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    election_type = models.CharField(max_length=50)
    voted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='completed')
    
    def __str__(self):
        return f"{self.user.phone_number} - {self.election_type}"

class PublicEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    organizer = models.CharField(max_length=100, blank=True, null=True)
    is_free = models.BooleanField(default=True)
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class EventAttendance(models.Model):
    event = models.ForeignKey(PublicEvent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attended_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.phone_number} - {self.event.title}"
