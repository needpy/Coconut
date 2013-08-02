import datetime
import urllib.parse, hashlib

from django.db import models
from django.core.urlresolvers import reverse

def _author_gravatar_url(self):
    if self.author_email:
        email=self.author_email.encode('utf-8')
        gravatar_url="http://www.gravatar.com/avatar/"+\
            hashlib.md5(email.lower()).hexdigest()

        return gravatar_url

    else:
        return '/static/blog/anonymous_gravatar.jpg'


class Setting(models.Model):

    blog_name=models.CharField(max_length=64)
    #site_url=models.URLField()
    # The number of articles which will be displayed on homepage.
    showed_article_num=models.IntegerField(default=7)
    # The number of page views of the whole blog.
    views=models.IntegerField(default=0)

    def __unicdoe__(self):
        return 'Blog Settings' 
    
    def __str__(self):
        return 'Blog Settings'


class Article(models.Model):
    title=models.CharField(max_length=128)
    content=models.TextField()
    pub_time=models.DateTimeField(default=datetime.datetime.now())
    published=models.BooleanField()
    # The number of page views of this article.
    views=models.IntegerField(default=0)
    
    tags=models.ManyToManyField('Tag',null=True,blank=True)
    category=models.ForeignKey('Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    
    """ 
    If has_aside is true, the article will be displayed with an aside,
    which includes tag list and category list, on the right side.
    If you want to place some big images in the article, you should condsider
    setting has_aside to false to have a more open space.
    """
    has_aside=models.BooleanField(default=True)
    
    """ 
    This method return summary of an article. The summary of an article means
    part of content before "<!--more-->" tag in this article.
    """
    def summary(self):
        end_index=self.content.find('<!--more-->')
        if end_index==-1:
            return None 
        else:
            return self.content[:end_index]
   

    def get_absolute_url(self):
        return reverse('article',args=[self.pk])

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class Tag(models.Model):
    name=models.CharField(max_length=64,unique=True)

    def published_article_num(self):
        num=0
        for article in Article.objects.filter(tags=self):
            if article.published:
                num+=1
        return num

    
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Category(models.Model):
    name=models.CharField(max_length=64,unique=True)
    
    def published_article_num(self):
        num=0
        for article in Article.objects.filter(category=self):
            if article.published:
                num+=1
        return num
        
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class ArticleComment(models.Model):
    author=models.CharField(max_length=64,blank=True,null=True)
    author_email=models.EmailField(blank=True,null=True)
    author_url=models.URLField(blank=True,null=True)
    content=models.TextField()
    pub_time=models.DateTimeField(default=datetime.datetime.now())

    article=models.ForeignKey(Article)

    author_gravatar_url=_author_gravatar_url


    def __unicode__(self):
        return self.author

    def __str__(self):
        return self.author


class Page(models.Model):
    title=models.CharField(max_length=128)
    content=models.TextField()
    pub_time=models.DateTimeField(default=datetime.datetime.now())
    published=models.BooleanField()

    """ 
    page_order determines which page should be displayed on the front in
    the blog navigation block. The page which has smaller page_order will 
    be displayed in front of others in the blog navigation block.
    """
    page_order=models.IntegerField(unique=True)
    # The number of page views of this page.
    views=models.IntegerField(default=0)

    """
    If has_aside is true, the page will be displayed with an aside,
    which includes tag list and category list, on the right side.
    If you want to place some big images in the page, you should condsider
    setting has_aside to false to have a more open space.
    """
    has_aside=models.BooleanField(default=True)
    
    def get_absolute_url(self):
        return reverse('page',args=[self.pk])

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

class PageComment(models.Model):
    author=models.CharField(max_length=64,blank=True)
    author_email=models.EmailField(blank=True)
    author_url=models.URLField(blank=True)
    content=models.TextField()
    pub_time=models.DateTimeField(default=datetime.datetime.now())

    page=models.ForeignKey(Page)
    
    author_gravatar_url=_author_gravatar_url
    

    def __unicode__(self):
        return self.author

    def __str__(self):
        return self.author

