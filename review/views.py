from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView)

from .models import (
    Book,
)

def index(request):
	 return render(request, 'index.html')

class BooksListView(ListView):
    template_name = 'books/books.html'
    model = Book
    def get_context_data(self, **kwargs):
        context = super(BooksListView, self).get_context_data(**kwargs)
        context.update({
            'top_4_books': Book.objects.order_by('-vote')[:4],
            # 'most_reviews': Book.objects.annotate(reviews_count=Count('reviews')).order_by('-reviews_count')[:3],
            # 'most_comments': Book.objects.annotate(comments_count=Count('comments')).order_by('-comments_count')[:3],
        })
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'

    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'books/book_detail.html', context={'book': book})
