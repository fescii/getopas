from optparse import Option
from django.shortcuts import render
from blog.models import Post
from magazine.models import Issue
from devices.models import Product
from .forms import SearchForm
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

# Create your views here.
#Search View
def query_search(request):
    form = SearchForm()
    query = None
    results = []

    form = SearchForm(request.GET)
    option = request.Get.get('option')
    #Search In Articles
    if option == 'one':
        if 'query' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                search_vector = SearchVector('title',weight='A') + \
                    SearchVector('body', weight='B')
                search_query = SearchQuery(query)
                results = Post.published.annotate(
                    search = search_vector,
                    rank=SearchRank(search_vector, search_query)
                    ).filter(rank__gte=0.3).order_by('-rank')
        return render(request,
                    'search/search/search.html',
                    {'form': form,
                    'query':query,
                    'results': results})

    elif option == 'two':
        if 'query' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                search_vector = SearchVector('title',weight='A') + \
                    SearchVector('description', weight='B')
                search_query = SearchQuery(query)
                results = Issue.published.annotate(
                    search = search_vector,
                    rank=SearchRank(search_vector, search_query)
                    ).filter(rank__gte=0.3).order_by('-rank')
        return render(request,
                    'search/search/search.html',
                    {'form': form,
                    'query':query,
                    'results': results})

    elif option == 'three':
        if 'query' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                search_vector = SearchVector('name',weight='A') + \
                    SearchVector('about', weight='B')
                search_query = SearchQuery(query)
                results = Product.published.annotate(
                    search = search_vector,
                    rank=SearchRank(search_vector, search_query)
                    ).filter(rank__gte=0.3).order_by('-rank')
        return render(request,
                    'search/search/search.html',
                    {'form': form,
                    'query':query,
                    'results': results})