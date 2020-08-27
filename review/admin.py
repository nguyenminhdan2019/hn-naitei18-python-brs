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

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fields = ('title', 'author', 'image')

    list_display = ('title', 'author')
    search_fields = ['title']

@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ['name']

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'author', 'status')
