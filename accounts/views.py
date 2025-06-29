from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user and return their authentication token
    """
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        token = Token.objects.get(user=user)

        return Response({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': 'user.first_name',
                'last_name': 'user.last_name',
            },
            'token': token.key
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Login user and return their authentication token
    """
    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'token': token.key
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    """
    Get or update user profile
    """
    user = request.user

    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(
            user, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'user': serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Change user password
    """
    serializer = ChangePasswordSerializer(
        data=request.data, context={'request': request})

    if serializer.is_valid():
        serializer.save()

        # Generate a new Token for security (invalidate old session)
        Token.objects.filter(user=request.user).delete()
        new_token = Token.objects.create(user=request.user)

        return Response({
            'message': 'Password changed successfully',
            'token': new_token.key
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Logout users by deleting thier authentication token
    """

    # Delete the user's token to logout
    Token.objects.filter(user=request.user).delete()

    return Response({
        'message': 'Successfully logged out'
    }, status=status.HTTP_200_OK)
