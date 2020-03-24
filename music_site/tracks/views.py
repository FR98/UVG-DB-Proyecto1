from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from tracks.models import Track
from userTracks.models import UserTrack

# Create your views here.

@login_required
def index(request):
    user = request.user
    tracks = Track.objects.all()
    return render(
        request,
        'tracks.html', 
        {
            'user': user,
            'tracks': tracks
        }
    )

def detail(request, id):
    return HttpResponse("Hello World, You are at track {id}.".format(id=id))

@login_required
def create(request):
    user = request.user
    return render(
        request,
        'track_create.html',
        {
            'user' : user
        }
    )

@login_required
def create_new(request):
    user = request.user
    try:
        name = request.POST.get('name')
        albumTitle = request.POST.get('albumTitle')
        genreName = request.POST.get('genreName')
        composer = request.POST.get('composer')
        milliseconds = request.POST.get('milliseconds')
        unitprice = 0.9
        album = Album.objects.get_or_create(title = albumTitle)
        genre = Genre.objects.get_or_create(name = genreName)
        track = Track.objects.get_or_create(
            name = name,
            albumid = album.id,
            genreid = genre.id,
            composer = composer,
            milliseconds = milliseconds,
            unitprice = unitprice,
        )
        userTrack = UserTrack.objects.create(trackid = track.id, userid = user.id)
    except Track.DoesNotExist:
        raise Http404("Track does not exist")
    return redirect('tracks:index')

@login_required
def update(request, id):
    try:
        track = Track.objects.get(pk = id)
    except Track.DoesNotExist:
        raise Http404("Track does not exist")
    return render(
        request,
        'track_edit.html',
        {
            'track' : track
        }
    )

@login_required
def update_object(request, id):
    try:
        name = request.POST.get('name')
        albumTitle = request.POST.get('albumTitle')
        genreName = request.POST.get('genreName')
        composer = request.POST.get('composer')
        milliseconds = request.POST.get('milliseconds')
        unitprice = 0.9
        album = Album.objects.get_or_create(title = albumTitle)
        genre = Genre.objects.get_or_create(name = genreName)
        track = Track.objects.filter(pk = id).update(
            name = name,
            albumid = album.id,
            genreid = genre.id,
            composer = composer,
            milliseconds = milliseconds,
            unitprice = unitprice,
        )
    except Track.DoesNotExist:
        raise Http404("Track does not exist")
    return redirect('tracks:index')

@login_required
def delete(request, id):
    try:
        track = Track.objects.get(pk = id)
        track.delete()
    except Track.DoesNotExist:
        raise Http404("Track does not exist")
    return redirect('tracks:index')
