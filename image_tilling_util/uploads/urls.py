from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from uploads.core import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^uploads/form/$', views.model_form_upload, name='model_form_upload'),
    url(r'^map/(?P<pk>[0-9]+)/$', views.view_map, name='view_map'),
    url(r'^generate_tiles/(?P<upload_id>[0-9]+)/$', views.generate_tiled_images, name='generate_tiled_images'),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
