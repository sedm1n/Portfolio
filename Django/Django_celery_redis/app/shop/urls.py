from django.urls import path
from .views import ProductListView, product_detail_view, category_list_view, search_products

app_name = "shop"

urlpatterns = [
      path("", ProductListView.as_view(), name="products"),
      path("search-products/", search_products, name="search-products"),
      path("search/<slug:slug>/", category_list_view, name="category_list"),
      path("<slug:slug>/", product_detail_view, name="product_detail"),
]