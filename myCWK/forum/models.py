from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify



#Creating my model for the Posts
class Post(models.Model):
  title = models.CharField(max_length=400)
  #slug is a short label for something, containing only letters, numbers, underscores or hyphens. They’re generally used in URLs. For example, in a typical blog entry URL: https://www.djangoproject.com/weblog/2008/apr/12/spring/ the last bit (spring) is the slug.
  # Has to be used in order to generate a link for each post to be clicked into
  slug = models.SlugField(max_length=400, unique = True, blank = True)
  content = models.TextField() #post content goes here
  author = models.ForeignKey(User, on_delete=models.CASCADE) #User who created the post
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def save(self, *args, **kwargs):
    if not self.slug: #only generate slug if not set url
      self.slug = slugify(self.title)
    super(Post, self).save(*args,**kwargs)

  def __str__(self):
    return self.title