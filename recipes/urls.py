from django.conf.urls.defaults import patterns, include, url
from django.views.generic import *
from django.contrib.auth.models import User
from models import Recipe, FoodPicture, UserForm
from views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^contents/$',RecipeListView.as_view(
            queryset=Recipe.objects.all().order_by('dish','name'),
            template_name='recipes/contents_dev.html'
            ), 
        name='recipe_contents'),
    url(r'^index/$',RecipeListView.as_view(
            queryset=Recipe.objects.all().order_by('name'),
            template_name='recipes/index_dev.html'
            ), 
        name='recipe_index'),
    url(r'^search/$',SearchListView.as_view(template_name='recipes/search_dev.html'), 
        name='recipe_search'),
    url(r'^(?P<slug>[-\w]+)/$', RecipeDetailView.as_view(),name='recipe_detail'),
    url(r'^(?P<slug>[-\w]+)/picture/$', PictureAddView.as_view()), 
    url(r'^fav/(?P<recipe_slug>[-\w]+)/$',FavView.as_view(),name='add_favorite'),
    url(r'^user/(?P<username>[^/]+)/$',RecipeListView.as_view(
            template_name='recipes/contents_dev.html'
       ), name='user_recipes'),


    url(r'^data/(?P<slug>[-\w]+)/$', RecipeDetailView.as_view(),{"format":"json"},name='recipe_json_detail'),
    url(r'^data/$',RecipeListView.as_view(
            queryset=Recipe.objects.all().order_by('name'),
            template_name='recipes/index_dev.html'
            ),{"format":"json"},name='recipe_json_list'),
)
