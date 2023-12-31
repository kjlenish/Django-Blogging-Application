from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,null=True, on_delete=models.CASCADE)
    profile_img = models.ImageField(default='profile_picture\default.jpg', upload_to='profile_picture', verbose_name='Profile Picture')
    country_code = models.CharField(max_length=5, default=None, blank=True, null=True)
    phone = models.CharField(max_length=15, default=None, blank=True, null=True)
    dob = models.DateField(default=None, blank=True, null=True, verbose_name='DOB')
    fav_mov = models.TextField(default=None, blank=True, null=True, verbose_name='Favorite Movie')
    date_created = models.DateField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile "
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.profile_img.path)

            if img.height > 400 or img.width >400:
                max_size = (400, 400)
                img.thumbnail(max_size)
                img.save(self.profile_img.path)
        except:
            pass
