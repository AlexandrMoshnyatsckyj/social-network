from rest_framework import serializers

from articles.models import Article


class ArticleSerializer(serializers.ModelSerializer):

    """Post serialize"""

    class Meta:
        model = Article
        fields = ('id', 'user', 'header', 'content', 'likers', 'date')


class ArticlesSerializer(serializers.ModelSerializer):

    """Post serialize"""

    class Meta:
        model = Article
        fields = ('header', 'content', )
