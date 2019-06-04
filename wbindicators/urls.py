from django.urls import path

from . import views

app_name = 'wbindicators'
urlpatterns = [
    path('', views.home, name='home'),
    path('myresults/', views.view_results, name='view_results'),
    #path('get_data/', views.get_data, name='get_data'),
]
