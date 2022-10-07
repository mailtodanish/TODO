from rest_framework import serializers
from projects.models import Activity, TaskComment, ProjectTask, Favoutite_item
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

# Activity Serializer
'''
 Activity Creation for scheduled activity
 Activty Done button
'''


class FavouriteItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favoutite_item
        fields = '__all__'

        def create(self, validated_data):
            print(validated_data)


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('Title', 'Description', 'status', 'scheduled', 'pk',
                  'parentActivityId')
        read_only_fields = ['scheduled']

        def create(self, validated_data):
            '''
            Create ACtivity using Rest API
            '''
            act = Activity(Title=validated_data['Title'],
                           Description=validated_data['Description'],
                           Type=validated_data['Type'],
                           parentActivityId=validated_data['parentActivityId'])
            act.save()
            return act

        def update(self, instance, validated_data):
            # Update Activity Status using Rest API
            instance.title = validated_data['status']
            instance.save()


class TaskCommentSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = TaskComment
        fields = ('pk', 'content', 'updated', 'tags', 'task', 'created')


# Task Serializer
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = '__all__'
