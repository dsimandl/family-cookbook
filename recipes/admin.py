from models import *
from django.contrib import admin

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

class InstructionStepInline(admin.StackedInline):
    model = InstructionStep
    extra = 1

class FoodPictureInline(admin.StackedInline):
    model = FoodPicture
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['name','dish','origin']}),
        (None, {'fields':[('cooking_time','prep_time','servings',),]}),
        (None, {'fields':['slug'],'classes':('collapse',)}),
        ('Notes', {'fields':['notes'],'classes':('collapse',)})
        ]
    radio_fields = {'dish': admin.HORIZONTAL}
    inlines= [RecipeIngredientInline,InstructionStepInline, FoodPictureInline]
    list_display = ('name','dish')
    list_filter = ['dish','date_added']
    prepopulated_fields = {'slug': ('name',)}


class NutritionUnitInline(admin.TabularInline):
    model = NutritionUnit
    extra = 1

class NutritionIngredientAdmin(admin.ModelAdmin):
    fields = ('name','weight_1','weight_1_desc','weight_2','weight_2_desc',
              'calories','protein','fat','carbohydrate')
    inlines = [NutritionUnitInline]
    

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(NutritionIngredient, NutritionIngredientAdmin)
admin.site.register(UserProfile)
