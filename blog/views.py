from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from forms import EmailPostForm
from django.core.mail import send_mail


def post_list(request):  # a view post_list tem request como unico paramentro que é necessário em toda view
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # três postagens em cada página
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Se a página não for um inteiro, exibe a primeira página
        posts = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo,
        # exibe a ultima página de resultados
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,'posts': posts})  # (objeto request, path do temple, variáveis de contexto)
    # usamos o atalho render para renderizar a lista de postagens com o template especificado.


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # obtém a postagem com base no id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Formulario foi submetido
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Campos de formulário passaram pela validação
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@myblog.com',
                      [cd['to']])
            sent = True
        else:
            form = EmailPostForm()
        return render(request, 'blog/post/share.html', {'post': post,
                                                        'form': form,
                                                        'sent': sent})
