from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager

''' Post.objects.all returns all posts
Post.tags.all returns all tags which associated with Post
for tagging, need to third party application django-taggit
	 install pip install django-taggit

in settings.py add 'taggit' app in installed _apps
in models.py > post class add 'tags = TaggableManager()'
TaggableManager() is the class which takes care of 
tagging feature and need to impost the bellow, from taggit.managers import TaggableManager.
open py manage.py shell > from App1.models import Post
> post = Post.objects.get(id=4)
> post.title
> post.tags.add('SPB',singer','films')
> post.tags.all()
o/p <QuerySet [<Tag: SPB>, <Tag: singer>, <Tag: films>]> '''

'''taggit module contains a table 'Tag'. table Tag contains 2 attributes name and slug
url(r'^tag/(?P<tag_slug>[-\w]+)/$',views.post_list_view,name='postlisttagname')
tag_slug receives a slug ( films)
ex: http://127.0.0.1:8000/tag/poet/
tag is endpoint
'''



class CustomManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(status='published')
	'''class name.objects.all() returns all records from DB.
	we can filter the data based on our requirement. to do so we can use
	get_queryset(). parent class's get_queryset() is available in models.Manager
	and with help of filter() we can filter the record based on given condition.
	when objects is refered in views.py, internally it calls get_queryset().'''

class Post(models.Model):
	tags = TaggableManager()
	STATUS_CHOICE = (('draft','Draft'),('published','Published'))
	#STATUS_CHOICE refer to status of an article or blog, draft is for internal use and Draft for external
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=100, unique_for_date='publish')
	#slug field can be used in URLS, it short lable contaning alpha, num, underscores, hyphens. we can slug field to bulit human understandable and SEO friendly URLS
	author = models.ForeignKey(User,related_name = 'blog_post',on_delete=models.CASCADE)
	#on_delete=models.PROTECTED will forebide the deletion of reference object
	#User table is given by auth module
	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
	status = models.CharField(max_length=20,choices=STATUS_CHOICE, default='draft')
	objects = CustomManager()

	class Meta:
		ordering = ('-publish',) 
		#orders by ('publish') published date by ascending and ('-publish') orders by descending
	
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('postdetail',args=[self.publish.year,self.publish.strftime('%m'),self.publish.strftime('%d'), self.slug])

class Comments(models.Model):
	post = models.ForeignKey(Post,related_name="Comments",on_delete=models.CASCADE)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)
	
	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return 'commented by {0} on {1}'.format(self.email,self.post)
