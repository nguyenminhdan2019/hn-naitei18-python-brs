from django.shortcuts import render, redirect, reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .forms import BookForm

from django.core.mail import send_mail

import os
import environ

env = environ.Env()
# reading .env file
environ.Env.read_env()

from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView)

from .models import (
    Book,
    Request,

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

class SearchBookListView(ListView):
    template_name = "books/book_search_result.html"
    model = Book
    paginate_by = 6

    def get_queryset(self):
        queryset = super(SearchBookListView, self).get_queryset()
        choice = self.request.GET.get("choice")
        word = self.request.GET.get("word")
        if word:
            if choice == "category":
                books_by_category = queryset.filter(category__name__icontains=word)
                return books_by_category
            elif choice == "author":
                books_by_author = queryset.filter(author__icontains=word)
                return books_by_author
            else:
                books_by_title = queryset.filter(title__icontains=word)
                return books_by_title
        return queryset
@login_required
def request_form(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            new_request = Request(title = title, author = author, user = request.user )
            new_request.save()
            messages.success(request, "Your request is sent")
            mess = '{0} is send a a request to admin'.format(request.user)
            send_mail(
                subject= 'Request book',
                message='{0} request book with title {1}'.format(request.user, author),
                from_email = env('EMAIL_HOST_USER'),
                recipient_list = [env('EMAIL_ADMIN'), ],
                )
            return redirect('index')
    if request.user.is_authenticated:
        form = BookForm()
        # form.fields['name'].initial = request.user.username
        form.fields['title'].widget.attrs['placeholder'] = 'Write title here'
        form.fields['author'].widget.attrs['placeholder'] = 'Write author here'
        return render(request, 'books/request.html', {'form': form})


