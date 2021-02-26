"""View module for handling requests about tasks"""
from django.db.models import query
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from datetime import date
from todoapi.models import Task, MyUser


class Tasks(ViewSet):

    def create(self, request):
        """Handle POST operations for tasks

        Returns:
            Response -- JSON serialized task instance
        """
        current_user = MyUser.objects.get(user=request.auth.user)

        # Grab required data from client to build a new task instance
        task = Task()
        task.user = current_user
        task.title = request.data["title"]
        task.content = request.data["content"]
        task.creation_date = date.today()
        task.is_complete = False

        try:
            task.save()
            serializer = TaskSerializer(task, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        """Handle PATCH requests for a task

        Returns:
            Response -- Empty body with 204 status code
        """

        # Allow user to PATCH is_complete field
        task = Task.objects.get(pk=pk)
        task.is_complete = request.data["is_complete"]
        task.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        """Handle PUT requests for a task

        Returns:
            Response -- Empty body with 204 status code
        """
        current_user = MyUser.objects.get(user=request.auth.user)

        task = Task.objects.get(pk=pk)
        task.user = current_user
        task.title = request.data["title"]
        task.content = request.data["content"]
        task.creation_date = request.data["creation_date"]
        task.is_complete = request.data["is_complete"]

        task.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            task = Task.objects.get(pk=pk)
            task.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Task.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single task

        Returns:
            Response -- JSON serialized task
        """
        try:
            task = Task.objects.get(pk=pk)
            serializer = TaskSerializer(
                task, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to get all tasks

        Returns:
            Response -- JSON serialized list of all tasks
        """

        # Get all task records from database
        all_tasks = Task.objects.all()

        # Get current logged in user
        current_user = MyUser.objects.get(user=request.auth.user)

        # Get all tasks associated to the current_user
        all_tasks = all_tasks.filter(user=current_user)

        # Note the addtional `many=True` argument to the
        # serializer. It's needed when you are serializing
        # a list of objects instead of a single object.
        serializer = TaskSerializer(
            all_tasks, many=True, context={'request': request})
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for default Django Users

    Arguments:
        serializers
    """

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')
        depth = 1


class MyUserSerializer(serializers.ModelSerializer):
    """JSON serializer for tasks

    Arguments:
        serializers
    """

    user = UserSerializer(many=False)

    class Meta:
        model = MyUser
        fields = ('id', 'user')
        depth = 1


class TaskSerializer(serializers.ModelSerializer):
    """JSON serializer for Tasks

    Arguments:
        serializers
    """

    user = MyUserSerializer(many=False)

    class Meta:
        model = Task
        fields = ('id', 'user', 'title', 'content',
                  'creation_date', 'is_complete')
        depth = 1
