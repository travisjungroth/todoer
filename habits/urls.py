import debug_toolbar
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.Home.as_view(), name='home'),
    path('report/', views.WeekScores.as_view(), name='report'),
    path('__debug__/', include(debug_toolbar.urls)),
]
