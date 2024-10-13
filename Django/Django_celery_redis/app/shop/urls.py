from django.urls import path
from .views import ProductListView, product_detail_view, category_list_view

app_name = "shop"

urlpatterns = [
      path("", ProductListView.as_view(), name="products"),
      path("<slug:slug>/", product_detail_view, name="product_detail"),
      path("search/<slug:slug>/", category_list_view, name="category_list"),
]