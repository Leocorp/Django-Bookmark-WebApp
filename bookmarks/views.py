from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.template import RequestContext

from bookmarks.forms import *

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