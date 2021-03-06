from allauth.account.views import logout
import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/logout/', logout, name="logout"),
    path("accounts/", include("allauth.urls")),
    path('habits/', views.HabitView.as_view(), name='habits'),
    path('habits/<int:pk>/move/<str:direction>/', views.HabitMove.as_view(), name='habit-reorder'),
    path('habits/<int:pk>/delete', views.HabitDelete.as_view(), name='habit-delete'),
    path('tasks/', views.TaskView.as_view(), name='tasks'),
    path('weekly-report/', views.WeeklyReport.as_view(), name='weekly-report'),
    path('documentation/', views.Documentation.as_view(), name='documentation'),
    path('privacy/', views.Privacy.as_view(), name='privacy'),
]

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
