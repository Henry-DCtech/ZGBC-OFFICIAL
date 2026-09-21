from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError
import uuid



class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    def __str__(self):
        return self.username

class Program(models.Model):
    # ... your existing Program model code
    DAY_CHOICES = [
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    day_of_week = models.CharField(max_length=20, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    host = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    
    class Meta:
        ordering = ['day_of_week', 'start_time']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.day_of_week}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} - {self.day_of_week}"

# ... keep all your other models: ContactMessage, PrayerRequest, Event, etc.

# ADD THIS AT THE BOTTOM
class WebsiteConfiguration(models.Model):
    site_name = models.CharField(max_length=100, default='ZGBC OFFICIAL')
    site_logo = models.ImageField(upload_to='config/', blank=True, null=True)
    favicon = models.ImageField(upload_to='config/', blank=True, null=True)
    
    hero_title = models.CharField(max_length=200, blank=True, default='Welcome to ZGBC OFFICIAL')
    hero_subtitle = models.TextField(blank=True, default='Your Gospel Broadcasting Network')
    hero_image = models.ImageField(upload_to='config/', blank=True, null=True)
    
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    
    facebook_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Website Configuration'
        verbose_name_plural = 'Website Configuration'
    
    def __str__(self):
        return self.site_name
    
    def clean(self):
        if not self.pk and WebsiteConfiguration.objects.exists():
            raise ValidationError('Only one Website Configuration is allowed.')
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_config(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Sermon(models.Model):
    title = models.CharField(max_length=200)
    preacher = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, blank=True)  # Add this
    sermon_date = models.DateField()
    description = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='sermons/audio/', blank=True, null=True)
    video_url = models.URLField()
    thumbnail = models.ImageField(upload_to='sermons/thumbnails/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)  # Add this
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['-sermon_date']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} - {self.preacher}"
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)  # add this
    is_read = models.BooleanField(default=False)  # optional
    is_published = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']  # add this if you add the field

   
    def __str__(self):
        return f"{self.name} - {self.subject}"

class PrayerRequest(models.Model):
    STATUS_CHOICES  = [
        ('pending', 'Pending'),
        ('praing', 'Praying'),
        ('answered', 'Answered'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    request = models.TextField()
    is_private = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    is_answered = models.BooleanField(default=False)
    is_urgent = models.BooleanField(default=False)
    is_prayed_for = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)  # Reverted
    is_published = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-submitted_at']  # Reverted
        verbose_name = "Prayer Request"
        verbose_name_plural = "Prayer Requests"
    
    def __str__(self):
        return f"Prayer from {self.name} - {self.submitted_at.date()}"
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.title} - {self.date}"
    

class RadioProgram(models.Model):
    title = models.CharField(max_length=200)
    host = models.CharField(max_length=100)
    description = models.TextField()
    schedule = models.CharField(max_length=100, help_text="e.g. Mon-Fri 6PM-8PM")
    air_time = models.TimeField(null=True, blank=True)
    stream_url = models.URLField(blank=True, help_text="Live stream URL")
    audio_file = models.FileField(upload_to='radio/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='radio/thumbnails/', blank=True, null=True)
    is_live = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_live', 'title']
        verbose_name = "Radio Program"
        verbose_name_plural = "Radio Programs"
    
    def __str__(self):
        return self.title

class DonationType(models.TextChoices):
    TITHE = 'TITHE', 'Tithe'
    OFFERING = 'OFFERING', 'Offering'
    DONATION = 'DONATION', 'General Donation'
    PROJECT = 'PROJECT', 'Special Project'

class Donation(models.Model):
    reference = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    currency = models.CharField(max_length=3, default='USD')
    email = models.EmailField()  # If this was new, keep it. Django will ask for default once.
    phone = models.CharField(max_length=20, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_type = models.CharField(
        max_length=20, 
        choices=DonationType.choices, 
        default=DonationType.DONATION
    )
    project = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    paystack_response = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - ₦{self.amount}"

class Partner(models.Model):
    PARTNER_TYPES = [
        ('individual', 'Individual'),
        ('organization', 'Organization/Church'),
        ('business', 'Business'),
        ('prayer', 'Prayer Partner'),
        ('financial', 'Financial Partner'),
        ('volunteer', 'Volunteer Partner'),
        ('building', 'Building Project'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    partner_type = models.CharField(max_length=20, choices=PARTNER_TYPES)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    receipt_number = models.CharField(max_length=20, blank=True, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0) # if you don't have amount already

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_partner_type_display()}"
    
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    excerpt = models.TextField(max_length=300, help_text="Short summary for blog list")
    content = models.TextField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:blog_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
    

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

class MinistryBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    church_name = models.CharField(max_length=200)
    event_date = models.DateField(unique=True) # 1 booking per day
    event_time = models.TimeField()
    event_address = models.TextField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['event_date']

    def clean(self):
        # Must book at least 30 days ahead
        if self.event_date < timezone.now().date() + timedelta(days=30):
            raise ValidationError({'event_date': 'Bookings must be made at least 1 month in advance.'})

        # Block past dates
        if self.event_date < timezone.now().date():
            raise ValidationError({'event_date': 'Cannot book dates in the past.'})

    def __str__(self):
        return f"{self.full_name} - {self.event_date} - {self.get_status_display()}"

class PrayerWall(models.Model):
    name = models.CharField(max_length=100)
    request = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    prayed_count = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.prayed_count} prayed"

class Testimony(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to='testimonies/', blank=True, null=True)
    youtube_link = models.URLField(blank=True)
    story = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class OnlineTracker(models.Model):
    ip_address = models.CharField(max_length=100, unique=True)
    user_agent = models.CharField(max_length=300, blank=True)
    last_seen = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.ip_address

class WorshipAudio(models.Model):
    title = models.CharField(max_length=200)
    audio_file = models.FileField(upload_to='worship/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email