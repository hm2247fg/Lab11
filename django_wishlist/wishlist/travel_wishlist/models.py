from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
# Create your models here.


# Model representing a place in the travel wishlist
class Place(models.Model):
    # Field to store the name of the place
    name = models.CharField(max_length=200)
    # Field to indicate whether the place has been visited or not
    visited = models.BooleanField(default=False)
    # Field to associate a place with a user
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE)
    # Field to store additional notes about the place
    notes = models.TextField(blank=True, null=True)
    # Field to store the date when the place was visited
    date_visited = models.DateField(blank=True, null=True)
    # Field to store the photo of the place
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Override the save method to handle photo deletion
        old_place = Place.objects.filter(pk=self.pk).first()  # Get reference to previous version of this Place
        if old_place and old_place.photo:
            if old_place.photo != self.photo:  # If photo has changed
                self.delete_photo(old_place.photo)  # Delete the old photo

        super().save(*args, **kwargs)  # Call the original save method

    def delete(self, *args, **kwargs):
        # Override the delete method to handle photo deletion
        if self.photo:  # If photo exists
            self.delete_photo(self.photo)  # Delete the photo

        super().delete(*args, **kwargs)  # Call the original delete method

    def delete_photo(self, photo):
        # Method to delete the photo from storage
        if default_storage.exists(photo.name):  # If photo exists in storage
            default_storage.delete(photo.name)  # Delete the photo from storage

    # Method to return a string representation of the object
    def __str__(self):
        # Return a string containing the name of the place and its visited status
        return f'{self.name}, visited? {self.visited}'

    def mark_as_visited(self):
        # Method to mark a place as visited
        self.visited = True  # Set the 'visited' attribute to True
        self.save()  # Save the changes to the database