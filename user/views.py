import json
from json.decoder import JSONDecodeError
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

        User.objects.create(
            email    = email,
            nickname = nickname,
            password = hashed_password,
        )

        return JsonResponse({'message': 'SUCCESS'}, status=201)

class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            user = User.objects.get(email = email)

            if not (user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))):
                return JsonResponse({"message" : "INVALID_USER"}, status = 401)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({"message" : "DOES_NOT_EXIST"}, status = 401)

        encoded_jwt = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm = 'HS256')

        return JsonResponse({'access_token' : encoded_jwt}, status = 201) 