from django.shortcuts import render
from blog.models import Post
from magazine.models import Issue
from .forms import SearchForm
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

# Create your views here.
#Search View
def query_search(request,option='one'):
    form = SearchForm()
    option = option
    search = None
    results = []
    if 'search' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                search = form.cleaned_data['search']

                if option == 'one':
                    search_vector = SearchVector('title',weight='A') + \
                        SearchVector('body', weight='B')
                    search_query = SearchQuery(search)
                    results = Post.published.annotate(
                        search = search_vector,
                        rank=SearchRank(search_vector, search_query)
                        ).filter(rank__gte=0.3).order_by('-rank')
                    return render(request,'search/search/search.html',
                                  {'form': form,'query':search,
                                   'section': 'search',
                                   'results': results,
                                   'title': 'articles'})
                elif option == 'two':
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
    return render(request,
                    'search/search/search.html',
                    {'form': form,
                    'query':search,
                    'section': 'search',
                    'results': results,
                    'option':option})