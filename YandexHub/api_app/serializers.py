# DRF
from rest_framework import serializers

# MODELS
from site_app.models import Article, Video

# HELPERS
from site_app.helpers import generate_id


# video serializer
class VideoSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Video
        fields = (
            'video_id',
            'title',
            'description',
            'creator',
            'video',
            'video_banner'
        )

    def create(self, validated_data):
        data = Video(
            video_id=generate_id(32),
            title=validated_data['title'],
            description=validated_data['description'],
            creator=validated_data['creator'],
            video=validated_data['video'],
            video_banner=validated_data['video_banner']
        )

        data.save()
        return data


# article serializer
class ArticleSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = Article
        fields = ('article_id', 'text', 'creator')

    def create(self, validated_data):
        data = Article(
            article_id=generate_id(32),
            text=validated_data['text'],
            creator=validated_data['creator'],
        )

        data.save()
        return data
