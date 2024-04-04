from django.urls import path
from . import views

# URL patterns for the travel wishlist application
urlpatterns = [
    # URL pattern for displaying the list of places on the homepage
    path('', views.place_list, name='place_list'),
    # URL pattern for displaying the list of visited places
    path('visited', views.places_visited, name='places_visited'),
    # URL pattern for marking a place as visited
    path('place/<int:place_pk>/was_visited', views.place_was_visited, name='place_was_visited'),
    # URL pattern for displaying details of a specific place
    path('place/<int:place_pk>', views.place_details, name='place_details'),
    # URL pattern for deleting a specific place
    path('place/<int:place_pk>/delete', views.delete_place, name='delete_place'),
]
