from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .forms import CheckoutForm, ImageForm, SearchbarForm
from .models import Recipe, OrderRecipe, Order, BillingAddress, Image, Searchbar


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(
                user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                same_shipping_address = form.cleaned_data.get(
                    'same_shipping_address')
                save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect('core:checkout')
            return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:order-summary")


class HomeView(ListView):
    model = Recipe
    paginate_by = 10
    template_name = "home.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "product.html"


@ login_required
def add_to_cart(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    order_recipe, created = OrderRecipe.objects.get_or_create(
        recipe=recipe,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order recipe is in the order
        if order.recipes.filter(recipe__slug=recipe.slug).exists():
            order_recipe.quantity += 1
            order_recipe.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was added to your cart.")
            order.recipes.add(order_recipe)
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.recipes.add(order_recipe)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@ login_required
def remove_single_recipe_from_cart(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if order recipe is in the order
        if order.recipes.filter(recipe__slug=recipe.slug).exists():
            order_recipe = OrderRecipe.objects.filter(
                recipe=recipe,
                user=request.user,
                ordered=False
            )[0]
            if order_recipe.quantity > 1:
                order_recipe.quantity -= 1
                order_recipe.save()
            else:
                order.recipes.remove(order_recipe)
            messages.info(request, "This item's quantity was updated")
            return redirect("core:order-summary")

        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("core:product", slug=slug)


@login_required
def remove_from_cart(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if order recipe is in the order
        if order.recipes.filter(recipe__slug=recipe.slug).exists():
            order_recipe = OrderRecipe.objects.filter(
                recipe=recipe,
                user=request.user,
                ordered=False
            )[0]
            order.recipes.remove(order_recipe)
            messages.info(request, "This item was removed to your cart.")
            return redirect("core:order-summary")

        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("core:product", slug=slug)


def image_upload_view(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            return render(request, 'imagetest.html', {'form': form, 'img_obj': img_obj})
    else:
        form = ImageForm()
    return render(request, 'imagetest.html', {'form': form})


def searchbar_view(request):
    form = SearchbarForm()
    return render(request, 'searchbar.html', {'form': form})
