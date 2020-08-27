from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import Http404, HttpResponseForbidden
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect
from django.contrib import messages

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
    Rating,
    Comment
)
from .forms import (
    ReviewForm,
    CommentForm,
    BookForm
)

from review.models import Follow

def index(request):
	 return render(request, 'index.html')

class BooksListView(ListView):
    template_name = 'books/books.html'
    model = Book
    def get_context_data(self, **kwargs):
        context = super(BooksListView, self).get_context_data(**kwargs)
        context.update({
            'top_4_books': Book.objects.order_by('-vote')[:4],
        })
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    paginate_by = 6
    review_form = ReviewForm()
    comment_form = CommentForm()

    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'books/book_detail.html', context={'book': book})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = self.review_form
        context['comment_form'] = self.comment_form
        context['ratings'] = Rating.objects.filter(book=self.object)
        return context
        
    def post(self, request, *args, **kwargs):
        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            rating_form = ReviewForm(request.POST)
            comment_form = CommentForm(request.POST)
            if rating_form.is_valid():
                book = self.get_object()
                star = rating_form.cleaned_data['star']
                comment = rating_form.cleaned_data['review']
                new_rating = Rating(star=star, review=comment, book=book, user=self.request.user)
                new_rating.save()
                success_url = reverse_lazy('books')
                success_message = "Thank!"
                return HttpResponseRedirect(url)
            if comment_form.is_valid():
                content = comment_form.cleaned_data['comment']
                review = request.POST.get('rating')
                review_id = int(review[0:len(review)-1])
                new_comment = Comment(comment=content, user=self.request.user, rate= Rating.objects.get(pk=review_id))
                new_comment.save()
                success_url = reverse_lazy('books')
                success_message = "Thank!"
                return HttpResponseRedirect(url)            

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
        else:
            form.fields['title'].widget.attrs['placeholder'] = 'Write title here'
            form.fields['author'].widget.attrs['placeholder'] = 'Write author here'
            return render(request, 'books/request.html', {'form': form})
