# DRF
from rest_framework import serializers

# MODELS
from .models import *

# HELPERS
from .helpers import generate_id

class VideoSerializer(serializers.ModelSerializer):

    class Meta():
        model = Video
        fields = ('video_id', 'title', 'description', 'creator', 'video', 'video_banner')

    def create(self, validated_data):
        data = Video(
            video_id = generate_id(32),
            title = validated_data['title'],
            description = validated_data['description'],
            creator = validated_data['creator'],
            video = validated_data['video'],
            video_banner = validated_data['video_banner']
        )

        data.save()
        return data