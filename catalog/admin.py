from django.contrib import admin
from .models import Book, BookInstance, Genre, Author, Language

# Register your models here.

admin.site.register(Genre)
admin.site.register(Language)
 

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    
    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )

class AuthorInstanceInline(admin.TabularInline):
    # what model you want to appear
    model = Book

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # does not display manytomany fields as it takes high memory costs
    list_display = ('title', 'author', 'language', 'display_genre')
    # inlines is where you want the fields to appear on admin
    inlines = [BooksInstanceInline]

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # will display in admin site the details of each field with sort functionality
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # where you want the model to appear as an inline tab
    inlines = [AuthorInstanceInline]
