from django.urls import path
from . import views

#  criar um arquivo urls.py para cada app é a melhor maneira de tornar a app reutilizavel para outros proj.
app_name = 'blog'  # isso permite organizar os urls por aplicação e usar o nome ao referenciá-los

urlpatterns = [
    # views de postagens
    path('', views.post_list, name='post_list'),  # padro de url sem args e é mapeado para a view post_list
    # path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    # esse padrão recebe os arg year,month... e é mapeado para a view post_detail
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),

  ]
