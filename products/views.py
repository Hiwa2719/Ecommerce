from django.views.generic import DetailView, ListView

from products.models import Product


class ProductDetailView(DetailView):
    model = Product


class ProductListView(ListView):
    model = Product
