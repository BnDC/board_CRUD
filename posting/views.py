import json
from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.views import View

from user.models import User
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
    
    def get(self, request, posting_id = None):
        if posting_id == None:
            return JsonResponse({"message" : "NEED_POSTING_ID"}, status = 400)
        
        posting_queryset = Posting.objects.filter(id = posting_id)
        posting          = posting_queryset.first()

        if not posting_queryset.exists() or posting.deleted_at != None:
            return JsonResponse({"message" : "DOES_NOT_EXIST"}, status = 400)
        
        result = {
            "id"         : posting.id,
            "title"      : posting.title,
            "content"    : posting.content,
            "created_at" : posting.created_at,
            "updated_at" : posting.updated_at,
        }

        return JsonResponse({"result" : result}, status = 200)

    @login_required
    def patch(self, request, posting_id = None):
        if posting_id == None:
            return JsonResponse({"message" : "NEED_POSTING_ID"}, status = 400)

        try:
            data    = json.loads(request.body)
            user    = request.user
            posting_queryset = Posting.objects.filter(id = posting_id)
            posting = posting_queryset.first()

        except JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status = 400)

        if not posting_queryset.exists() or posting.deleted_at != None:
            return JsonResponse({"message" : "DOES_NOT_EXIST"}, status = 400)

        if posting.user_id != user.id:
            return JsonResponse({"message" : "FORBIDDEN"}, status = 403)

        posting.__dict__.update(data)
        posting.save()

        return JsonResponse({"message" : "UPDATED"}, status = 200)