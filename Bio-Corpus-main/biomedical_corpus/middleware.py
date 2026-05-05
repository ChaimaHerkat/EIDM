"""
Custom middleware for HTTP caching and performance headers.
"""


class CacheHeaderMiddleware:
    """Add cache control headers to responses."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Static files: cache for 1 year (they have content-based names)
        if request.path.startswith('/static/'):
            response['Cache-Control'] = 'public, max-age=31536000, immutable'
        
        # API/HTML responses: cache for 5 minutes
        elif request.path.startswith('/articles/') or request.path == '/':
            response['Cache-Control'] = 'public, max-age=300'
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Enable compression hints
        response['Vary'] = 'Accept-Encoding'
        
        return response
