from django.urls import path
from .views import (
    RecipeDetailView,
    CheckoutView,
    HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_recipe_from_cart,
    image_upload_view,
    searchbar_view
)


app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<slug>/', RecipeDetailView.as_view(), name='product'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-recipe-from-cart/<slug>/', remove_single_recipe_from_cart,
         name='remove-single-recipe-from-cart'),
    path('upload/', image_upload_view, name='upload'),
    path('searchbar/', searchbar_view, name='searchbar')
]
