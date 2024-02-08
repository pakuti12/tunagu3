from Post_app.models import *
from django.db.models import Max,Min
def default(rq):
    categories=Category.objects.all()

    
    return{
        'categories':categories,
    }