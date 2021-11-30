from django.views.generic import DetailView, ListView

from products.models import Product


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_chain'] = self.categories_list()
        return context

    def categories_list(self):
        category = self.object.categories.first()
        category_list = []
        while category.parent:
            category_list.insert(0, category)
            category = category.parent
        else:
            category_list.insert(0, category)
        return category_list


class ProductListView(ListView):
    model = Product
