from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.template import RequestContext

from bookmarks.forms import *
from bookmarks.models import Link, Bookmark, Tag

def main_page(request):

    variables = RequestContext(
        request,{
        'user': request.user, #parsing the logged in user's object to the main page
        'head_title':'Django Bookmarks',
       'page_title':'Welcome to Django Bookmarks',
       'page_body':'Here you can store and share bookmarks.'})
    return render_to_response('main_page.html',variables)

def user_page(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404('Requested User Not Found!')

    bookmarks = user.bookmark_set.all() #gets all data instances in Bookmark table belonging to the User.
                                        # Created by django when the two tables were linked.

    variables = RequestContext(
        request,
        {
        'username':username,
        'bookmarks':bookmarks
    })


    return render_to_response('user_page.html', variables)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/') #Redirect to the main page, logged out!

def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username= form.clean_username(),
                email= form.clean_email(),
                password= form.clean_password2()
            )
            return HttpResponseRedirect('success')

        #Reload page with errors if form is_not valid
        variables = RequestContext(request,{
            'form':form
        })
        return render_to_response('registration/register.html',variables) #use hierarchical path

    else:
        form = RegistrationForm()
        variables = RequestContext(request,{
            'form':form
        })
        return render_to_response('registration/register.html',variables) #use hierarchical path

def bookmark_save_page(request):
    if request.method == 'POST':
        form = BookmarkSaveForm(request.POST)
        if form.is_valid():
            #Create or get Link
            link, dummy = Link.objects.get_or_create(url=form.cleaned_data['url'])
            bookmark, created = Bookmark.objects.get_or_create(user=request.user, link = link)
            #update the bookmark title
            bookmark.title = form.cleaned_data['title']
            if not created:
                bookmark.tag_set.clear()

            #create new tag list
            tagnames = form.cleaned_data['tags'].split()
            for tagname in tagnames:
                tag, dummy = Tag.objects.get_or_create(name=tagname)
                bookmark.tag_set.add(tag)
            bookmark.save()

            return HttpResponseRedirect('/user/%s/' % request.user.username)
        else:
            variables = RequestContext(request, {
                'form':form
            })
            return render_to_response('bookmark_save.html',variables)
    form = BookmarkSaveForm()
    variables = RequestContext(request, {
                'form':form
            })
    return render_to_response('bookmark_save.html', variables)