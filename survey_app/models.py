from django.db import models
from .choices import *

class News_article (models.Model):

    aid = models.CharField(max_length=512, null=True)
    original_title = models.CharField(max_length=512, blank=True, null=True)
    image_url = models.URLField()
    date = models.DateField(blank=True, null=True) 
    article_url = models.URLField()
    category = models.CharField(max_length=512, blank=True, null=True)
    text = models.CharField(max_length=100000)   
    style = models.CharField(max_length=512, blank=True, null=True)
    manipulated_title= models.CharField(max_length=512, blank=True, null=True)
    title = models.CharField(max_length=512, blank=True, null=True) #manipulated_boring_title


    def __str__(self):
        return self.title



class Personal_info(models.Model):
    id = models.AutoField(primary_key=True)
    session_id = models.CharField(max_length=100, blank=False, default=None)
    name = models.CharField(max_length=50, blank=False, default=None, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    headline_style = models.CharField(max_length=200, blank=False, null=True)
    manipulated_headlines = models.TextField(default='{}')
    selected_articles_list = models.CharField(max_length=300, blank=False, null=True, default=None)
    score = models.IntegerField(default=0)
    
    #################### pre-questionnaire items ####################
    
    preferred_headline = models.CharField(
        max_length=200,
        choices=headline_choices,
        verbose_name='preferred_headline',
        default=None,
        blank=False
    )
    
    preferred_headline2 = models.CharField(
        max_length=200,
        choices=headline_choices2,
        verbose_name='preferred_headline2',
        default=None,
        blank=False
    )

    preferred_headline3 = models.CharField(
        max_length=200,
        choices=headline_choices3,
        verbose_name='preferred_headline3',
        default=None,
        blank=False
    )


    class Meta:
        verbose_name = 'personal_info'
        ordering = ['id']
        db_table = 'personal_info'

    def __str__(self):
        return "{}".format(self.id)
    
    
    
    
