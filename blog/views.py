from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required



def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


# Открывем выбранный пост на отдельной странице по ссылке на его заголовке
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


# Публикуем новый пост через форму

@login_required
def post_new(request):
    if request.method == "POST":
    # т.е. request.POST
    # в post_edit.html the tag <form> has method="POST"
        form = PostForm(request.POST)
        # print(form)
        # строим PostForm с данными формами и передаем в переменную form
        if form.is_valid():
            # проверяем валидность данных и сохраняем в БД
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            # комментируем для схранения постов как черновик
            post.save()
            return redirect('post_detail', pk=post.pk)
            # Переходим на страницу просмотра поста
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    print(post)
    # в переменную post передаем запись из модели Post с заданным pk
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        # requestPOST это словарь где ключи - названия полей, значения - их содержимое
        # print(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            # комментируем для схранения постов как черновик
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


# Функция просмотра списка  черновых постов

def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

# Функция публикации черновых постов

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


# Функция удаления постов
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')