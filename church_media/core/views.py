# CLEAN IMPORTS - Paste this at very top of core/views.py
from datetime import date, timedelta
from calendar import monthcalendar, month_name
import hmac
import hashlib
from .models import Partner, PrayerRequest  # adjust to your model names
import json
from django.utils import timezone
from datetime import timedelta
from .models import Partner, PrayerWall, OnlineTracker
from django.db.models import Sum
from .models import Partner, PrayerWall, OnlineTracker, WorshipAudio
from django.shortcuts import render
from django.db.models import Sum, Q
from django.db.models.functions import TruncDate
import uuid
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from .models import Partner, PrayerWall # + Sermon, Testimony if you have
from .models import OnlineTracker
from django.contrib.auth.models import User
import urllib.parse
import base64
import requests
import qrcode
from io import BytesIO
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.text import slugify
from django.utils.html import strip_tags
from django.conf import settings
from django.db.models.functions import TruncDate
from datetime import timedelta

from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import models
from .models import Partner
from django.shortcuts import render, redirect
from django.db.models import Sum
from .models import Partner, PrayerWall, OnlineTracker
from django.contrib.auth.models import User

# Local imports - FIXED spacing
from .models import (
    MinistryBooking,
    BlogPost,
    Program,
    RadioProgram,
    Event,
    Partner,
    ContactMessage,
    PrayerRequest,
    Donation,
    WebsiteConfiguration,
    Sermon,
)
from .forms import (
    BookingForm,
    ContactForm,
    PrayerRequestForm,
    EventForm,
    ProgramForm,
    DonationForm,
    PartnerForm,
    SermonForm,
    SignUpForm,
)

import os
from django.conf import settings
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas

