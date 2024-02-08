from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

# 作ってあるmodelsのクラス全て持ってくる
from Post_app.models import *

from Post_app.forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from User_app.models import *
from django.core.paginator import Paginator
from django.db.models import Q
from comment_app.models import *
from comment_app.forms import *
# Create your views here.
@login_required
def home(request):
    user = request.user
    user = request.user
    all_users = User.objects.all()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

    profile = Profile.objects.all()

    posts = Stream.objects.filter(user=user)
    group_ids = []

    
    for post in posts:
        group_ids.append(post.post_id)
        
    post_items = Post.objects.all().order_by('-posted')

    query = request.GET.get('q')
    if query:
        users = User.objects.filter(Q(username__icontains=query))

        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)


    context = {
        'post_items': post_items,
        'follow_status': follow_status,
        'profile': profile,
        'all_users': all_users,
        # 'users_paginator': users_paginator,
    }
    return render(request, 'main/home.html', context)


@login_required
# カテゴリ一覧
def category_list(rq):
    # カテゴリmodelの をすべて　categoriesに入れる
    categories=Category.objects.all()
    # modelsから持ってきたカテゴリを辞書に入れる
    context={
        'categories':categories
    }
    # render でカテゴリ一覧をcontextからcategory.htmlに表示する
    return render(rq,'category/category.html',context)

@login_required
def category_Post_list(rq,cid):
    category=Category.objects.get(cid=cid)
    posts = Post.objects.filter(status=True, category=category)

    context={
        'category':category,
        'posts':posts
    }
    return render(rq,'category/category-post-list.html',context)



@login_required
def NewPost(request):
    user = request.user
    tags_obj = []
    
    if request.method == "POST":
        form = NewPostform(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tag_form = form.cleaned_data.get('tags')
            tag_list = list(tag_form.split(','))

            for tag in tag_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user=user)
            p.tags.set(tags_obj)
            p.save()
            return redirect('home')
    else:
        form = NewPostform()
    context = {
        'form': form
    }
    return render(request, 'Post/newpost.html', context)


@login_required
def PostDetail(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-date')

    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            return HttpResponseRedirect(reverse('post-details', args=[post.id]))
    else:
        form = NewCommentForm()

    context = {
        'post': post,
        'form': form,
        'comments': comments
    }


    return render(request, 'Post/postdetail.html', context)


@login_required
def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
        
    post.likes = current_likes
    post.save()
    # return HttpResponseRedirect(reverse('post-details', args=[post_id]))
    return HttpResponseRedirect(reverse('post-details', args=[post_id]))


@login_required
def favourite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    profile = Profile.objects.get(user=user)

    if profile.favourite.filter(id=post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return HttpResponseRedirect(reverse('post-details', args=[post_id]))

