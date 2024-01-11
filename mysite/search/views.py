from django.shortcuts import render
from django.contrib.auth.models import User
from blog.models import Post
from magazine.models import Issue

from .forms import SearchForm
# from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

# Create your views here.
#Search View
def query_search(request,option = 'one'):
    form = SearchForm()
    option = 'one'
    search = None
    results = []
    if 'search' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            search = str(form.cleaned_data['search'])
            # search_e = PostDocument.search().filter("contains", name=search)
            # results =  search_e.to_queryset()
            results =  Post.objects.filter(title__icontains=search ) | Post.objects.filter(body__icontains=search )

            #Newsletters
            # search_vector_issue = IssueDocument.search().filter("contains", name=search)
            # issues = search_vector_issue.to_queryset()
            issues =  Issue.objects.filter(title__icontains=search) | Issue.objects.filter(description__icontains=search)

            #People
            # search_vector_people = UserDocument.search().filter("contains", name=search)
            people =  User.objects.filter(first_name__icontains=search) | User.objects.filter(last_name__icontains=search)

            return render(request,'search/search/search.html',
                                    {'form': form,'query':search,
                                    'section': 'search',
                                    'results': results,
                                    'issues': issues,'tab': 'search',
                                    'people': people,
                                    'title': 'articles'})
    return render(request,
                    'search/search/search.html',
                    {'form': form,
                    'query':search,'tab': 'search',
                    'section': 'search',
                    'results': results,
                    'option':option})

    form = SearchForm()
    search = str(search)
    results = []
    return render(request,'search/search/search.html',
                                  {'form': form,'query':search,
                                   'section': 'search',
                                   'results': results,
                                   'title': 'newsletters'})