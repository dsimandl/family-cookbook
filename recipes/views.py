from django.http import HttpResponse, QueryDict, HttpResponseRedirect
from django.views.generic import DetailView, ListView, View, CreateView, UpdateView
from django.views.generic.edit import ProcessFormView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.forms.models import inlineformset_factory
from django.core import serializers
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login, logout
from models import *
from contentaware import *

def home(request):
    respString = r"<html><head><title>Merry Christmas!</title></head>"
    respString += r"<body>Dear Jenny,<p>I love you.  I want to make your life easier.  I present to you this custom-made, fully-configurable, always-on cookbook in the cloud.  This present includes all the technical support that you could ever need.  I also promise to type in lots of our favorite recipes, and to make the site look prettier and work better over time.</p><p>Love,<br />Mark</p>"
    respString += "<ul><li>To add or edit recipes, <a href='/admin/'>click here</a></li><li>Contents: <a href='/recipes/contents/'>click here</a> </li><li>Index: <a href='/recipes/'>click here</a></li><li>Search: <a href='/recipes/search/'>click here</a></li></ul></body></html>"
    return HttpResponse(respString)

def recipeList(request):
    response = HttpResponse()
    serializers.serialize('json',Recipe.objects.all(),stream=response)
    return response

def search(request):
    respString = r"<html><head><title>Search</title></head><body><h1>In progress</h1></body></html>"
    return HttpResponse(respString)

class DishListView(ListView):
    
    template_name='recipes/contents.html'

    def get_queryset(self):
        return Recipe.objects.filter(dish__iexact=self.kwargs['dish_type']).order_by('name')

class RecipeListView(AwareListView):
    def get_queryset(self):
        if self.kwargs.get('username','') == '':
            return self.queryset
        else:
            return User.objects.get(username=self.kwargs['username']).get_profile().fav_recipes.order_by('dish','name')

    def get_context_data(self,**kwargs):
        context = super(RecipeListView, self).get_context_data(**kwargs)
        if self.kwargs.get('username','') != '':
            context['fav_user'] = User.objects.get(username=self.kwargs['username'])
        return context

class SearchListView(RecipeListView):
    template_name='recipes/index.html'

    def get_queryset(self):
        return Recipe.objects.filter(Q(recipeingredient__ingredient__name__icontains=self.request.GET['term']) | Q(name__icontains=self.request.GET['term'])).distinct().order_by('name')

class RecipeDetailView(AwareDetailView):

    queryset = Recipe.objects.all()
    template_name = 'recipes/detail_dev.html'

    def get_context_data(self,**kwargs):
        context = super(RecipeDetailView,self).get_context_data(**kwargs)
        # PictureFormSet = inlineformset_factory(Recipe, FoodPicture, extra=1)
        # context['formset'] = PictureFormSet(instance=Recipe.objects.get(slug=self.kwargs['slug']))
        context['form'] = FoodPictureForm()
        return context

class AuthenticatedProcessFormView(ProcessFormView):
    def post(self,*args,**kwargs):
        if self.request.user.is_authenticated():
            return super(AuthenticatedProcessFormView,self).post(*args,**kwargs)
        else:
            return self.get(*args,**kwargs)
            
class UserUpdateView(AuthenticatedProcessFormView, UpdateView):
    model = User
    slug_field = 'username'
    form_class = UserForm

    def post(self,*args,**kwargs):
        if self.request.user == self.get_object():
            return super(UserUpdateView,self).post(*args,**kwargs)
        else:
            return self.get(*args,**kwargs)


class PictureAddView(CreateView):
    model = FoodPicture
    form_class = FoodPictureForm

    def get_form_kwargs(self):
        kwargs = super(CreateView, self).get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                    'instance':FoodPicture(recipe=Recipe.objects.get(slug=self.kwargs['slug']))
                    })
        return kwargs

    def get_success_url(self):
        return reverse('recipe_detail',args=[self.kwargs['slug']])

    def get_context_data(self,**kwargs):
        context = super(PictureAddView,self).get_context_data(**kwargs)
        context['object'] = Recipe.objects.get(slug=self.kwargs['slug'])
        return context

    # def post(self,request,*args,**kwargs):
    #     resp = HttpResponse(content_type="text/plain")
    #     if request.user.is_authenticated():
    #         fp_form = FoodPictureForm(request.POST)
    #         if fp_form.is_valid():
    #             new_pic = fp_form.save(commit=False)
    #             new_pic.recipe = Recipe.objects.get(slug=self.kwargs['slug'])
    #             new_pic.save()
    #             return HttpResponseRedirect(reverse('recipe_detail',args=[self.kwargs['slug']]))
    #         else:
    #             resp.write("there was a problem")
    #             return resp
    #     else:
    #         resp.write("Sorry, charlie")
    #         return resp


class FavView(View):

    def get(self,request,*args,**kwargs):
        resp = HttpResponse()
        resp.write(str(self.kwargs))
        return resp

    def put(self,request,*args,**kwargs):
        resp = HttpResponse(content_type="text/plain")
        if request.user.is_authenticated():
            fav_recipe = Recipe.objects.get(slug=self.kwargs['recipe_slug'])
            request.user.userprofile.fav_recipes.add(fav_recipe)
            resp.write("You made a favorite")
        else:
            resp.write("no luck this time")
        return resp

    def delete(self,request,*args,**kwargs):
        resp = HttpResponse(content_type="text/plain")
        if request.user.is_authenticated():
            fav_recipe = Recipe.objects.get(slug=self.kwargs['recipe_slug'])
            request.user.userprofile.fav_recipes.remove(fav_recipe)
            resp.write("You deleted a favorite")
        else:
            resp.write("no luck this time")
        return resp

class PersonaLoginView(View):

    def post(self,request,*args,**kwargs):
        user = authenticate(assertion=request.POST.get('assertion'))
        if user is not None:
            login(request,user)
            print("persona login", user, user.is_authenticated())

        return HttpResponse(user.username)
