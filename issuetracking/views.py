from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Issue, Project, Contributor, Comment
from .serializers import (
    UserSerializer, 
    ProjectSerializer, 
    ContributorSerializer,
    ContributorCreateSerializer,
    IssueSerializer, 
    ProjectDetailSerializer, 
    IssueDetailSerializer, 
    IssueUpdateSerializer,
    CommentSerializer,
    CommentDetailSerializer,
    CommentUpdateSerializer
    )
from .permissions import (
    IsContributorPermission,
    IsAuthorProjectPermission,
    IsAuthorIssuePermission,
    IsAuthorCommentPermission
    )


class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        request.user.is_active = False
        request.user.delete()
        return Response(status=204)


class ProjectView(viewsets.ViewSet):

    queryset = Project.objects.all()

    def create(self, request):
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_project = serializer.save()
        new_project.contributor_set.create(permission='R', role='author', user=request.user)
        return Response(serializer.data)

    def list(self, request):
        user_projects = self.queryset.filter(contributor__user=request.user)
        serializer = ProjectSerializer(user_projects, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        project = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(self.request, project)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    def update(self, request, pk=None):
        project = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(self.request, project)
        serializer = ProjectSerializer(project, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        project = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(self.request, project)
        project.delete()
        return Response(status=204)

    def get_permissions(self):
        if self.action == 'create' or self.action == 'list':
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsContributorPermission]
        else:
            permission_classes = [IsAuthenticated, IsContributorPermission, IsAuthorProjectPermission]
        return [permission() for permission in permission_classes]


class IssueView(viewsets.ViewSet):

    queryset = Issue.objects.all()

    def create(self, request, project_id):
        project = self.get_queryset()
        self.check_object_permissions(self.request, project)
        request.data['project'] = project.pk
        request.data['author'] = request.user.pk
        if 'assignee' not in request.data:
            request.data['assignee'] = request.user.pk
        serializer = IssueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def list(self, request, project_id):
        obj = self.get_queryset()
        self.check_object_permissions(self.request, obj)
        issues = Issue.objects.filter(project=project_id)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)

    def retrieve(self, request, project_id, pk=None):
        issue = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(self.request, self.get_queryset())
        serializer = IssueDetailSerializer(issue)
        return Response(serializer.data)

    def update(self, request, project_id, pk=None):
        issue = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(self.request, issue)
        if 'assignee' not in request.data:
            request.data['assignee'] = request.user.pk
        serializer = IssueUpdateSerializer(issue, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, project_id, pk=None):
        issue = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(self.request, issue)
        issue.delete()
        return Response(status=204)

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return get_object_or_404(id=project_id)

    def get_permissions(self):
        if self.action == 'create' or self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsContributorPermission]
        else:
            permission_classes = [IsAuthenticated, IsAuthorIssuePermission]
        return [permission() for permission in permission_classes]


class ContributorView(viewsets.ViewSet):

    queryset = Contributor.objects.all()

    def create(self, request, project_id):
        project = self.get_queryset()
        self.check_object_permissions(self.request, project)
        request.data['project'] = project.id
        serializer = ContributorCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request, project_id):
        self.check_object_permissions(self.request, self.get_queryset())
        contributors = self.get_queryset().contributor_set
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data)

    def destroy(self, request, project_id, pk=None):
        contributor = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(self.request, self.get_queryset())
        contributor.delete()
        return Response(status=204)

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return get_object_or_404(Project, id=project_id)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated, IsContributorPermission]
        else:
            permission_classes = [IsAuthenticated, IsContributorPermission, IsAuthorProjectPermission]
        return [permission() for permission in permission_classes]


class CommentView(viewsets.ViewSet):

    queryset = Comment.objects.all()

    def create(self, request, project_id, issue_id):
        self.check_object_permissions(self.request, project_id)
        request.data['author'] = request.user.pk
        request.data['issue'] = issue_id
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def retrieve(self, request, project_id, issue_id, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(self.request, project_id)
        serializer = CommentDetailSerializer(comment)
        return Response(serializer.data)

    def list(self, request, project_id, issue_id):
        comments = self.get_queryset().comment_set
        self.check_object_permissions(self.request, project_id)
        serializer = CommentDetailSerializer(comments, many=True)
        return Response(serializer.data)

    def update(self, request, project_id, issue_id, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(self.request, comment)
        serializer = CommentUpdateSerializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, project_id, issue_id, pk=None):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(self.request, comment)
        comment.delete()
        return Response(status=204)

    def get_queryset(self):
        issue_id = self.kwargs['issue_id']
        return get_object_or_404(Issue, id=issue_id)

    def get_permissions(self):
        if self.action == 'list' or self.action == 'create' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsContributorPermission]
        else:
            permission_classes = [IsAuthenticated, IsAuthorCommentPermission]
        return [permission() for permission in permission_classes]