def generate_receipt(partner):
    receipt_dir = os.path.join(settings.MEDIA_ROOT, 'receipts')
    os.makedirs(receipt_dir, exist_ok=True)

    if not partner.receipt_number:
        import random
        partner.receipt_number = f"ZGBC-{partner.id:05d}-{random.randint(100,999)}"
        partner.save()

    filename = f"receipt_{partner.receipt_number}.pdf"
    filepath = os.path.join(receipt_dir, filename)

    c = canvas.Canvas(filepath, pagesize=A5)
    width, height = A5

    c.setFillColorRGB(0.01, 0.04, 0.18)
    c.rect(0,0,width,height,fill=1)
    c.setStrokeColorRGB(0.98, 0.64, 0.01)
    c.setLineWidth(3)
    c.rect(10,10,width-20,height-20)
    c.setFillColorRGB(0.98, 0.64, 0.01)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height-50, "ZION GLOBAL BIBLE CHURCH")
    c.setFillColorRGB(1,1,1)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width/2, height-70, "The Portals' Gate - OFFICIAL RECEIPT")

    c.setFont("Helvetica", 11)
    y = height-120
    full_name = getattr(partner, 'full_name', getattr(partner, 'name', 'Partner'))
    p_type = getattr(partner, 'partnership_type', 'Kingdom Partner')
    
    for line in [
        f"Receipt No: {partner.receipt_number}",
        f"Name: {full_name}",
        f"Email: {partner.email}",
        f"Phone: {partner.phone}",
        f"Type: {p_type}",
        f"Amount: N{partner.amount}",
        f"Date: {partner.created_at.strftime('%d %B, %Y')}",
    ]:
        c.drawString(30, y, line)
        y -= 20

    c.setFont("Helvetica-Bold", 10)
    c.setFillColorRGB(0.98, 0.64, 0.01)
    c.drawCentredString(width/2, 80, "2 Cor 9:7 - God loves a cheerful giver")
    c.setFillColorRGB(1,1,1)
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, 60, "Apostle Henry Leboku | +2349131245154")
    c.setFont("Helvetica-Bold", 14)
    c.setFillColorRGB(0.98, 0.64, 0.01)
    c.drawCentredString(width/2, 40, "PAID & BLESSED")
    c.showPage()
    c.save()

    return f"/media/receipts/{filename}", filepath

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('core:home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})


User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('core:landing')
    
    next_url = request.GET.get('next') or request.POST.get('next') or 'core:landing'
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created!')
            if next_url.startswith('/'):
                return redirect(next_url)
            return redirect(next_url)
        else:
            messages.error(request, 'Please correct errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/signup.html', {'form': form, 'next': next_url})

def logout_view(request):
    logout(request)
    return redirect('core:landing')

def home(request):
    return render(request, 'core/home.html')
  
def tv(request):
    return render(request, 'core/tv.html')

def about(request):
    return render(request, 'core/about.html')

def livestream(request):
    return render(request, 'core/livestream.html')

def radio(request):
    return render(request, 'core/radio.html')

def live(request):
    return render(request, 'core/live.html')

def prayer_request(request):
    return render(request, 'core/prayer_request.html')

def programs(request):
    return render(request, 'core/programs.html')

@login_required(login_url='/signup/')
def partners(request):
    if request.method == 'POST':
        form = PartnerForm(request.POST)
        if form.is_valid():
            partner = form.save(commit=False)
            partner.save() # save to get ID

            # Generate receipt
            receipt_url, receipt_path = generate_receipt(partner)

            # WhatsApp auto message for you and partner
            message = f"Hello {partner.name}, thank you for partnering with ZGBC! Your receipt {partner.receipt_number} for ₦{partner.amount} is confirmed. God bless you! - Apostle Henry Leboku"
            wa_link = f"https://wa.me/{partner.phone.replace('+','').replace(' ','')}?text={urllib.parse.quote(message)}"

            # Send email with receipt (optional)
            # send_mail(...)

            return render(request, 'core/partners_success.html', {
                'partner': partner,
                'receipt_url': receipt_url,
                'wa_link': wa_link,
                'message': message
            })
    else:
        form = PartnerForm()

    return render(request, 'core/partners.html', {'form': form})

# ---------- EVENTS ----------

def event_list(request):
    events = Event.objects.order_by('date')
    return render(request, 'core/events.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'core/event_detail.html', {'event': event})

class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'core/event_list.html'
    context_object_name = 'events'
    paginate_by = 9
    queryset = Event.objects.filter(is_published=True).order_by('-date')

class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'core/event_detail.html'
    context_object_name = 'event'
    queryset = Event.objects.filter(is_published=True)

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'core/event_form.html'
    success_url = reverse_lazy('core:events')
    login_url = 'core:login'

    def form_valid(self, form):
        messages.success(self.request, 'Event created successfully!')
        return super().form_valid(form)

# ---------- SCHEDULE / PROGRAMS ----------
class ProgramListView(LoginRequiredMixin, ListView):
    model = Program
    template_name = 'core/program_list.html'
    context_object_name = 'programs'
    queryset = Program.objects.filter(is_active=True).order_by('day_of_week', 'start_time')

class ProgramCreateView(LoginRequiredMixin, CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'core/program_form.html'
    success_url = reverse_lazy('core:schedule')
    login_url = 'core:login'

    def form_valid(self, form):
        messages.success(self.request, 'Program added to schedule!')
        return super().form_valid(form)


def schedule(request):
    programs = Program.objects.filter(is_active=True).order_by('day_of_week', 'start_time')
    return render(request, 'core/schedule.html', {'programs': programs})

# ---------- CONTACT ----------
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            admin_subject = f'New Contact Form: {contact_message.subject}'
            admin_message = f"""
You have a new message from your website:

Name: {contact_message.name}
Email: {contact_message.email}
Subject: {contact_message.subject}

Message:
{contact_message.message}

View in admin: http://127.0.0.1:8000/admin/core/contactmessage/{contact_message.id}/change/
            """

            user_subject = 'Thanks for contacting us'
            user_message = f"""
Hi {contact_message.name},

Thank you for reaching out to us. We've received your message and will get back to you as soon as possible.

Here's a copy of what you sent:
---
Subject: {contact_message.subject}
Message: {contact_message.message}
---

Blessings,
The Church Team
            """

            try:
                send_mail(
                    admin_subject,
                    admin_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                send_mail(
                    user_subject,
                    user_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [contact_message.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email failed: {e}")

            messages.success(request, 'Message sent successfully! Check your email for confirmation.')
            return redirect('core:contact')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {'form': form})

# ---------- PRAYER REQUESTS ----------

def prayer_request(request):
    if request.method == 'POST':
        form = PrayerRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your prayer request has been received. We are standing with you in prayer.')
            return redirect('core:prayer_request')
    else:
        form = PrayerRequestForm()

    requests = PrayerRequest.objects.filter(is_prayed_for=False).order_by('-submitted_at')

    context = {
        'form': form,
        'requests': requests
    }
    return render(request, 'core/prayer_request.html', {
        'form': form,
        'requests': requests
    })

class PrayerRequestCreateView(CreateView):
    model = PrayerRequest
    form_class = PrayerRequestForm
    template_name = 'core/prayer_request.html'
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        messages.success(self.request, 'Prayer request submitted. We are praying with you!')
        return super().form_valid(form)

# ---------- PARTNERS CBV ----------
class PartnerCreateView(CreateView):
    model = Partner
    form_class = PartnerForm
    template_name = 'core/partner.html'
    success_url = reverse_lazy('core:home')

    def form_valid(self, form):
        messages.success(self.request, 'Thank you for partnering with us!')
        return super().form_valid(form)

# ---------- DONATIONS + PAYSTACK ----------

def donation(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')
        donation_type = request.POST.get('donation_type')

        if not all([full_name, email, amount, donation_type]):
            messages.error(request, 'Please fill all required fields')
            return redirect('core:donation')

        currency_symbols = {'USD': '$', 'NGN': '₦', 'GBP': '£', 'EUR': '€'}
        symbol = currency_symbols.get(currency, currency)

        context = {
            'full_name': full_name,
            'email': email,
            'amount': amount,
            'amount_kobo': int(float(amount) * 100),
            'currency': currency,
            'currency_symbol': symbol,
            'donation_type': donation_type,
            'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY
        }
        return render(request, 'core/donation_confirm.html', context)

    context = {
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY
    }
    return render(request, 'core/donation.html', context)

@login_required
def verify_donation_view(request):
    reference = request.GET.get('reference')
    if not reference:
        messages.error(request, 'No payment reference found')
        return redirect('core:donation')

    url = f'https://api.paystack.co/transaction/verify/{reference}'
    headers = {'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
    response = requests.get(url, headers=headers)
    res_data = response.json()

    if res_data['status'] and res_data['data']['status'] == 'success':
        data = res_data['data']
        metadata = data.get('metadata', {}).get('custom_fields', [])

        full_name = next((f['value'] for f in metadata if f['variable_name'] == 'full_name'), 'Anonymous')
        donation_type = next((f['value'] for f in metadata if f['variable_name'] == 'donation_type'), 'Offering')
        currency = next((f['value'] for f in metadata if f['variable_name'] == 'currency'), data.get('currency', 'USD'))

        donation, created = Donation.objects.get_or_create(
            reference=reference,
            defaults={
                'email': data['customer']['email'],
                'name': full_name,
                'amount': data['amount'] / 100,
                'currency': currency,
                'donation_type': donation_type.lower(),
                'paid': True,
                'paystack_response': data
            }
        )

        if created:
            send_donation_receipt(donation)

        currency_symbols = {'USD': '$', 'NGN': '₦', 'GBP': '£', 'EUR': '€'}
        symbol = currency_symbols.get(currency, currency)

        messages.success(request, f'Thank you {full_name}! Your donation of {symbol}{data["amount"]/100} was successful.')
        return render(request, 'core/donation_success.html', {'donation': donation, 'currency_symbol': symbol})
    else:
        messages.error(request, 'Payment verification failed. Contact us if debited.')
        return render(request, 'core/donation_failed.html')

@csrf_exempt
@require_POST
def paystack_webhook(request):
    paystack_signature = request.headers.get('x-paystack-signature')
    if not paystack_signature:
        return HttpResponse(status=400)

    computed_signature = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode('utf-8'),
        request.body,
        hashlib.sha512
    ).hexdigest()

    if not hmac.compare_digest(computed_signature, paystack_signature):
        return HttpResponse(status=400)

    payload = json.loads(request.body)
    event = payload['event']

    if event == 'charge.success':
        reference = payload['data']['reference']
        try:
            donation = Donation.objects.get(reference=reference)
            if not donation.paid:
                donation.paid = True
                donation.paystack_response = payload['data']
                donation.save()
                send_donation_receipt(donation)
        except Donation.DoesNotExist:
            data = payload['data']
            metadata = data.get('metadata', {}).get('custom_fields', [])
            full_name = next((f['value'] for f in metadata if f['variable_name'] == 'full_name'), 'Anonymous')
            donation_type = next((f['value'] for f in metadata if f['variable_name'] == 'donation_type'), 'Offering')

            donation = Donation.objects.create(
                reference=reference,
                email=data['customer']['email'],
                name=full_name,
                amount=data['amount'] / 100,
                donation_type=donation_type.lower(),
                paid=True,
                paystack_response=data
            )
            send_donation_receipt(donation)

    return JsonResponse({'status': 'success'}, status=200)

def send_donation_receipt(donation):
    subject = f'Receipt for your {donation.get_donation_type_display()}'
    html_message = render_to_string('core/emails/donation_receipt.html', {
        'donation': donation,
        'admin_email': settings.ADMIN_EMAIL
    })
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [donation.email],
        html_message=html_message,
        fail_silently=True,
    )

    admin_subject = f'New {donation.get_donation_type_display()}: ${donation.amount}'
    send_mail(
        admin_subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        html_message=html_message,
        fail_silently=True,
    )

# ---------- SERMONS ----------
class SermonListView(LoginRequiredMixin, ListView):
    model = Sermon
    template_name = 'core/sermon_list.html'
    context_object_name = 'sermons'
    paginate_by = 12
    queryset = Sermon.objects.filter(is_published=True)

class SermonDetailView(LoginRequiredMixin, DetailView):
    model = Sermon
    template_name = 'core/sermon_detail.html'
    context_object_name = 'sermon'
    queryset = Sermon.objects.filter(is_published=True)

class SermonCreateView(LoginRequiredMixin, CreateView):
    model = Sermon
    form_class = SermonForm
    template_name = 'core/sermon_form.html'
    success_url = reverse_lazy('core:sermons')
    login_url = 'core:login'

    def form_valid(self, form):
        messages.success(self.request, 'Sermon added successfully!')
        return super().form_valid(form)

# ---------- ERROR ----------
def permission_denied_view(request, exception=None):
    return render(request, 'core/403.html', status=403)


def debug_urls(request):
    from django.urls import get_resolver
    return HttpResponse(str(get_resolver().reverse_dict.keys()))


def generate_qr_base64(link):
    qr = qrcode.QRCode(box_size=5, border=2)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # For now just print to console
        print(f"Message from {name}: {subject}")
        
        # Add success message
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('core:contact')
        
    return render(request, 'core/contact.html')

def whatsApp(request):
    wa_data = {
        'chat': {
            'link': 'https://wa.me/2347035043607?text=Hello%20ZGBC%20RTV',
            'title': 'Direct ChatRoom',
            'desc': 'Message us 1-on-1'
        },
        'group': {
            'link': 'https://chat.whatsapp.com/Cd0GcVF29NwH2AUsbcLRIZ',
            'title': 'Join Our Group', 
            'desc': 'Join the ZGBC Community'
        },
        'channel': {
            'link': 'https://whatsapp.com/channel/0029VaAuQZ8KGGGOnK0zVU1w',
            'title': 'Follow Our Official Channel',
            'desc': 'Get updates and broadcasts'
        }
    }
    
    for data in wa_data.items():
        data['qr'] = generate_qr_base64(data['link'])
        return render(request, 'core/contact.html', {'wa_data': wa_data})


def blog(request):
    post_list = BlogPost.objects.filter(published=True).order_by('-created_at')  # Changed
    paginator = Paginator(post_list, 9)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'core/blog.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)  # Changed
    related_posts = BlogPost.objects.filter(category=post.category, published=True).exclude(id=post.id)[:3]  # Changed
    return render(request, 'core/blog_detail.html', {
        'post': post,
        'related_posts': related_posts
    })

def booking_calendar(request, year=None, month=None):
    today = timezone.now().date()
    if year is None or month is None:
        year, month = today.year, today.month
    year, month = int(year), int(month)

    start_date = date(year, month, 1)
    end_date = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)

    booked_dates = set(
        MinistryBooking.objects.filter(
            event_date__gte=start_date,
            event_date__lt=end_date,
            status__in=['pending', 'confirmed']
        ).values_list('event_date', flat=True)
    )

    cal = monthcalendar(year, month)
    min_booking_date = today + timedelta(days=30)

    calendar_weeks = []
    for week in cal:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append({'day': '', 'status': 'empty'})
            else:
                current_date = date(year, month, day)
                if current_date < today:
                    status = 'past'
                elif current_date in booked_dates:
                    status = 'booked'
                elif current_date < min_booking_date:
                    status = 'unavailable'
                else:
                    status = 'available'
                week_data.append({'day': day, 'status': status, 'date': current_date})
        calendar_weeks.append(week_data)

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    form = BookingForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        booking = form.save()

        try:
            ctx = {'booking': booking, 'site_url': getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')}

            # Admin email
            admin_text = render_to_string('core/emails/admin_booking.txt', ctx)
            admin_html = render_to_string('core/emails/admin_booking.html', ctx)
            msg_admin = EmailMultiAlternatives(
                f"New Booking: {booking.church_name} - {booking.event_date}",
                admin_text, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL]
            )
            msg_admin.attach_alternative(admin_html, "text/html")
            msg_admin.send()

            # User email
            user_text = render_to_string('core/emails/user_booking.txt', ctx)
            user_html = render_to_string('core/emails/user_booking.html', ctx)
            msg_user = EmailMultiAlternatives(
                "Booking Request Received", user_text,
                settings.DEFAULT_FROM_EMAIL, [booking.email]
            )
            msg_user.attach_alternative(user_html, "text/html")
            msg_user.send()

        except Exception as e:
            print(f"EMAIL FAILED: {e}")

        messages.success(request, 'Booking request sent successfully!')
        return redirect('request.path')

    context = {
        'calendar_weeks': calendar_weeks,
        'month_name': month_name[month],
        'year': year,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'form': form,
        'today': today,
    }
    return render(request, 'core/booking_calendar.html', context)

from .models import PrayerWall
from django.http import JsonResponse

def prayer_wall(request):
    prayers = PrayerWall.objects.filter(is_approved=True).order_by('-created_at')[:20]
    return render(request, 'core/prayer_wall.html', {'prayers': prayers})

def prayed_click(request, id):
    prayer = PrayerWall.objects.get(id=id)
    prayer.prayed_count += 1
    prayer.save()
    return JsonResponse({'count': prayer.prayed_count})


import json
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, Q
from django.db.models.functions import TruncDate
from django.shortcuts import render

@login_required
def super_dashboard(request):
    # Partner uses created_at, Prayer uses submitted_at
    seven_days_ago = timezone.now() - timedelta(days=6)
    daily_qs = Partner.objects.filter(created_at__gte=seven_days_ago).annotate(date=TruncDate('created_at')).values('date').annotate(
        tithe_sum=Sum('amount', filter=Q(partner_type__icontains='tithe')),
        offering_sum=Sum('amount', filter=Q(partner_type__icontains='offering'))
    ).order_by('date')

    dates, tithe_daily, offering_daily = [], [], []
    date_map = {item['date']: item for item in daily_qs}

    for i in range(7):
        day = (timezone.now() - timedelta(days=6-i)).date()
        dates.append(day.strftime('%b %d'))
        row = date_map.get(day)
        tithe_daily.append(float(row['tithe_sum'] or 0) if row else 0)
        offering_daily.append(float(row['offering_sum'] or 0) if row else 0)

    context = {
        'total_online': 0,
        'total_partners': Partner.objects.count(),
        'total_amount': Partner.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
        'total_prayers': PrayerRequest.objects.count(),
        'total_tithe': Partner.objects.filter(partner_type__icontains='tithe').aggregate(Sum('amount'))['amount__sum'] or 0,
        'total_offering': Partner.objects.filter(partner_type__icontains='offering').aggregate(Sum('amount'))['amount__sum'] or 0,
        'recent_partners': Partner.objects.order_by('-created_at')[:5],
        'recent_prayers': PrayerRequest.objects.order_by('-submitted_at')[:5],
        'dates': json.dumps(dates),
        'tithe_daily': json.dumps(tithe_daily),
        'offering_daily': json.dumps(offering_daily),
    }
    return render(request, 'core/dashboard.html', context)

def export_excel(request):
    wb = openpyxl.Workbook()
    
    ws1 = wb.active
    ws1.title = "Partners"
    ws1.append(["Name", "Email", "Partner Type", "Amount", "Date", "Phone"])
    for p in Partner.objects.all().order_by('-created_at'):
        ws1.append([p.name, p.email, p.partner_type, float(p.amount), p.created_at.strftime('%Y-%m-%d %H:%M'), p.phone])

    ws2 = wb.create_sheet("Summary")
    total_tithe = Partner.objects.filter(partner_type__icontains='tithe').aggregate(Sum('amount'))['amount__sum'] or 0
    total_offering = Partner.objects.filter(partner_type__icontains='offering').aggregate(Sum('amount'))['amount__sum'] or 0
    ws2.append(["ZGBC Financial Summary"])
    ws2.append([])
    ws2.append(["Total Tithe", float(total_tithe)])
    ws2.append(["Total Offering", float(total_offering)])
    ws2.append(["Total Combined", float(total_tithe + total_offering)])
    
    ws3 = wb.create_sheet("Prayers")
    ws3.append(["Name", "Request", "Date", "Phone"])
    for r in PrayerRequest.objects.all().order_by('-submitted_at'):
        ws3.append([r.name, r.request[:200], r.submitted_at.strftime('%Y-%m-%d'), r.phone])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=ZGBC_Report.xlsx'
    wb.save(response)
    return response


from .models import Testimony

def testimonies(request):
    items = Testimony.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'core/testimonies.html', {'items': items})

def submit_testimony(request):
    if request.method == 'POST':
        Testimony.objects.create(
            name=request.POST.get('name'),
            title=request.POST.get('title'),
            story=request.POST.get('story'),
            youtube_link=request.POST.get('youtube_link',''),
        )
        return render(request, 'core/testimony_success.html')
    return render(request, 'core/submit_testimony.html')

import openpyxl
from django.http import HttpResponse
from django.db.models import Sum

def export_excel(request):
    wb = openpyxl.Workbook()
    
    # Sheet 1 - Partners
    ws1 = wb.active
    ws1.title = "Partners"
    ws1.append(["Name", "Email", "Type", "Amount", "Currency", "Date"])
    from .models import Partner
    for p in Partner.objects.all().order_by('-created_at'):
        ws1.append([p.full_name if hasattr(p,'full_name') else p.name, p.email, p.donation_type, float(p.amount), p.currency if hasattr(p,'currency') else 'NGN', p.created_at.strftime('%Y-%m-%d')])

    # Sheet 2 - Summary
    ws2 = wb.create_sheet("Summary")
    total_tithe = Partner.objects.filter(donation_type__icontains='tithe').aggregate(Sum('amount'))['amount__sum'] or 0
    total_offering = Partner.objects.filter(donation_type__icontains='offering').aggregate(Sum('amount'))['amount__sum'] or 0
    ws2.append(["ZGBC Financial Summary"])
    ws2.append([])
    ws2.append(["Total Tithe", total_tithe])
    ws2.append(["Total Offering", total_offering])
    ws2.append(["Total Combined", total_tithe + total_offering])
    
    # Sheet 3 - Prayers
    ws3 = wb.create_sheet("Prayers")
    ws3.append(["Name", "Request", "Date"])
    from .models import PrayerRequest
    for r in PrayerRequest.objects.all().order_by('-created_at'):
        ws3.append([r.name, r.request[:200], r.created_at.strftime('%Y-%m-%d')])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=ZGBC_Report.xlsx'
    wb.save(response)
    return response

from .models import Subscriber
from django.contrib import messages

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            obj, created = Subscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, "Welcome to ZGBC family! You are subscribed.")
            else:
                messages.info(request, "You are already subscribed.")
    return redirect('core:home')