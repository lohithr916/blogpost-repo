from django.shortcuts import render,get_object_or_404
from App1.models import Post,Comments
from django.urls import reverse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from App1.forms import EmailForm,CommentForm
from django.core.mail import send_mail
from taggit.managers import TaggableManager
from taggit.models import Tag
'''Pagination
if more number of post are available then it is recomended to be paginated. django Paginator module available in django.core.paginator 
pagination steps: 1.create paginator object with list of records and number of records per page, 
paginator = Paginator(post_list,3)

2.get list of records related to current page, 
page_number=request.GET.get('page')
post_list=paginator.page(page_number)
page(page_number) return list of recors in page_number where page_number carries current page number 
3.if page_number is not an integer ie no page number is passed then consider first page,
post_list=paginator.page(1)
4.if parameter is greater than last page number then consider the last page
post_list=paginator.page(paginator.num_pages)'''

def post_list_view(request,tag_slug=None):
	post_list = Post.objects.all()
	tag=None
	if tag_slug:
		tag=get_object_or_404(Tag,slug=tag_slug)
		post_list=post_list.filter(tags__in=[tag])
	paginator=Paginator(post_list,2)
	page_number=request.GET.get('page')
	try:
		post_list=paginator.page(page_number)
	except PageNotAnInteger:
		post_list=paginator.page(1)
	except EmptyPage:
		post_list=paginator.page(paginator.num_pages)
	d = {'post_list':post_list,'tag':tag}
	return render(request,'App1/post_list.html',d)
'''tag_slug is None by default and will be received from url
if tag_slug is received from url then variable tag will
collect all the tags which is present in table Tag which matches
then post_list will collect all posts and filters according to tags
'''
def post_detail_view(request,year,month,day,post):
	post=get_object_or_404(Post,slug=post,publish__year=year,publish__month=month,publish__day=day)
	'''get_object_or_404() is used to fetch the current record if record is nor available then it returns 404 error
	it accepts class name as first parameter and args are assigned to field of class.
	in url pattern last regular expression pattern ie (?P<post>[\w]+) is refer to slug field of perticular post which is matched 
	using 1 or more word pattern'''
	comments = post.Comments.filter(active=True)
	comment_submitted = False
	form = CommentForm()
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.post = post
			new_comment.save()
			comment_submitted = True
	d={'post':post,'form':form,'comment_submitted':comment_submitted,'comments':comments}
	return render(request,'App1/post_detail.html',d)

'''https://www.google.com/search?rlz=value
domin/search?query="resource"
query = key
resource = value
request.GET.get("query","Not found")
o/p is resource if requested page ia available else Not found
GET boject to retrieve get method'''

'''Email utility in Django
from django.core.mail import send_mail--21:50 min

send_mail("This is to check SMTP working","EOM","lohith.rangaraj@smartbear.com",
["lohithrangaraju@gmail.com","lohithrangaraj916@gmail.com"],fail_silently=True)
'''
'''
if form.is_valid():
	new_comment = form.save(commit=False) # accept end user comment but don't save
	new_comment.post = post # associate corresponding post value
	new_comment.save() save, new comment is associted with post
	comment_submitted = true 
'''
def mail_view(request,id):
	post = get_object_or_404(Post,id=id,status='published')
	form = EmailForm()
	if request.method == 'POST':
		form = EmailForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = '{0}{1} suggest you to read {2}'.format(data['name'],data['fromemail'],post.title)
			message = 'Read post at \n {0} \n {1} comments\n {2}'.format(post_url,data['name'],data['comments'])
			send_mail(subject,message,'lohithrangaraj916@gmail.com',[data['toemail']])
	d = {'post':post,'form':form}
	return render(request,'App1/sharebymail.html',d)

''' absolute uri is full path of the resource and url is a part of uri
HttpRequest.build_absolute_uri(location=None)
request.build_absolute_uri(post.get_absolute_url())
returns the absolute uri form of location, if no location
is provided then location will be set to request.get_full_path()

>>>request.build_absolute_uri()
'https://example.com/music/bands/the_beatles?print=true'
>>>request.build_absolute_uri('/bands/')
'https://example.com/music/bands/'
>>>request.build_absolute_uri('https://example.com/bands/')
'https://example.com/music/bands/'
'''

'''
there are 3 utilities available to define custom template tags
1. simple tags: performs some processing and return a string
2. inclusion tags:same as 1 and renders template
3. assignment tags: same as 1 and assign result to variable in context

creating custom template tags: inside application folder create folder named with 'templatetags',
create a blank file __init__.py
create python file inside templatetags, here we define our own template tags

'''