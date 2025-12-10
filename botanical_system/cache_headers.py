# middleware/cache_headers.py
from django.utils.deprecation import MiddlewareMixin

class CacheControlForAuthMiddleware(MiddlewareMixin):
    """
    Ensure we don't accidentally let CDNs/cache servers serve HTML
    intended for authenticated users to other visitors.
    """

    def process_response(self, request, response):
        # Only touch HTML responses
        content_type = response.get('Content-Type', '')
        if 'text/html' not in content_type.lower():
            return response

        # Authenticated users: prevent public caching
        if getattr(request, 'user', None) and request.user.is_authenticated:
            # prevents intermediary caches from storing the page
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
            # Remove any cached-friendly headers if present
            if 'Expires' in response:
                del response['Expires']
        else:
            # Anonymous users: allow short public caching (adjust max-age as desired)
            # public cache is okay since content for anonymous users is identical,
            # but keep it short to avoid stale content: 60s is safe starting point.
            response['Cache-Control'] = 'public, max-age=60, s-maxage=60'
            # ensure Vary includes Cookie so caches consider cookies
            vary = response.get('Vary', '')
            if 'Cookie' not in vary:
                response['Vary'] = (vary + ', Cookie').strip(', ')
        return response
