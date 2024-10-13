from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from .models import Category, ProductProxy



class ProductListView(ListView):
      model = ProductProxy
      template_name = "shop/products.html"
      context_object_name = "products"

      paginate_by = 15

      def get_template_names(self) -> list[str]:
            if self.request.htmx:
                  return ["shop/components/product_list.html"]
            return "shop/products.html"

      def get_queryset(self):
            return ProductProxy.objects.all()

# def products_view(request):
#       products = ProductProxy.objects.all()

#       return render(request, "shop/products.html", {"products": products})

def product_detail_view(request, slug):
      product = get_object_or_404(ProductProxy, slug=slug)
      return render(request, "shop/product_detail.html", {"product": product})

def category_list_view(request, slug):
      category = get_object_or_404(Category, slug=slug)
      products = ProductProxy.objects.select_related("category").filter(category=category)
      context = {"category": category, "products": products}

      return render(request, "shop/category_list.html", context)
