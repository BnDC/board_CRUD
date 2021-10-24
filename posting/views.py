import json

from django.http import JsonResponse
from django.views import View

from posting.models import Posting
from core.views import login_required

class PostingView(View):
    @login_required
    def post(self, request):
        try:
            data    = json.loads(request.body)
            title   = data['title']        
            content = data['content']        
            user    = request.user

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

        Posting.objects.create(
            title   = title,
            content = content,
            user_id = user.id,
        )

        return JsonResponse({"message" : "CREATED"}, status = 201)
    
    @login_required
    def get(self, request):
        postings = Posting.objects.all()

        result = [{
            "id" : posting.id,
            "title" : posting.title,
        } for posting in postings]

        return JsonResponse({"result" : result}, status = 200)
