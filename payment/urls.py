from django.urls import path
from payment import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', views.payment_form, name='payment_form'),
    path('generate_token/', login_required(views.generate_token), name='generate_token'),
    path('process_payment/', login_required(views.process_payment), name='process_payment'),
]
