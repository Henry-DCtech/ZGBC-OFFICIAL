class OnlineUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        try:
            from core.models import OnlineTracker
            from django.utils import timezone
            from datetime import timedelta
            
            ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
            if ip:
                OnlineTracker.objects.update_or_create(
                    ip_address=ip,
                    defaults={'user_agent': request.META.get('HTTP_USER_AGENT','')[:200]}
                )
                # Clean old
                OnlineTracker.objects.filter(last_seen__lt=timezone.now() - timedelta(minutes=10)).delete()
        except:
            pass  # Don't crash site if DB error
            
        return response