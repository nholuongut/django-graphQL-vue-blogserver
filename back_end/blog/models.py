from django.db import models
from django.conf import settings

# Create your models here.


class Profile(models.Model):
    # define each attribute related to user profile
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    website = models.URLField(blank=True)
    bio = models.CharField(max_length=240, blank=True)

    def __str__(self) -> str:
        return self.user.get_username()


class Tag(models.Model):
    # define tag model for each type
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    # define the blog post model consists of metadata , contents and tags
    title = models.CharField(max_length=255, unique=True)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    body = models.TextField()
    meta_description = models.CharField(max_length=150, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)

    # integrate authour and tag from different other models
    """
    The on_delete=models.PROTECT argument for author ensures that you won’t accidentally delete an author who still has posts on the blog
    """
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ["-publish_date"]
