import string
import random
from django.http import HttpResponse

def generateLP(l=6):
    c=string.ascii_uppercase
    d=string.digits
    return ''.join(random.choice(d+c+d) for x in range(l))

LP=[generateLP() for i in range(500)]

def check(request):
    if 'l' in request.GET and request.GET['l']:
        chars=request.GET['l'].strip().upper()
        def f(x):
            return x.find(chars)==0
        message=str(filter(f,LP)).strip('[').strip(']')
        return HttpResponse(message)


