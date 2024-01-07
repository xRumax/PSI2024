import graphene
from graphene_django.types import DjangoObjectType
from appgraphql.models import Book, User, Author, Shop, Review

class AuthorType(DjangoObjectType):
    class Meta:
        model = Author


class BookType(DjangoObjectType):
    class Meta:
        model = Book


class UserType(DjangoObjectType):
    class Meta:
        model = User


class ShopType(DjangoObjectType):
    class Meta:
        model = Shop


class ReviewType(DjangoObjectType):
    class Meta:
        model = Review


class Query(graphene.ObjectType):
    all_authors = graphene.List(AuthorType)
    all_books = graphene.List(BookType)
    all_users = graphene.List(UserType)
    all_reviews = graphene.List(ReviewType)

    def resolve_all_authors(self, info, **kwargs):
        return Author.objects.all()
    
    def resolve_all_books(self, info, **kwargs):
        return Book.objects.all()

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_all_reviews(self, info, **kwargs):
        return Review.objects.all()

schema = graphene.Schema(query=Query)

class CreateAuthor(graphene.Mutation):
    author = graphene.Field(AuthorType)

    class Arguments:
        name = graphene.String()
        date_of_birth = graphene.DateTime()

    def mutate(self, info, **kwargs):
        author = Author(
            name = kwargs.get('name'),
            date_of_birth = kwargs.get('date_of_birth'),
        )    
        author.save()
        return CreateAuthor(author=author)
    

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        name = graphene.String()
        password = graphene.String()
        admin = graphene.Boolean()

    def mutate(self, info, name, password, admin):
        user = User(
            name = name,
            password = password,
            admin = admin, 
        )    
        user.save()
        return CreateUser(user=user)


class CreateReview(graphene.Mutation):
    review = graphene.Field(ReviewType)

    class Arguments:
        user = graphene.Int()
        book = graphene.Int()
        rating = graphene.Float()
        desc = graphene.String()

    def mutate(self, info, **kwargs):
        review = Review(
        user=kwargs.get('user'),
        book=kwargs.get('book'),
        rating=kwargs.get('rating'),
        desc=kwargs.get('desc'),
    ) 
        review.save()
        return CreateReview(review = review)

class CreateBook(graphene.Mutation):
    book = graphene.Field(BookType)

    class Arguments:
        author = graphene.Int()
        name = graphene.String()
        pub = graphene.Int()

    def mutate(self, info, **kwargs):
        book = Book(
        author=kwargs.get('author'),
        name=kwargs.get('name'),
        pub=kwargs.get('pub'),
    )   
        book.save()
        return CreateBook(book = book)
    
class CreateShop(graphene.Mutation):
    shop = graphene.Field(ShopType)

    class Arguments:
        name = graphene.String()
        adress = graphene.String()
        email = graphene.String()
        book = graphene.Int()

    def mutate(self, info, **kwargs):
        shop = Shop(
        name=kwargs.get('name'),
        adress=kwargs.get('adress'),
        email=kwargs.get('email'),
        book=kwargs.get('book'),
    )   
        shop.save()
        return CreateShop(shop = shop)

class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    create_user = CreateUser.Field()
    create_book = CreateBook.Field()
    create_review = CreateReview.Field()
    create_shop = CreateShop.Field()

    