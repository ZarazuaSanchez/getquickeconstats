from django.urls import path

from . import views

app_name = 'wbindicators'
urlpatterns = [
    path('', views.request_stats, name='request-stats'),
    #path('get_stats/', views.get_stats, name='get-stats'),
    path('view_results/', views.view_results, name='view-results'),
]
