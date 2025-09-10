from django.http import JsonResponse, Http404
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Tenant
from typing import Any, Dict


def serialize_tenant(tenant: Tenant) -> Dict[str, Any]:
    return {
        "id": tenant.id,
        "name": tenant.name,
        "subdomain": tenant.subdomain,
        "status": tenant.status,
        "created_at": tenant.created_at.isoformat() if tenant.created_at else None,
        "updated_at": tenant.updated_at.isoformat() if tenant.updated_at else None,
    }


@method_decorator(csrf_exempt, name="dispatch")
class TenantListView(View):
    def get(self, request):
        tenants = Tenant.objects.all().order_by("id")
        data = [serialize_tenant(t) for t in tenants]
        return JsonResponse({"results": data, "count": len(data)}, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class TenantDetailView(View):
    def get(self, request, pk: int):
        try:
            tenant = Tenant.objects.get(pk=pk)
        except Tenant.DoesNotExist:
            raise Http404("Tenant no encontrado")
        return JsonResponse(serialize_tenant(tenant), safe=False)


def _extract_subdomain_from_host(host: str) -> str:
    # host puede incluir puerto, ej: subdominio.dominio.tld:8000
    host_without_port = host.split(":")[0]
    parts = host_without_port.split(".")
    # Si hay al menos 3 partes, asuma primer elemento como subdominio
    # Para desarrollo con localhost, permita 'localhost' sin subdominio
    if host_without_port.startswith("localhost") or host_without_port.startswith("127.0.0.1"):
        return "default"
    return parts[0] if len(parts) >= 3 else "default"


def current_tenant(request):
    subdomain = _extract_subdomain_from_host(request.get_host())
    try:
        tenant = Tenant.objects.get(subdomain=subdomain)
    except Tenant.DoesNotExist:
        raise Http404("Tenant actual no encontrado")
    return JsonResponse(serialize_tenant(tenant), safe=False)
