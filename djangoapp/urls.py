# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # path for registration
    path('register', views.registration, name='register'),  # ✅ Registration route added

    # path for login
    path('login', views.login_user, name='login'),

    # path for logout
    path('logout', views.logout_request, name='logout'),

    # path for dealer reviews view
    # path('dealers/<int:dealer_id>', views.get_dealer_details, name='dealer_details'),
    path(route='get_cars', view=views.get_cars, name ='getcars'),
    # path for add a review view
    # path('add_review/<int:dealer_id>', views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
