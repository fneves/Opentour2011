from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from wall.models import Post
from wall.forms import PostForm
from django.template.loader import render_to_string
from django.conf import settings
from socialregistration.middleware import Facebook
import facebook


@login_required    
def allposts(request):
    posts = Post.objects.all().order_by('-pub_date')
    post_form = PostForm()
    return render_to_response("wall/wall.html", {
        "posts": posts,
        "list": 'all',
        "post_form": post_form
    }, context_instance=RequestContext(request))

@login_required
def yourposts(request):
    post_form = PostForm()
    yourposts = Post.objects.filter(publisher=request.user).order_by('-pub_date')
    return render_to_response("wall/wall.html", {
        "posts": yourposts,
        "list": 'yours',
        "post_form": post_form
    }, context_instance=RequestContext(request))

@login_required
def post(request):
    # POST request
    if request.method == "POST":
        previous_list = request.POST['previous_list']
        post_form = PostForm(request.POST)
        
        if post_form.is_valid():
            # from ipdb import set_trace; set_trace()
            new_post = post_form.save(commit=False)
            new_post.publisher = request.user
            new_post.save()
            #request.user.message_set.create(message=_("You have successfully posted a message ") )
            if previous_list == "yours":
                return HttpResponseRedirect(reverse("wall.views.yourposts"))
            else:
                return HttpResponseRedirect(reverse("wall.views.allposts")) 
    # GET request
    else:
        return HttpResponseRedirect(reverse("wall.views.yourposts"))
    # generic case
    return HttpResponseRedirect(reverse("wall.views.yourposts"))


@login_required
def share(request,uuid):
    post = Post.objects.get(uuid=uuid)
    user = facebook.get_user_from_cookie(request.COOKIES, settings.FACEBOOK_API_KEY, settings.FACEBOOK_SECRET_KEY)
    if user:
        graph = facebook.GraphAPI(user["access_token"])
        graph.put_wall_post(message=post.text,profile_id="129427383797915")
    
    return HttpResponseRedirect(reverse("wall.views.allposts"))

@login_required
def like(request, uuid):
    post = Post.objects.get(uuid=uuid)
    post.likes_set.create(post = post,description='like',liker=request.user)
    post.save()
    return HttpResponseRedirect(reverse("wall.views.allposts"))

@login_required
def dislike(request,uuid):
    post = Post.objects.get(uuid=uuid)
    post.likes_set.create(post = post,description='dislike',liker=request.user)
    post.save()
    return HttpResponseRedirect(reverse("wall.views.allposts"))
    