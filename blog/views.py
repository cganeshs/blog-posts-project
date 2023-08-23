from rest_framework import generics
from rest_framework.response import Response
from .serializers import PostSerializer, Post
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .pagination import CustomPagination
from rest_framework.filters import SearchFilter
from rest_framework.throttling import UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend


# Define a view for listing and creating posts
class PostListCreateView(generics.ListCreateAPIView):
    # Specify the queryset to retrieve all Post objects
    queryset = Post.objects.all()
    # Use the PostSerializer to serialize Post objects
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title','body','author']
    search_fields = ['title','body','author']
    throttle_classes = [UserRateThrottle]


    # Custom list method to handle listing of posts
    def list(self, request):
        user = request.user
        if user.is_superuser:
            queryset = self.get_queryset()
        else:
            queryset = self.queryset.filter(author=user)
        page = self.paginate_queryset(queryset)
        if page:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
    
    # Custom create method to handle post creation
    def create(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(author=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Define a view for retrieving, updating, and deleting a single post
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_object(self):
        # Retrieve the object based on the provided id
        obj = super().get_object()
        # Check if the user is a superuser or the author of the post
        if not self.request.user.is_superuser and obj.author != self.request.user:
            raise PermissionDenied("You do not have permission to perform this action.")
        return obj