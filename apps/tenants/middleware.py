from django.http import Http404
from .models import Tenant


def _extract_subdomain_from_host(host: str) -> str:
    host_without_port = host.split(":")[0]
    if host_without_port.startswith("localhost") or host_without_port.startswith("127.0.0.1"):
        return "default"
    parts = host_without_port.split(".")
    return parts[0] if len(parts) >= 3 else "default"


class TenantMiddleware:
    """
    Middleware que resuelve el tenant desde el subdominio y lo inyecta
    en el objeto request como request.tenant y request.tenant_id.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        subdomain = _extract_subdomain_from_host(request.get_host())
        try:
            tenant = Tenant.objects.get(subdomain=subdomain)
        except Tenant.DoesNotExist:
            # En desarrollo, permitir "default" sin registro
            if subdomain == "default":
                tenant = None
            else:
                raise Http404("Tenant no encontrado")

        request.tenant = tenant
        request.tenant_id = getattr(tenant, "id", None)

        response = self.get_response(request)
        return response


