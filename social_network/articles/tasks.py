from celery import shared_task
from djoser import signals
from djoser.serializers import UserCreateSerializer
from rest_framework import status
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response

from pyhunter import PyHunter
import clearbit

from articles.serializers import *

clearbit.key = 'sk_9e9630cc257d9cc80555aa866fef1663'

hunter = PyHunter('1983e7ca805c1cff4121b2cf7d8e990daf2c7d49')


@shared_task()
def create_user(request):
    try:
        email = request.data['email']
    except AttributeError:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'Email is required attribute'})

    if hunter.email_verifier(email)['webmail']:
        # response = clearbit.Enrichment.find(email=email, stream=True)
        # user = UserSerializer(data=response.person)
        user = UserCreateSerializer(data=request.data)

        if user.is_valid():
            user = user.save()
            signals.user_registered.send(sender="<class 'type'>", user=user, request=request)
            return Response({'status': status.HTTP_201_CREATED})

        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST})

    else:
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'You enter incorrect email'})


@shared_task()
def get_articles():
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response({'status': status.HTTP_200_OK, 'data': serializer.data})


@shared_task()
def create_article(request):
    article = ArticlesSerializer(data=request.data)

    if article.is_valid():
        article.save(user=request.user)
        return Response({'status': status.HTTP_201_CREATED})
    else:
        return Response({'status': status.HTTP_400_BAD_REQUEST})


@shared_task()
def like_article(request):
    article_id = request.data.get('article_id')
    article = get_object_or_404(Article, pk=article_id)
    action_type = request.data.get('type')
    if action_type == 'like':
        article.likers.add(request.user)

    elif action_type == 'unlike':
        article.likers.remove(request.user.id)

    return Response({'status': status.HTTP_200_OK})
