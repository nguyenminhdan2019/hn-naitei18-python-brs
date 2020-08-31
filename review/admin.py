from django.contrib import admin
from .models import (
    Book,
    Category,
    BookMark,
    Request,
    Rating,
    Comment,
    Follow, 
    Activity,

)
# Register your models here.

admin.site.register(Book)

admin.site.register(Category)


admin.site.register(Request)

