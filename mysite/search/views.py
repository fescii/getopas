from django.shortcuts import render
from django.contrib.auth.models import User
from blog.models import Post
from magazine.models import Issue
from .forms import SearchForm
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

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
            search = form.cleaned_data['search']
            search_vector = SearchVector('title',weight='A') + \
                    SearchVector('body', weight='B')
            search_query = SearchQuery(search)
            results = Post.published.annotate(
                    search = search_vector,
                            rank=SearchRank(search_vector, search_query)
                            ).filter(rank__gte=0.05).order_by('-rank')
            #Newsletters
            search_vector_issue = SearchVector('title',weight='A') + SearchVector('description', weight='B')
            issues = Issue.published.annotate(search = search_vector_issue,
                                              rank=SearchRank(search_vector_issue, search_query))\
                                                  .filter(rank__gte=0.05).order_by('-rank')
            #People
            search_vector_people = SearchVector('first_name',weight='A') + SearchVector('last_name', weight='B')
            people =  User.objects.annotate(search = search_vector_people,
                                              rank=SearchRank(search_vector_people, search_query))\
                                                  .filter(rank__gte=0.05).order_by('-rank')

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
    search_vector = SearchVector('title',weight='A') + \
        SearchVector('description', weight='B')
    search_query = SearchQuery(search)
    results = Issue.published.annotate(
        search = search_vector,
        rank=SearchRank(search_vector, search_query)
        ).filter(rank__gte=0.3).order_by('-rank')
    return render(request,'search/search/search.html',
                                  {'form': form,'query':search,
                                   'section': 'search',
                                   'results': results,
                                   'title': 'newsletters'})