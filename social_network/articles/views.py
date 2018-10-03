from rest_framework.views import APIView
from rest_framework import permissions

from articles.tasks import *


class Users(APIView):

    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        return create_user(request)


class Articles(APIView):

    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        return get_articles()

    def post(self, request):
        return create_article(request)


class ArticleLike(APIView):

    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        return like_article(request)
