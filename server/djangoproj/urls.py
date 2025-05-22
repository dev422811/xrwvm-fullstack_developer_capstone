from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # These routes are handled by React (SPA)
    path('login/', TemplateView.as_view(template_name="index.html")),
    path('register/', TemplateView.as_view(template_name="index.html")),
    path('dealer/<int:dealer_id>/', TemplateView.as_view(template_name="index.html")),
    path('dealers/', TemplateView.as_view(template_name="index.html")),
    path('postreview/<int:dealer_id>',TemplateView.as_view(template_name="index.html")),
    # Django backend API routes
    path('djangoapp/', include('djangoapp.urls')),

    # Root path handled by React
    path('', TemplateView.as_view(template_name="index.html")),

    # Catch-all route for unmatched paths (React handles them)
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]

# Serve static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
