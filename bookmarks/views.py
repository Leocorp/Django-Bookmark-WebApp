from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404

from bookmarks.forms import *
from bookmarks.models import Link, Bookmark, Tag
from django.contrib.auth.decorators import login_required

def main_page(request):

    variables = RequestContext(
        request,{
        'user': request.user, #parsing the logged in user's object to the main page
        'head_title':'Django Bookmarks',
       'page_title':'Welcome to Django Bookmarks',
       'page_body':'Here you can store and share bookmarks.'})
    return render_to_response('main_page.html',variables)

def user_page(request, username):
    user = get_object_or_404(User, username= username)
    bookmarks = user.bookmark_set.order_by('-id')
    variables = RequestContext(
        request,
        {
        'username':username,
        'bookmarks':bookmarks,
            'show_tags': True,
    })


    return render_to_response('user_page.html', variables)

def tag_page(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    bookmarks = tag.bookmark.order_by('-id') #Descending order
    variables = RequestContext(request, {
        'bookmarks':bookmarks,
        'tag_name':tag_name,
        'show_tags':True,
        'show_user':True,
    })
    return render_to_response('tag_page.html', variables)

def tag_cloud_page(request):
    MAX_WEIGHT = 5
    tags = Tag.objects.order_by('name')
    min_count = max_count = tags[0].bookmark.count()
    for tag in tags:
        tag.count = tag.bookmark.count()
        if tag.count < min_count:
            min_count = tag.count
        if max_count < tag.count:
            max_count = tag.count
        #compute range to avoid a division by zero
        range = float(max_count - min_count)
        if range == 0:
            range = 1.0
        #calculate weight
    for tag in tags:
        tag.weight = int(MAX_WEIGHT * (tag.count - min_count)/range)
    variables = RequestContext(request, {
        'tags':tags
    })
    return render_to_response('tag_cloud_page.html', variables)


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

@login_required(login_url='/login/')
def bookmark_save_page(request):
    if request.method == 'POST':
        form = BookmarkSaveForm(request.POST)
        if form.is_valid():
            bookmark = _bookmark_save(request, form)
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

def _bookmark_save(request, form):
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
        return bookmark


def search_page(request):
    form = SearchForm() #pass this form to the render on initial visit ; when there is no query
    bookmarks = []
    show_results = False
    query = request.GET.get('ajaxquery', None)
    if query:
        show_results = True
        form = SearchForm({'query':query})
        bookmarks = Bookmark.objects.filter(title__icontains = query)[:10] #fetch the bookmarks with their tags

    variables = RequestContext(request, {
        'form':form,
        'bookmarks':bookmarks,
        'show_results':show_results,
        'show_tags': True,
        'show_user':True,
    })

    if request.GET.get('ajaxquery'):
        return render_to_response('bookmark_list.html', variables)
    else:
        return render_to_response('search.html', variables)