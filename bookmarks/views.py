from django.shortcuts import render
from django.template import Context
from django.contrib.auth.models import User
from django.http import Http404

def main_page(request):

    variables = Context({
        'head_title':'Django Bookmarks',
       'page_title':'Welcome to Django Bookmarks',
       'page_body':'Where you can store and share bookmarks!'})
    return render(request, 'main_page.html',variables)

def user_page(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404('Requested User Not Found!')

    bookmarks = user.bookmark_set.all() #I don't really understand this syntax

    variables = Context({
        'username':username,
        'bookmarks':bookmarks
    })

    return render(request, 'user_page.html', variables)
