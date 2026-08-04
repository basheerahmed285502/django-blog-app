from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post

# Create your views here.


def home(request):
    posts = Post.objects.all().select_related("user").order_by("-published_date")

    paginator = Paginator(
        object_list=posts,
        per_page=4,
        orphans=2
    )

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "posts/index.html", {"page_obj": page_obj})


@login_required
def get_post(request, id):
    post = get_object_or_404(
        Post.objects.select_related('user').prefetch_related('comments__user'),
        id=id
    )

    return render(request, "posts/post.html", {"post": post})
