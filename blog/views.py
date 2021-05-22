from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):  # a view post_list tem request como unico paramentro que é necessário em toda view
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})  # (objeto request, path do temple, variáveis de contexto)
    # usamos o atalho render para renderizar a lista de postagens com o template espeicificado.


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             published__year=year,
                             published__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
