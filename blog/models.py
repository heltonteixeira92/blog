from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)  # titulo da postagem
    slug = models.SlugField(max_length=250, unique_for_date='published')  # o slug é usando compor urls mais elegantes
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')  # relacionamento many-to-one(muitos para um)= um autor, varias postagens
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)  # o datetime informa quando a postagem foi publicada, inclui o fuso horario
    created = models.DateTimeField(auto_now_add=True)  # informa quando foi criada e data salva automaticamente quando salvo
    updated = models.DateTimeField(auto_now=True)  # data será atualizada quando for salvo novamente
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')  # foi usado o parametro choice para definir os valores a ser usado

    class Meta:
        ordering = ('-publish',)  # aqui dizemos ao django para que ordene os resultados com base no campo publish

    def __str__(self):
        return self.title
