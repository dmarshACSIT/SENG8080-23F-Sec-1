from django.db import models

# Create your models here.
class allAppData(models.Model):

    # model to save all app reated data from exect sheet

    web_scraper_order = models.CharField(max_length=200, null=True, blank=True)
    web_scraper_order_start_url = models.TextField(null=True, blank=True)
    app_link_txt = models.CharField(max_length=500, null=True, blank=True)
    app_link_href = models.TextField(null=True, blank=True)
    app_name = models.CharField(max_length=500, null=True, blank=True)
    app_category = models.CharField(max_length=200, null=True, blank=True)
    app_rating = models.CharField(max_length=200, null=True, blank=True)
    app_rating_count = models.CharField(max_length=200, null=True, blank=True)
    number_of_downloads = models.CharField(max_length=200, null=True, blank=True)
    developer_email = models.CharField(max_length=200, null=True, blank=True)
    last_update = models.CharField(max_length=200, null=True, blank=True)
    privacy_policy = models.CharField(max_length=500, null=True, blank=True)
    contains_ads = models.CharField(max_length=200, null=True, blank=True)
    in_app_purchase = models.CharField(max_length=200, null=True, blank=True)
    rated_for = models.CharField(max_length=200, null=True, blank=True)
    reviews = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.app_name
#from review_app.models import *
#kk = allAppData.objects.filter(app_name__regex = r'(:)') 
"""
for i in kk:
    i.app_name = i.app_name.replace(":", "_")
    i.save()
    
"""