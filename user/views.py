import json
import bcrypt
import jwt
import re

from django.http import JsonResponse
from django.views import View

from user.models import User
from django.conf.global_settings import SECRET_KEY

class SignUpView(View):
    def post(self, request):

        REGX_EMAIL    = '^[\w]+@[\w.\-]+\.[A-Za-z]{2,3}$'
        REGX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[~!@#$^&*()+|=])[A-Za-z\d~!@#$%^&*()+|=]{8,20}$'
        
        try:
            data     = json.loads(request.body)
            email    = data['email']
            nickname = data['nickname']
            password = data['password']

            if User.objects.filter(email = email).exists():
                return JsonResponse({'message': 'EXIST_EMAIL'}, status=400)

            if not re.match(REGX_EMAIL, email):
                return JsonResponse({'message': 'INVALID_EMAIL_FORM'}, status=400)

            if not re.match(REGX_PASSWORD, password):
                return JsonResponse({'message': 'INVALID_PASSWORD_FORM'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        
        User.objects.create(
            email    = email,
            nickname = nickname,
            password = hashed_password,
        )

        return JsonResponse({'message': 'SUCCESS'}, status=201)