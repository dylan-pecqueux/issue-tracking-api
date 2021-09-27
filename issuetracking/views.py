from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from .serializers import UserSerializer, ProjectSerializer, ContributorSerializer, IssueSerializer, ProjectDetailSerializer
from .models import Issue, Project, Contributor
from .permissions import IsContributorPermission, IsAuthorPermission


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProjectDetailView(viewsets.ViewSet):
    queryset = Project.objects.all()

    def create(self, request):
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_project = serializer.save()
        new_project.contributor_set.create(permission='R', role='author', user=request.user)
        return Response(serializer.data)

    def list(self, request):
        serializer = ProjectSerializer(self.queryset, many=True)
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
            permission_classes = [IsAuthenticated, IsContributorPermission, IsAuthorPermission]
        return [permission() for permission in permission_classes]
        

class IssueView(APIView):

    permission_classes = [IsAuthenticated, IsContributorPermission]

    def post(self, request, pk):
        obj = Project.objects.get(pk=pk)
        self.check_object_permissions(self.request, obj)
        request.data['project'] = obj.pk
        request.data['author'] = request.user.pk
        request.data['assignee'] = request.user.pk
        serializer = IssueSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project=obj)
        return Response(serializer.data)
    
    def get(self, request, pk):
        obj = Project.objects.get(pk=pk)
        self.check_object_permissions(self.request, obj)
        issues = Issue.objects.filter(project=pk)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)
