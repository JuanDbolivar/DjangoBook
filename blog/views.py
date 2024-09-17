from django.shortcuts import render, get_object_or_404
from .models import Post
# from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

# Create your views here.


class PostListView(ListView):
    """Alternative post list view"""
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request):
    post_list = Post.published.all()
    # se instancia el Paginador con la clase y el numero de elementos por pagina
    paginator = Paginator(post_list, 3)
    # se recupera los parametros del numero de pagina y se guardan en page_number
    # if en el request no hay parametro de pagina se usa el 1 por defecto
    page_number = request.GET.get('page', 1)
    # el metodo page devuelve el objeto con la informacion y la pagina que queriamos
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # si page_number no es un entero devuelve la primera pagina
        posts = paginator.page(1)
    except EmptyPage:
        # if page_number is out of range deliver last page of results
        # si page_number esta fuera de rango devuelve la ultima pagina como resultado
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


# def post_detail(request, id):
# esta es una manera de realizar la vista del detail
#     try:
#         post = Post.published.get(id=id)
#     except Post.DoesNotExist:
#         raise Http404("No Post found.")
#     return render(request,
#                   'blog/post/detail.html',
#                   {'post': post})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
