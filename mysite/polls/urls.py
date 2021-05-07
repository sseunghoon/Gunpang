from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('check/', views.check, name='check'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
