class CompleteProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        
        # Get all fields from request
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        language = request.data.get('language')
        
        # Update user fields if provided
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if email is not None:
            user.email = email
        if language is not None:
            user.language = language
        
        # Save the user
        user.save()
        
        # Return the updated user data
        return Response({
            'message': 'Profile completed successfully',
            'user': {
                'id': user.id,
                'phone_number': user.phone_number,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'language': user.language,
                'civic_score': user.civic_score,
                'account_type': user.account_type
            }
        })
