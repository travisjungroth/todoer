from allauth.account.views import logout
import debug_toolbar
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/logout/', logout, name="logout"),
    path('accounts/', include('todoist_oauth2.urls')),
    path('habits/', views.HabitView.as_view(), name='habits'),
    path('habits/<int:pk>/move/<str:direction>/', views.HabitMove.as_view(), name='habit-reorder'),
    path('habits/<int:pk>/delete', views.HabitDelete.as_view(), name='habit-delete'),
    path('report/', views.WeekScores.as_view(), name='report'),
    path('__debug__/', include(debug_toolbar.urls)),
]
