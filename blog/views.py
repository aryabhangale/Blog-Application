from django.shortcuts import render
from	django.core.paginator	import	Paginator,	EmptyPage, PageNotAnInteger
from	django.views.generic	import	ListView
from	django.core.mail	import	send_mail

# Create your views here.
from	django.shortcuts	import	render,	get_object_or_404
from	.models	import	Post, Comment
from	.forms	import	EmailPostForm, CommentForm

def contact(request):
    return	render(request,'blog/post/contact.html')

class	PostListView(ListView):
	queryset	=	Post.published.all()
	context_object_name	=	'posts'
	paginate_by	=	3
	template_name	=	'blog/post/list.html'

def	post_list(request):
	object_list	=	Post.published.all()
	paginator	=	Paginator(object_list,	5)	#	5	posts	in	each	page
	page	=	request.GET.get('page')
	try:
			posts	=	paginator.page(page)
	except	PageNotAnInteger:
	#	If	page	is	not	an	integer	deliver	the	first	page
			posts	=	paginator.page(1)
	except	EmptyPage:
	#	If	page	is	out	of	range	deliver	last	page	of	results
	    posts	=	paginator.page(paginator.num_pages)

	return	render(request,'blog/post/list.html',{'posts':	posts})
def	post_detail(request,	year,	month,	day,	post):
    post	=	get_object_or_404(Post,	slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    comments	=	post.comments.filter(active=True)
    new_comment	=	None
    if	request.method	==	'POST':
        comment_form	=	CommentForm(data=request.POST)
        if	comment_form.is_valid():								
            new_comment	=	comment_form.save(commit=False)
            new_comment.post	=	post
            new_comment.save()
    else:
        comment_form	=	CommentForm()
    return	render(request,'blog/post/detail.html',{'post':	post,'comments':comments,'new_comment':new_comment,'comment_form':comment_form})

def	post_share(request,	post_id):
    sent=False
    post	=	get_object_or_404(Post,	id=post_id,	status='published')
    form	=	EmailPostForm(request.POST)
    if	request.method	==	'POST':
        if	form.is_valid():
            cd	=	form.cleaned_data
            post_url	=	request.build_absolute_uri(post.get_absolute_url())
            subject	=	'{}	({})	recommends	you	reading	"{}"'.format(cd['name'],	cd['email'],	post.title)
            message	=	'Read	"{}"	at	{}\n\n{}\'s	comments:	{}'.format(post.title,	post_url,	cd['name'],	cd['comments'])
            send_mail(subject,	message,	'aryabhangale72@gmail.com',[cd['to']])
            sent	=	True
        else:
            form	=	EmailPostForm()
    return	render(request,	'blog/post/share.html',	{'post':post,'form':form,'sent':sent})