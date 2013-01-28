from django.conf import settings
#from whauth.models import User
from django.contrib.auth import authenticate as djauth
from django.contrib.auth import login as djlogin

class AuthBackend:
    
    def get_fbid(self,token):
        if token is not None:
            import urllib2
            import simplejson
            req = urllib2.Request("https://graph.facebook.com/me?access_token="+token)
            opener = urllib2.build_opener()
            try:    
                res = opener.open(req)
            except:  
                #a bad request was made,facebook said our access token was shit
                return None

            js = simplejson.load(res)
            fbid = js.get('id')

            return fbid

    def authenticate(self, username=None, password=None, token=None):
        from whauth.models import User
        if token is not None: #login wif da facebook
            fbid = self.get_fbid(token)

            if fbid is None:
               return None

            try:    
                user = User.objects.get(fbid=fbid) 
            except:
                return None

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            return user
        
        #if token ain't provided, login normally.
        try:
            user = User.objects.get(username=username)
        except:
            return None

        if not user.check_password(password):
            return None

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        return user
   
    def get_user(self, user_id):
        from whauth.models import User
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

        
