from django.views.generic import DetailView

from products.models import Product


class ProductDetailView(DetailView):
    model = Product
