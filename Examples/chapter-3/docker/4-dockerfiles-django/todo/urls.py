from django.conf.urls import url
from todo.views import index, delete, create, update

urlpatterns = [
    url(r'^$', index, name='list'),
    url(r'^create$', create, name='create'),
    url(r'^delete$', delete, name='delete'),
    url(r'^update$', update, name='update'),
]
