from django import forms
from .models import ContactMessage, PrayerRequest, Event, Program, Donation, Partner

from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your message...'}),
        }

from django import forms
from .models import PrayerRequest

from django import forms
from .models import PrayerRequest

class PrayerRequestForm(forms.ModelForm):
    class Meta:
        model = PrayerRequest
        fields = ['name', 'email', 'phone', 'request', 'is_urgent', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone optional'}),
            'request': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your prayer request'}),
            'is_urgent': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        labels = {
            'is_private': 'Keep this request private to prayer team only'
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'date', 'location', 'description', 'image', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
            

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['title', 'description', 'day_of_week', 'start_time', 'end_time', 'host', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'day_of_week': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'host': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['name', 'email', 'phone', 'amount', 'donation_type', 'project', 'message', 'is_anonymous']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount (₦)', 'min': '100'}),
            'donation_type': forms.Select(attrs={'class': 'form-select'}),
            'project': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Name (Optional)'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Message (Optional)'}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'is_anonymous': 'Donate anonymously',
        }

class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'email', 'phone', 'website', 'partner_type', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name / Organization'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website (Optional)'}),
            'partner_type': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'How would you like to partner?'}),
        }

from .models import Sermon

class SermonForm(forms.ModelForm):
    class Meta:
        model = Sermon
        fields = ['title', 'preacher', 'description', 'sermon_date', 'video_url', 'audio_file', 'thumbnail', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'preacher': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'sermon_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'audio_file': forms.FileInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, 
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Username'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'First Name'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Last Name'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Confirm Password'
        })

from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm): 
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
        }

from django import forms
from.models import MinistryBooking
from datetime import date, timedelta

class BookingForm(forms.ModelForm):
    class Meta:
        model = MinistryBooking
        fields = ['full_name', 'email', 'phone', 'church_name', 'event_date', 'event_time', 'event_address', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'church_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Church/Ministry Name'}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'min': (date.today() + timedelta(days=30)).isoformat()}),
            'event_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'event_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Event Venue Address'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Additional details'}),
        }

    def clean_event_date(self):
        event_date = self.cleaned_data['event_date']
        if event_date < date.today() + timedelta(days=30):
            raise forms.ValidationError("Bookings must be at least 1 month in advance.")
        return event_date