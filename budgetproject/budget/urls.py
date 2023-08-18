from django.urls import path

from . import views

urlpatterns = [
    path('', views.project_list, name = 'Project-List'),
    path('add', views.ProjectCreateView.as_view(), name = 'add'),
    path('<slug:project_slug>', views.project_detail, name = 'Project-Detail'),
    
]
