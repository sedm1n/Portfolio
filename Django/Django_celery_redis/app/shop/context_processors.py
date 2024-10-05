from .models import Category


def categories(request):
      """
            Context processor for categories.
      
             Returns a dictionary with a single key `categories` containing a QuerySet of root categories.
      """
      
      categories = Category.objects.filter(parent=None)
      return {
            "categories": categories
      }