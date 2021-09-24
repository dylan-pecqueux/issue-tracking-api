from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework import generics
from .serializers import UserSerializer, ProjectSerializer, ContributorSerializer, IssueSerializer
from .models import Issue, Project, Contributor


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProjectView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_project = serializer.save()
        new_project.contributor_set.create(permission='R', role='author', user=request.user)
        return Response(serializer.data)

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


class IssuePermission(BasePermission):
    message = 'Access not allowed ! Only contributors of the project can access'

    def has_object_permission(self, request, view, obj):
        in_project = Contributor.objects.filter(project=obj, user=request.user)
        return len(in_project) != 0
        

class IssueView(APIView):

    permission_classes = [IsAuthenticated, IssuePermission]

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
