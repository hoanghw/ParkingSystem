from parkingsystem import settings
from django.contrib.auth.models import User
from parker.models import Parker
import ldap
import requests
import xml.etree.ElementTree as ET

class SettingsBackend(object):
    def authenticate(self,ticket=None):
	r=requests.get('https://auth-test.berkeley.edu/cas/serviceValidate?service=http://23.23.166.34/checkticket/&ticket='+ticket)
        if r.content.find('Failure')<0:     
            tree=ET.fromstring(r.content)
            uid=tree[0][0].text
            l=ldap.initialize('ldap://ldap.berkeley.edu:389')
            r=l.search_s('ou=people,dc=berkeley,dc=edu',ldap.SCOPE_SUBTREE,'UID='+uid,['displayName','mail'])
            if 'displayName' in r[0][1] and r[0][1]['displayName']:
                username=r[0][1]['displayName'][0]
		email=''
            	if 'mail' in r[0][1] and r[0][1]['mail']:
                   email=r[0][1]['mail'][0]
	        try:
		   user=User.objects.get(username=username)
	   	except User.DoesNotExist:
		   user=User.objects.create(username=username,email=email,password='')
		   user.set_password(settings.ADMIN_PASSWORD)
		   user.save()
		   parker=Parker.objects.create(user=user,userId=uid)
		   parker.save()
            	return user
	    else: return None
	else:
            return None
 	    
    def get_user(self,user_id):
	try:
	    return User.objects.get(pk=user_id)
	except User.DoesNotExist:
	    return None
