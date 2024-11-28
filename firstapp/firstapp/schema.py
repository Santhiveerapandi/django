# import graphene
# from graphene_django.types import DjangoObjectType
# from firstapp.models import Department


from graphene_django.types import DjangoObjectType
from .models import Book
import graphene

# Define a GraphQL type for the Department model
""" class DepartmentType(DjangoObjectType):
    class Meta:
        model = Department

# Define Query class
class Query(graphene.ObjectType):
    departments = graphene.List(DepartmentType)

    def resolve_departments(root, info, **kwargs):
        return Department.objects.all() """


class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "published_date")

class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)

    def resolve_all_books(root, info):
        return Book.objects.all()


class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        published_date = graphene.Date(required=True)

    book = graphene.Field(BookType)

    def mutate(self, info, title, author, published_date):
        book = Book.objects.create(title=title, author=author, published_date=published_date)
        return CreateBook(book=book)

class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        author = graphene.String()
        published_date = graphene.Date()

    book = graphene.Field(lambda: BookType)

    def mutate(self, info, id, title=None, author=None, published_date=None):
        try:
            book = Book.objects.get(pk=id)
        except Book.DoesNotExist:
            raise Exception("Book not found")

        if title:
            book.title = title
        if author:
            book.author = author
        if published_date:
            book.published_date = published_date

        book.save()
        return UpdateBook(book=book)


class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            book = Book.objects.get(pk=id)
            book.delete()
            return DeleteBook(success=True)
        except Book.DoesNotExist:
            raise Exception("Book not found")

class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

# schema = graphene.Schema(query=Query)
