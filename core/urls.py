from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('status/', views.status, name='status'),
    path('backend/', views.backend, name='backend'),
    path('logout/', views.logout_user, name="logout"),
    path('solved/<str:pk>', views.solved, name='solved'),
    path('completed/<str:pk>', views.completed, name='completed'),
    path('payment/', views.make_payment, name='payment'),
    path('completed-projects/', views.completed_projects, name='completed_projects'),
    path('add_project/', views.add_project, name='add_project'),
    path('add_freelancer/', views.add_freelancer, name='add_freelancer'),
    path('show_freelancers/', views.show_freelancers, name='show_freelancers'),
    path('pay_freelancers/<int:pk>', views.pay_freelancer, name='pay_freelancer'),
    path('add_client/', views.add_client, name='add_client')
]
