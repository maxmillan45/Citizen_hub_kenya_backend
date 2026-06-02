from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Phone number is required')
        user = self.model(phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    national_id_hash = models.CharField(max_length=64, blank=True, null=True)
    is_id_verified = models.BooleanField(default=False)
    civic_score = models.IntegerField(default=0)
    account_type = models.CharField(max_length=20, default='free')
    language = models.CharField(max_length=5, default='en')
    created_at = models.DateTimeField(default=timezone.now)
    last_active = models.DateTimeField(auto_now=True)

    username = None
    email = None

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone_number

class MpesaTransaction(models.Model):
    checkout_request_id = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    result_code = models.IntegerField()
    result_desc = models.CharField(max_length=200)
    is_successful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.checkout_request_id} - {self.result_desc}"

# Did You Know - Kenyan History Facts
class DidYouKnowFact(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    image_alt = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=50, choices=[
        ('precolonial', 'Pre-Colonial Era'),
        ('colonial', 'Colonial Era'),
        ('independence', 'Independence Struggle'),
        ('post_independence', 'Post Independence'),
        ('culture', 'Culture & Heritage'),
        ('leaders', 'Historical Leaders'),
    ], default='post_independence')
    year = models.IntegerField(blank=True, null=True)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

# FAQ
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
        return self.question[:100]

# MP Scorecard
class MP(models.Model):
    name = models.CharField(max_length=200)
    constituency = models.CharField(max_length=200)
    party = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    image_url = models.URLField(blank=True)
    photo_url = models.URLField(blank=True)
    term_start = models.DateField()
    term_end = models.DateField()
    
    def __str__(self):
        return f"{self.name} - {self.constituency}"

class MPPerformance(models.Model):
    mp = models.ForeignKey(MP, on_delete=models.CASCADE, related_name='performances')
    year = models.IntegerField()
    attendance = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    bills_sponsored = models.IntegerField(default=0)
    bills_passed = models.IntegerField(default=0)
    motions_contributed = models.IntegerField(default=0)
    questions_asked = models.IntegerField(default=0)
    projects_completed = models.IntegerField(default=0)
    projects_ongoing = models.IntegerField(default=0)
    projects_delayed = models.IntegerField(default=0)
    grade = models.CharField(max_length=2, choices=[
        ('A', 'Excellent'),
        ('B', 'Good'),
        ('C', 'Average'),
        ('D', 'Poor'),
        ('F', 'Very Poor'),
    ], default='C')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['mp', 'year']

# Crime Report
class CrimeReport(models.Model):
    CATEGORY_CHOICES = [
        ('theft', 'Theft / Robbery'),
        ('assault', 'Assault / GBV'),
        ('corruption', 'Corruption / Bribery'),
        ('land', 'Land Dispute'),
        ('police', 'Police Misconduct'),
        ('domestic', 'Domestic Violence'),
        ('cyber', 'Cybercrime'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('reviewing', 'Under Review'),
        ('authorities', 'With Authorities'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    ]
    ANONYMITY_CHOICES = [
        ('full', 'Fully Anonymous'),
        ('pseudo', 'Pseudonymous'),
        ('public_map', 'Show on Map'),
        ('named', 'Named'),
    ]
    
    reference_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    location_description = models.TextField()
    incident_time = models.DateTimeField()
    description = models.TextField()
    evidence_photo = models.URLField(blank=True, null=True)
    evidence_video = models.URLField(blank=True, null=True)
    witness_name = models.CharField(max_length=200, blank=True)
    witness_phone = models.CharField(max_length=15, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='submitted')
    anonymity = models.CharField(max_length=20, choices=ANONYMITY_CHOICES, default='full')
    is_visible_on_map = models.BooleanField(default=False)
    police_station = models.CharField(max_length=200, blank=True)
    officer_badge = models.CharField(max_length=50, blank=True)
    resolution_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.reference_number:
            import random
            import string
            self.reference_number = f"CR-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.reference_number} - {self.category}"

# Voting Record
class VotingRecord(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='votes')
    election_name = models.CharField(max_length=200)
    election_date = models.DateField()
    polling_station = models.CharField(max_length=200)
    has_voted = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'election_name']

# Public Event
class PublicEvent(models.Model):
    EVENT_TYPES = [
        ('national', 'National Holiday'),
        ('county', 'County Event'),
        ('participation', 'Public Participation'),
        ('community', 'Community Event'),
    ]
    name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    description = models.TextField()
    event_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    county = models.CharField(max_length=100)
    location = models.CharField(max_length=300)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class EventAttendance(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='events_attended')
    event = models.ForeignKey(PublicEvent, on_delete=models.CASCADE, related_name='attendees')
    checked_in_at = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    check_in_method = models.CharField(max_length=20, choices=[
        ('gps', 'GPS Location'),
        ('qr', 'QR Code'),
        ('manual', 'Manual'),
    ], default='gps')
    verified = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['user', 'event']
