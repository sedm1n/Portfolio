from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
      list_display = ['name','parent' ,'slug']
      ordering = ['name']
      
      def get_prepopulated_fields(self, request: HttpRequest, obj: Any | None = ...) -> dict[str, tuple[str]]:
            return {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
      list_display = ['title','brang','slug','price','available', 'created_at', 'updated_at']
      ordering = ['title']
      list_filter = ['available', 'created_at', 'updated_at']
 
      def get_prepopulated_fields(self, request: HttpRequest, obj: Any | None = ...) -> dict[str, tuple[str]]:
            return {'slug': ('title',)}
      

      