import debug_toolbar
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.WeekScores.as_view(), name='home'),
    path('__debug__/', include(debug_toolbar.urls)),
]
