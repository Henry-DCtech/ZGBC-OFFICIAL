from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render


app_name = 'core'


urlpatterns = [
    # Your login view
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('calendar', views.booking_calendar, name='booking_calendar'),
    path('<int:year>/<int:month>/', views.booking_calendar, name='booking_calendar_month'),

    # Password reset - add success_url to override defaults
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='core/password_reset_form.html',
        success_url=reverse_lazy('core:password_reset_done')
        ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='core/password_reset_done.html'
        ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='core/password_reset_confirm.html',
        success_url=reverse_lazy('core:password_reset_complete')
        ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='core/password_reset_complete.html'
        ), name='password_reset_complete'),


         # Rest of your URLs... same as you have
    path('tv/', views.tv, name='tv'),
    path('radio/', views.radio, name='radio'),
    path('about/', views.about, name='about'),
    path('live/', views.live, name='live'),
    path('livestream/', views.livestream, name='livestream'),
    path('partners/', views.partners, name='partners'),
    path('schedule/', views.schedule, name='schedule'),
    path('contact/', views.contact, name='contact'),
    path('prayer-request/', views.prayer_request, name='prayer_request'),
    path('donation/', views.donation, name='donation'),
    path('donation/verify/', views.verify_donation_view, name='verify_donation'),
    path('paystack/webhook/', views.paystack_webhook, name='paystack_webhook'),
    
    # Events
    path('events/', views.event_list, name='events'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/list/', views.EventListView.as_view(), name='event_list'),
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
    
    # Programs
    path('programs/', views.programs, name='programs'),
    path('programs/', views.ProgramListView.as_view(), name='program_list'),
    path('programs/create/', views.ProgramCreateView.as_view(), name='program_create'),
    
    # Sermons
    path('sermons/', views.SermonListView.as_view(), name='sermons'),
    path('sermons/<int:pk>/', views.SermonDetailView.as_view(), name='sermon_detail'),
    path('sermons/create/', views.SermonCreateView.as_view(), name='sermon_create'),

    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),

    #Booking URL
    # path('booking', views.booking, name='booking'),
    path('booking/', views.booking_calendar, name='booking_calender'),
    path('booking/<int:year>/<int:month>/', views.booking_calendar, name='booking_calendar_month'),
   
    # ... your existing urls ...
    path('privacy/', lambda r: render(r, 'core/privacy.html'), name='privacy'),
    path('terms/', lambda r: render(r, 'core/terms.html'), name='terms'),
    path('prayer-wall/', views.prayer_wall, name='prayer_wall'),
    path('prayed/<int:id>/', views.prayed_click, name='prayed_click'),
    path('dashboard/', views.super_dashboard, name='dashboard'),
    path('testimonies/', views.testimonies, name='testimonies'),
    path('testimonies/submit/', views.submit_testimony, name='submit_testimony'),
    path('export-excel/', views.export_excel, name='export_excel'),
    path('subscribe/', views.subscribe, name='subscribe'),
    ]



if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )