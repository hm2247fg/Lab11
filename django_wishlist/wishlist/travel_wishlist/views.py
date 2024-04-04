from django.shortcuts import render, redirect, get_object_or_404            # Importing necessary functions for rendering views and redirecting
from .models import Place                                                    # Importing the Place model
from .forms import NewPlaceForm, TripReviewForm                               # Importing form classes for creating and reviewing places
from django.contrib.auth.decorators import login_required                    # Importing decorator for restricting access to logged-in users
from django.contrib import messages                                          # Importing module for displaying messages
from django.http import HttpResponseForbidden                                # Importing HTTP response class for forbidden access


@login_required
def place_list(request):
    """
    View function for displaying the list of places.
    If a POST request is received, the user clicked the Add button in the form.
    Check if the new place is valid, if so, save a new Place to the database, and redirect to this same page.
    If not a POST request, or Place is not valid, display a page with a list of places and a form to add a new place.
    """
    if request.method == 'POST':
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False)
        place.user = request.user  # Associate the place with the current logged-in user
        if form.is_valid():
            place.save()
            return redirect('place_list')

    # If not a POST request, or the form is not valid, display the page with the form and place list
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': form})


@login_required
def places_visited(request):
    """ View function for displaying the list of visited places """
    visited = Place.objects.filter(user=request.user).filter(visited=True).order_by('name')
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})


@login_required
def place_was_visited(request, place_pk):
    """
    View function for marking a place as visited.
    If a POST request is received, mark the place as visited and redirect to the place list.
    """
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:  # Only let a user visit their own places
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect('place_list')


@login_required
def delete_place(request, place_pk):
    """ View function for deleting a place """
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()


@login_required
def place_details(request, place_pk):
    """
    View function for displaying details of a place and allowing the user to update trip information.
    If a POST request is received, save the form data and display appropriate messages.
    """
    place = get_object_or_404(Place, pk=place_pk)

    if place.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)  # Instance = model object to update with the form data
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)  # Temporary error message - future version should improve

        return redirect('place_details', place_pk=place_pk)

    else:  # GET place details
        if place.visited:
            review_form = TripReviewForm(instance=place)  # Pre-populate with data from this Place instance
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form})

        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place})
