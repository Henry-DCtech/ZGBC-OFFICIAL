from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse
from core import views as core_views
from django.contrib.auth import views as auth_views
from core import views as core_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
#     # path('booking/', include('core.urls')),
#     # ... your other paths
#     path('accounts/signup/', core_views.signup, name='signup'),
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
