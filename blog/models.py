from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
            .filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)  # titulo da postagem
    slug = models.SlugField(max_length=250, unique_for_date='publish')  # o slug é usando compor urls mais elegantes
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')  # relacionamento many-to-one(muitos para um)= um autor, varias postagens
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)  # o datetime informa quando a postagem foi publicada, inclui o fuso horario
    created = models.DateTimeField(auto_now_add=True)  # informa quando foi criada e data salva automaticamente quando salvo
    updated = models.DateTimeField(auto_now=True)  # data será atualizada quando for salvo novamente
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')  # foi usado o parametro choice para definir os valores a ser usado
    objects = models.Manager()  # o gerenciador default
    published = PublishedManager()  # nosso gerenciador personalizado

    class Meta:
        ordering = ('-publish',)  # aqui dizemos ao django para que ordene os resultados com base no campo publish

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comentado por {self.name} no {self.post}'
