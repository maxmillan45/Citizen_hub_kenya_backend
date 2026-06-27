# Add or update this view in your accounts/views.py
class CompleteProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.email = request.data.get('email', user.email)
        user.language = request.data.get('language', user.language)
        user.save()
        
        return Response({
            'message': 'Profile completed successfully',
            'user': {
                'id': user.id,
                'phone_number': user.phone_number,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'language': user.language,
                'civic_score': user.civic_score,
                'account_type': user.account_type
            }
        })
