from rest_framework import serializers
from .models import User, Project, Contributor, Issue, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class ContributorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Contributor
        fields = ['id', 'project', 'user', 'permission', 'role']


class ContributorCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'project', 'user', 'permission', 'role']


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type']


class IssueDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    assignee = UserSerializer()

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'project', 'author', 'assignee']
        depth = 1


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'project', 'author', 'assignee']


class ProjectDetailSerializer(serializers.ModelSerializer):
    contributors = ContributorSerializer(source='contributor_set', many=True)
    issues = IssueSerializer(source='issue_set', many=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'issues', 'contributors']
        depth = 1


class IssueUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'assignee']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue']


class CommentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'description']


class CommentDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue', 'created_time']

