from django.shortcuts import render
from .models import Book, BookInstance, Author
from django.views import generic
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AuthorListView(generic.ListView):
    model = Author
    queryset = Author.objects.all()
    paginate_by = 10
   
class AuthorDetailView(generic.DetailView):
    model = Author
    # paginate_by = 5

    # this is how to pahinate a one to many relationship in a detail view
    """
    def get_context_data(self, **kwargs):
        object_list = Book.objects.filter(author=self.get_object())
        context = super(AuthorDetailView, self).get_context_data(object_list=object_list, **kwargs)
        return context
        """


# for function bassed views I have to define the model queries myself and insert it into context

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'   # template for jinja variable
    # template_name = 'books/my_arbitrary_template_name_list.html'   Use to specify template directory 
    queryset = Book.objects.all() # get all books  for the homepage
    paginate_by = 20

    """
    # this is the same as above
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['book_list'] = self.queryset
        return context
    """

class BookDetailView(generic.DetailView):
    model = Book

# basic function based views
def index(request):
    count_books = Book.objects.count()
    count_instances = BookInstance.objects.count()
    count_instances_available = BookInstance.objects.filter(status__exact='a').count()
    count_authors = Author.objects.count()
    count_books_containing_Rick = Book.objects.filter(title__contains='Rick').count()
    
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'title': 'Index Page',
        'count_books': count_books,
        'count_books_containing_Rick': count_books_containing_Rick,
        'count_instances': count_instances,
        'count_instances_available': count_instances_available,
        'count_authors': count_authors,
        'num_visits': num_visits,
    }

    return render(request, 'catalog/index.html', context=context)