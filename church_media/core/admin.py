
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from .models import BlogPost, Category  # Changed from Post
from django.contrib import admin
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import MinistryBooking
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from.models import MinistryBooking
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from .models import (
    Program, RadioProgram, Sermon, Event, Partner, 
    ContactMessage, PrayerRequest, Donation, WebsiteConfiguration
)

admin.site_urls = '/'

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(RadioProgram)
class RadioProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'host', 'air_time', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'host']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'is_published']
    list_filter = ['is_published', 'date']
    list_editable = ['is_published']
    search_fields = ['title', 'description']
    date_hierarchy = 'date'

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    
    def has_add_permission(self, request):
        return False

@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_urgent', 'is_answered', 'submitted_at']
    list_filter = ['is_urgent', 'is_answered', 'is_private', 'submitted_at']
    readonly_fields = ['submitted_at']
    

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'donation_type', 'paid', 'created_at']
    list_filter = ['paid', 'donation_type', 'created_at']
    readonly_fields = ['reference', 'created_at', 'updated_at']

@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ['title', 'preacher', 'sermon_date', 'is_published', 'is_featured']
    list_filter = ['is_published', 'is_featured', 'sermon_date']
    search_fields = ['title', 'preacher', 'description']
    prepopulated_fields = {'slug': ('title', 'sermon_date')}
    date_hierarchy = 'sermon_date'

@admin.register(WebsiteConfiguration)
class WebsiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'hero_title', 'updated_at', 'edit_link']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Site Info', {
            'fields': ('site_name', 'site_logo', 'favicon')
        }),
        ('Homepage Hero', {
            'fields': ('hero_title', 'hero_subtitle', 'hero_image')
        }),
        ('Contact Info', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'youtube_url', 'instagram_url')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return not WebsiteConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def changelist_view(self, request, extra_context=None):
        if WebsiteConfiguration.objects.exists():
            obj = WebsiteConfiguration.objects.first()
            return redirect(reverse('admin:core_websiteconfiguration_change', args=[obj.pk]))
        return super().changelist_view(request, extra_context)
    
    def edit_link(self, obj):
        return format_html('<a class="button" href="{}">Edit Config</a>', 
                         reverse('admin:core_websiteconfiguration_change', args=[obj.pk]))
    edit_link.short_description = 'Actions'
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
    

@admin.register(MinistryBooking)
class MinistryBookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'church_name', 'email', 'event_date', 'status']
    list_filter = ['status', 'event_date']
    actions = ['confirm_bookings']

    def confirm_bookings(self, request, queryset):
        confirmed_count = 0
        for booking in queryset:
            booking.status = 'confirmed'
            booking.save()
            confirmed_count += 1
            
            # SAFE EMAIL - never crashes admin
            try:
                html = render_to_string("core/emails/user_confirmed.html", {"booking": booking})
                text = strip_tags(html)
                msg = EmailMultiAlternatives(
                    subject="Booking Confirmed - ZGBC",
                    body=text,
                    from_email="admin@zgbc.com",
                    to=[booking.email]
                )
                msg.attach_alternative(html, "text/html")
                msg.send(fail_silently=False)
            except Exception as e:
                print(f"EMAIL FAILED: {e}")
                messages.warning(request, f"{booking.church_name} confirmed but email failed: {e}")

        if confirmed_count > 0:
            messages.success(request, f"{confirmed_count} booking(s) confirmed!")

    confirm_bookings.short_description = "Confirm selected bookings"


from .models import OnlineTracker, WorshipAudio

@admin.register(OnlineTracker)
class OnlineTrackerAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'last_seen']

@admin.register(WorshipAudio)
class WorshipAudioAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']