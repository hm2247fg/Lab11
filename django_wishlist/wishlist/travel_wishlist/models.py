from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
# Create your models here.


class Place(models.Model):
    # Model representing a place in the travel wishlist
    # Field to store the name of the place
    name = models.CharField(max_length=200)
    # Field to indicate whether the place has been visited or not
    visited = models.BooleanField(default=False)

    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # get reference to previous version of this Place
        old_place = Place.objects.filter(pk=self.pk).first()
        if old_place and old_place.photo:
            if old_place.photo != self.photo:
                self.delete_photo(old_place.photo)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.photo:
            self.delete_photo(self.photo)

        super().delete(*args, **kwargs)

    def delete_photo(self, photo):
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)

    # Method to return a string representation of the object
    def __str__(self):
        # Return a string containing the name of the place and its visited status
        return f'{self.name}, visited? {self.visited}'

    def mark_as_visited(self):
        # Set the 'visited' attribute to True
        self.visited = True
        # Save the changes to the database
        self.save()
