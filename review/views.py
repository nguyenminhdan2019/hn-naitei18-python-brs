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

from django.contrib.auth.mixins import LoginRequiredMixin
env = environ.Env()
# reading .env file
environ.Env.read_env()

from django.forms import model_to_dict
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import Http404, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic import (
    View,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView)
from django.views.generic.edit import FormMixin

from .models import (
    Book,
    Request,
    Rating,
    Comment,
    BookMark,
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

    def get_success_url(self):
        return reverse('book-detail', kwargs={'pk': self.object.pk})

    # def book_detail_view(self, request, primary_key):
    #     book = get_object_or_404(Book, pk=primary_key)
    #     bookmark = BookMark.objects.filter(user=self.request.user.id, book=book.id)
    #     print(bookmark)
    #     return render(request, 'books/book_detail.html', context={'book': book, 'bookmark': bookmark})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['book'] = book
        if BookMark.objects.filter(user=self.request.user.id, book=book.id).first():
            context['bookmark'] = BookMark.objects.filter(user=self.request.user.id, book=book.id).first()
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
            return redirect('list-request')
        else:
            return render(request, 'books/request.html', {'form': form})
    form = BookForm()
    # form.fields['name'].initial = request.user.username
    form.fields['title'].widget.attrs['placeholder'] = 'Write title here'
    form.fields['author'].widget.attrs['placeholder'] = 'Write author here'
    return render(request, 'books/request.html', {'form': form})

@login_required
def list_request(request):
    try:
        requests = Request.objects.filter(user = request.user)
    except requests.DoesNotExist:
        raise Http404('Request does not exist')
    return render(request, 'books/list_request.html', context={'requests': requests})

class MarkFavorite(generic.View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        try:
            mark = BookMark.objects.get(user = self.request.user, book = Book.objects.get(id=pk))
            mark.fa_status = self.request.POST['fa_status']
            if mark.fa_status == 'fa':
                stt = 'fa'
            else:
                stt = 'un_fa'
            mark.save()
            return JsonResponse({'serializedData': model_to_dict(mark), 'stt': stt}, status=200)
        except:
            mark = BookMark()
            mark.user = self.request.user
            mark.book = Book.objects.get(id=pk)
            mark.fa_status = self.request.POST['fa_status']
            if mark.fa_status == 'fa':
                stt = 'fa'
            else:
                stt = 'un_fa'
            mark.save()
            return JsonResponse({'serializedData': model_to_dict(mark), 'stt': stt}, status=200)

class MarkRead(generic.View):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        try:
            mark = BookMark.objects.get(user = self.request.user, book = Book.objects.get(id=pk))
            mark.mark_status = self.request.POST['mark_status']
<<<<<<< HEAD
            if mark.mark_status == 'nr':
                stt = 'nr'
            elif mark.mark_status == 'r_ing' :
                stt = 'r_ing'
            else:
                stt = 'r_ed'
            mark.save()
            return JsonResponse({'serializedData': model_to_dict(mark), 'stt': stt}, status=200)
=======
            mark.save()
            return JsonResponse({'serializedData': model_to_dict(mark)}, status=200)
>>>>>>> 2c7c16d... Mark a book
        except:
            mark = BookMark()
            mark.user = self.request.user
            mark.book = Book.objects.get(id=pk)
            mark.mark_status = self.request.POST['mark_status']
            if mark.mark_status == 'nr':
                stt = 'nr'
            elif mark.mark_status == 'r_ing' :
                stt = 'r_ing'
            else:
                stt = 'r_ed'
            mark.save()
            return JsonResponse({'serializedData': model_to_dict(mark), 'stt': stt}, status=200)
