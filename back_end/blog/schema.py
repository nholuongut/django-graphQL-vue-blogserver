from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from blog import models
import graphene

# define graphql type , which wrapps the models we defined


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class AuthorType(DjangoObjectType):
    class Meta:
        model = models.Profile


class PostType(DjangoObjectType):
    class Meta:
        model = models.Post


class TagType(DjangoObjectType):
    class Meta:
        model = models.Tag


# define the Query class
class Query(graphene.ObjectType):
    # define query methods with return graphql types
    """
    You use
    graphene.Field if the query should return a single item and
    graphene.List if it will return multiple items
    """
    all_posts = graphene.List(PostType)
    author_by_username = graphene.Field(AuthorType, username=graphene.String())
    post_by_slug = graphene.Field(PostType, slug=graphene.String())
    posts_by_author = graphene.List(PostType, username=graphene.String())
    posts_by_tag = graphene.List(PostType, tag=graphene.String())

    """
    For each of the above attributes, you also create a method to resolve the query:
    """

    # receive all the posts
    def resolve_all_posts(root, info):
        return (
            models.Post.objects.prefetch_related("tags").select_related("author").all()
        )

    # get an author with a given username
    def resolve_author_by_username(root, info, username):
        return models.Profile.objects.select_related("user").get(
            user__username=username
        )

    # get a post with a given slug
    def resolve_post_by_slug(root, info, slug):
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .get(slug=slug)
        )

    # receive all the posts by a given author
    def resolve_posts_by_author(root, info, username):
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(author__user__username=username)
        )

    # receive all the posts with the given tag
    def resolve_posts_by_tag(root, info, tag):
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(tags__name__iexact=tag)
        )


# create a graphene schema
schema = graphene.Schema(query=Query)
