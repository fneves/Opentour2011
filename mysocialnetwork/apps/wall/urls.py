from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'wall.views.allposts', name="all_posts"),
    url(r'^yours/$', 'wall.views.yourposts', name="your_posts"),
    url(r'^add/$', 'wall.views.post', name="add_post"),
    url(r'^share/(?P<uuid>[-0-9a-f]{36})/$', 'wall.views.share', name="share"),
    url(r'^like/(?P<uuid>[-0-9a-f]{36})/$', 'wall.views.like', name="like"),
    url(r'^dislike/(?P<uuid>[-0-9a-f]{36})/$', 'wall.views.dislike', name="dislike"),
)