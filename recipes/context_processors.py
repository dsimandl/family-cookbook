from recipes.models import Recipe

def master_recipe_list(request):
    return {'master_recipe_list':Recipe.objects.all().order_by('dish','name')}
