from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.shortcuts import render,get_object_or_404
from django.views.decorators.http import require_POST
from blog.models import Post
from django.views.generic import ListView
from .forms import EmailPostForm,CommentForm

# Create your views here.
# def post_list(request):
#     post_list = Post.published.all()
#     paginator = Paginator(post_list,3)
#     page_number = request.GET.get('page',1)
#     posts = paginator.get_page(page_number)
#     return render(request, 'blog/post/list.html', {'posts': posts})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_detail(request,year,month,day,post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year = year,
        publish__month = month,
        publish__day = day
        )
    
    return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request,post_id):
    post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)

    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # send email...
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{cd['name']} ({cd['email']})"
                f"recommends you to read {post.title}"
                )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']} included the following comment: {cd['comments']}"
            )

            send_mail(
                subject = subject,
                message = message,
                from_email = None,
                recipient_list= [cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(request,'blog/post/share.html',{
        'post':post,
        'form': form,
        'sent': sent
    })
        
@require_POST
def post_comment(request,post_id):
    post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request,'blog/post/comment.html',{'post':post,'form':form,'comment':comment})