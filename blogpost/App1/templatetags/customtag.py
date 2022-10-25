from django import template
from App1.models import Post
from django.db.models import Count
register = template.Library()
@register.simple_tag
#total_posts is a default tag
def total_posts():
	return Post.objects.count()
	#return total number of posts

#to display latest posts, for inclusion tag we have to specify
# template file where data has to be returned
@register.inclusion_tag('App1/latest_post.html')
def latest_post(count=3):
	latest_posts=Post.objects.order_by('-publish')[:count]
	return {'latest_posts':latest_posts}

'''returning most commented post
to get all records according to ascending order of salaries 
we say Employee.objects.order_by('salary'),
now want to create a new column
Employee.objects.annotate(len_of_name=len(name)).order_by('salary')
'annotate' used to create a new column
'''
@register.simple_tag
def most_commented_post(count=3):
	return Post.objects.annotate(total_comments=Count('Comments')).order_by('-total_comments')[:count]
# total_comments is the new column created