from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('city/<int:pk>', views.CityDetailView.as_view(), name='city_detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
