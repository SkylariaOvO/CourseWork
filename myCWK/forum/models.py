from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Post(models.Model):
  title = models.CharField(max_length=400)
  slug = models.SlugField(max_length=400, unique=True, blank=True)
  content = models.TextField()
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def save(self, *args, **kwargs):
    if not self.slug:
      base_slug = slugify(self.title)[:390]
      slug = base_slug
      counter = 1

      while Post.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

      self.slug = slug  # Assign unique slug

    super(Post, self).save(*args, **kwargs)

  def __str__(self):
    return self.title
