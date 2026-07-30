"""
Security middleware for adding protective HTTP headers.
These headers help prevent various web attacks like XSS, clickjacking,
MIME sniffing, and information leakage.
"""


class SecurityHeadersMiddleware:
    """
    Adds security-related HTTP headers to all responses.
    Should be placed early in the middleware chain.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Content Security Policy — restrict resource loading sources
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://fonts.gstatic.com",
            "font-src 'self' https://fonts.gstatic.com",
            "img-src 'self' data: https: blob:",
            "connect-src 'self'",
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'",
        ]
        response['Content-Security-Policy'] = '; '.join(csp_directives)

        # Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'

        # Referrer Policy — limit information sent in Referer header
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Permissions Policy — restrict browser features
        response['Permissions-Policy'] = (
            'camera=(), microphone=(), geolocation=(), '
            'payment=(), usb=(), magnetometer=()'
        )

        return response
