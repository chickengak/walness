from django.db import models

class Product(models.Model):
    modify_date = models.DateTimeField(null=True, blank=True)
    imgfile = models.ImageField(null=True, upload_to="image/", blank=True) # 이미지 컬럼 추가
