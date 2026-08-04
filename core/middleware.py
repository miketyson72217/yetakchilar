"""
Security middleware for adding protective HTTP headers.
These headers help prevent various web attacks like XSS, clickjacking,
MIME sniffing, and information leakage.
"""
from django.http import HttpResponsePermanentRedirect


class NonWwwRedirectMiddleware:
    """
    www.yetakchilar.uz ni yetakchilar.uz ga 301 redirect qiladi.
    Bu telefonlarda www.* domeniga tushib qolish muammosini hal qiladi.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().lower()
        # www. bilan boshlansa — www siz variantga redirect
        if host.startswith('www.'):
            non_www_host = host[4:]  # "www." ni olib tashla
            redirect_url = f"{request.scheme}://{non_www_host}{request.get_full_path()}"
            return HttpResponsePermanentRedirect(redirect_url)
        return self.get_response(request)


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

        # Disable QUIC/HTTP3 to prevent ERR_QUIC_PROTOCOL_ERROR on mobile
        response['Alt-Svc'] = 'clear'

        return response
