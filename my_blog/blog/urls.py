from django.urls import path
from .views import HomePage, PostDetail, thumbs_rate, UserRegisterView, CategoryPage, Search, Tagging

urlpatterns = [   

            path("", HomePage, name='home'),
            path("post/<id>", PostDetail, name='content'),
            path('vote/', thumbs_rate, name='rate-post'),
            path('register/', UserRegisterView.as_view(), name='register'),
            path('category/<slug>', CategoryPage, name='section'),
            path('tags/<slug>', Tagging, name='tagged'),
            path('search', Search, name='search')

        ] 


