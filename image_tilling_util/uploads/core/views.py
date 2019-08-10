from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404

from uploads.core.models import Document, TiledDocument
from uploads.core.forms import DocumentForm
from django.http import HttpResponse

from utils import tiling
import os

def home(request):
    documents = Document.objects.all()
    tiled = TiledDocument.objects.all()
    return render(request, 'core/home.html', { 'images': documents,
                                               'tiled_images': tiled})

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'core/model_form_upload.html', {
        'form': form
    })

def view_map(request, pk):
    tiled = get_object_or_404(TiledDocument, pk=pk)
    return render(request, 'core/map.html', {'map_id': tiled.id,
                                             'tiles_folder': tiled.tiles_folder,
                                             'size_x': tiled.size_x,
                                             'size_y': tiled.size_y})

def generate_tiled_images(request, upload_id):
    upload = Document.objects.filter(id=upload_id).get()
    url = upload.document.url
    file_path = url.strip("/")
    save_dir = "media/tiled_images/" + upload_id
    # Create needed directories
    try:
        os.makedirs(save_dir)
    except e:
        print(e)

    # Tile images
    [sx, sy] = tiling.generate_tiles(file_path, save_dir)

    # Create new tiledDocument
    tiled = TiledDocument(description=upload.description, tiles_folder="/"+save_dir,
                          size_x=sx, size_y=sy)
    tiled.save()

    # Remove original image
    upload.delete()

    return redirect('/')
