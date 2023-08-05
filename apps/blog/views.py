from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Post
from django.core.paginator import Paginator


class BlogView(View):
    template_name = 'blog/blog.html'

    def get(self, request, *args, **kwargs):
        posts = Post.objects.filter(is_active=True).order_by('-publish_date')
        paginator = Paginator(posts, 15)
        page_number = request.GET.get('page')
        page_objects = paginator.get_page(page_number)
        return render(request, self.template_name, {'posts': page_objects})


class PostView(View):
    template_name = 'blog/post.html'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=kwargs.get('id'))
        return render(request, self.template_name, {'post': post})


class LatestPostsPartial(View):
    template_name = 'includes/latest_posts.html'


    def get(self, request):
        latest_posts = Post.objects.order_by('-publish_date')[:10]
        return render(request, self.template_name, {'latest_posts': latest_posts, 'slider_titile': 'محصولات جدید', 'type': 'new',})
