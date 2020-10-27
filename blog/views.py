from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
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

@login_required
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

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

# Функция публикации черновых постов

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


# Функция удаления постов
@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})



@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)