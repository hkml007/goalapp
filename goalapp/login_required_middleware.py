# from django.shortcuts import redirect
# from django.urls import reverse

# class LoginRequiredMiddleware:
#     """
#     Middleware to require login for all routes except:
#     - login
#     - register
#     - admin_user route
#     """

#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.exempt_urls = [
#             reverse('logins'),
#             reverse('register'),
#         ]

#     def __call__(self, request):
#         path = request.path

#         if path.startswith('/admin_user/'):
#             return self.get_response(request)

#         if path in self.exempt_urls:
#             return self.get_response(request)

#         # Redirect if not logged in
#         if not request.session.get('user_id'):
#             return redirect('logins')

#         return self.get_response(request)



from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be logged in to access certain pages.
    Allows access if any one of the session keys for valid users is present.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            reverse('logins'),
            reverse('register'),
            # Add other exempt URLs as needed
        ]
        self.session_keys = [
            'admin',
            'user_id',
        ]

    def __call__(self, request):
        # Skip check for exempt URLs
        if request.path not in self.exempt_urls:
            # Check if any of the expected session keys are present
            if not any(request.session.get(key) for key in self.session_keys):
                return redirect('logins')  # Redirect to login if not authenticated

        return self.get_response(request)
