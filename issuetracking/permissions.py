from .models import Issue, Project, Contributor, Comment
from rest_framework.permissions import IsAuthenticated, BasePermission


class IsContributorPermission(BasePermission):
    message = 'Access not allowed ! Only contributors of the project can access'

    def has_object_permission(self, request, view, obj):
        in_project = Contributor.objects.filter(project=obj, user=request.user)
        return len(in_project) != 0


class IsAuthorProjectPermission(BasePermission):
    message = 'Access not allowed ! Only the author can access'

    def has_object_permission(self, request, view, obj):
        is_author = Contributor.objects.get(project=obj, user=request.user)
        return is_author.role == 'author'


class IsAuthorIssuePermission(BasePermission):
    message = 'Access not allowed ! Only the author can access'

    def has_object_permission(self, request, view, obj):
        is_author = Issue.objects.get(pk=obj.pk)
        return is_author.author == request.user


class IsAuthorCommentPermission(BasePermission):
    message = 'Access not allowed ! Only the author can access'

    def has_object_permission(self, request, view, obj):
        is_author = Comment.objects.get(pk=obj.pk)
        project = is_author.issue.project
        contributor = Contributor.objects.filter(project=project, user=request.user)
        return len(contributor) != 0 and is_author.author == request.user