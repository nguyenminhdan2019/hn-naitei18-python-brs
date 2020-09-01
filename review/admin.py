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

admin.site.register(BookMark)

admin.site.register(Request)

admin.site.register(Rating)

admin.site.register(Comment)

admin.site.register(Follow)

admin.site.register(Activity)
