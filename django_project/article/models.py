from django.db import models
from django.conf import settings
from django.urls import reverse
from django.template.defaultfilters import slugify
# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length= 225)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add= True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(null= False, unique=True)

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        # return reverse("article_detail", kwargs={"pk": self.pk})
        return reverse("article_detail", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.CharField(max_length=140)
    author  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.comment
    
    def get_absolute_url(self):
        return reverse("home")
    