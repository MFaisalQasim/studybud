from django.db import models

# Create your models here.
class Profile(models.Model):

    name = models.CharField(("name"), max_length=50)
    email = models.EmailField(("email"), max_length=254)
    about =  models.TextField(("about"), null=True, blank=True)

    def __str__(self):
        return self.name