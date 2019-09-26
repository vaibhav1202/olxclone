from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_img(upload): 
    ext = upload.name[-4:]
    if not ext in ['.jpg', ".png",'jpeg',".gif"]:
        raise ValidationError(u'File type is not supported!')    
    if upload.size > 1024*1024*2:
        raise ValidationError(u'File is too big!')    

# Create your models here.

class seller(models.Model):
    s_name=models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    s_pn=models.CharField(validators=[RegexValidator("^0?[6-9]{1}\d{9}$")]  ,max_length=20)
    s_email=models.EmailField()
    item_name=models.CharField(max_length=100)
    s_description=models.TextField()
    
    s_img=models.ImageField(upload_to = "images//", validators=[validate_img], null=True, blank=True)    
    s_price=models.IntegerField()
    s_years=models.DateTimeField(auto_now_add=True)
    s_area=models.CharField(max_length=100)
    