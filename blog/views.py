from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.http import HttpResponse


# Create your views here.

def post_list(request, category=None):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page,
                                                   'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


def post_add(request):
    print(request)
    import uuid
    user = User.objects.get(username='lion')
    for i in range(1, 10):
        pid = uuid.uuid4().hex
        post= Post(author=user, title='t' + pid, status='Published', body=pid * 10)
        post.save()

    response = HttpResponse()
    response.write(r'add 10 post')
    return response
