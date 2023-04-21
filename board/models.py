from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
# pprod from cloudinary.models import CloudinaryField
# pprod import cloudinary.uploader

# create mesagges
class Meep(models.Model):
    user=models.ForeignKey(User, related_name='meeps', on_delete = models.DO_NOTHING )
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.user}"
        f" {self.created_at:%d-%m-%Y %H:%M} "
        f"  {self.body}")



# # User profile Model (linked to the django predefined User model  )
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self',
        related_name="followed_by",         ## El related_name es ol opuesto al follows, o sea guarda quienes d ela tabla siguen a este perfil
        symmetrical=False,
        blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)
    preset_image = models.CharField(max_length=50, null=True, blank=True, default="default1.jpg")

    def __str__(self):
        return self.user.username

#Create profile when new user signs up

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        #have the user follow himself
        user_profile.follows.set([instance.profile.id])

post_save.connect(create_profile, sender=User)    #this can be done also with receiver decorator, see code bellow 


# Model for storing user uploaded avatar image
class Avatar(models.Model):
    profile=models.OneToOneField(Profile, on_delete = models.CASCADE )
    # pprod uploaded_image=CloudinaryField('image',folder='avatar', transformation={'height':250, 'width':250, 'crop':"lfill"})
    uploaded_image=models.ImageField(null=True, blank=True, upload_to="images/")

# This signal deletes de img from cloudinary when the image is removed form the database
# pprod @receiver(pre_delete, sender=Avatar)          # using decorator
# pprod def photo_delete(sender, instance, **kwargs):
# pprod    cloudinary.uploader.destroy(instance.uploaded_image.public_id)