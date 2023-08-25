from django.shortcuts import render
from .models import Post
# Create your views here.
def blog(request):
    posts = Post.objects.order_by('-date_publi')[:5]
    context = {
        'posts': posts
    } 
    return render(request, 'tibiameta/blog.html', context)

def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    context = {
        'post': post
    }
    print(context)
    return render(request, 'tibiameta/post_detail.html', context)

# def blog(request):
#     posts = Post.objects.order_by('-date_publi')[:5]
#     context = {
#         'posts': posts      
#     }
#     print(context)
#     return render(request,'blog/blog.html', context)