from django.urls import path
from Eapp import views

urlpatterns = [
   path('',views.home,name='home'),
   path('purchase/', views.purchase, name='purchase'),
   path('tracker', views.tracker, name="TrackingStatus"),
   path('checkout/', views.checkout, name="Checkout"),
   path('about/', views.about, name="about"),
   path('services/', views.services, name="services"),
   path('portfolio-details/', views.portfolio_details, name='portfolio_details'),
   path('receive_message/', views.receive_message, name='receive_message'),
   path('Privacy_Policy/', views.Privacy_Policy, name='Privacy_Policy'),
   path('Termofuse/', views.Termofuse, name='Termofuse'),
   
]