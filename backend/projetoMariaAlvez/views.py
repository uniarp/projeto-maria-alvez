from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from projetoMariaAlvezApp.views import home, sample_api  # Importe do app

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=True)),  # Redireciona / para /admin/
    path('admin/', admin.site.urls),
    path('api/', include('projetoMariaAlvezApp.urls')),
]