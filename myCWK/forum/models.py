from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from myCWK.validators import validate_file_extension

class Post(models.Model):
    title = models.CharField(max_length=400)
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upvotes = models.ManyToManyField(User, related_name="post_upvotes", blank=True)
    downvotes = models.ManyToManyField(User, related_name="post_downvotes", blank=True)

    # Attachments with file type validation
    image = models.ImageField(upload_to="post_images/", null=True, blank=True, validators=[validate_file_extension])
    file = models.FileField(upload_to="post_files/", null=True, blank=True, validators=[validate_file_extension])

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:390]
            super(Post, self).save(*args, **kwargs)  
            unique_id = self.id
            self.slug = f"{base_slug}-{unique_id}" 
            self.save(update_fields=["slug"])
        else:
            super(Post, self).save(*args, **kwargs)

    def total_votes(self):
        return self.upvotes.count() - self.downvotes.count()

    def __str__(self):
        return self.title


class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="replies")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="children")
    slug = models.SlugField(max_length=400, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Attachments with file type validation
    image = models.ImageField(upload_to="reply_images/", null=True, blank=True, validators=[validate_file_extension])
    file = models.FileField(upload_to="reply_files/", null=True, blank=True, validators=[validate_file_extension])

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == "":
            base_slug = slugify(f"{self.post.title}-{self.author.username[:6]}")[:390]
            slug = base_slug
            counter = 1

            while Reply.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug  # Assign unique slug

        super(Reply, self).save(*args, **kwargs)
