from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ToDoItem
from .serializers import ToDoItemSerializer

# Handle Create and Read (GET and POST)
@api_view(['GET', 'POST'])
def task_list(request):
    if request.method == 'GET':
        tasks = ToDoItem.objects.all()
        serializer = ToDoItemSerializer(tasks, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ToDoItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Handle Update and Delete (PUT and DELETE)
@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
    try:
        task = ToDoItem.objects.get(pk=pk)
    except ToDoItem.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ToDoItemSerializer(task)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = ToDoItemSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        task.delete()
        return Response({'message': 'Task deleted successfully'}, status=status.HTTP_204_NO_CONTENT)