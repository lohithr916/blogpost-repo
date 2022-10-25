from django.contrib import admin
from App1.models import Post,Comments
# Register your models here.
class PostAdmin(admin.ModelAdmin):
	ls = ['title','slug','author','body','publish','created','updated', 'status']
	prepopulated_fields = {'slug':['title']}
	#it will autofill the title in slug field by removing special chars except (-_) and 
	#it considers numbers, alphabets and it is SEO friendly
	list_filter = ['status','created','updated','publish','author']
	search_field = ['title','body']
	ordering = ['status','publish']
	raw_id_fields = ('author',)
	#it will represent given field in the form of id

class CommentAdmin(admin.ModelAdmin):
	ls = ['post','email','body','created','updated','active']
	list_filter = ['active','created','updated']
	search_field = ['post','email','body']

admin.site.register(Post,PostAdmin)
admin.site.register(Comments,CommentAdmin)