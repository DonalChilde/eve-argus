from eve_argus.eve_argus_esi.esi_models import EsiRequest
from eve_argus.eve_argus_esi.esi_schema.eve_openapi_protocol import EveOpenApiProtocol


def compile_cache_url(
    base_url: str, request: EsiRequest, open_api: EveOpenApiProtocol
) -> str:
    url = open_api.get_url(
        base_url=base_url,
        op_id=request.op_id,
        path_params=request.path_params,
        query_params=request.query_params,
        include_query=True,
    )
    return url
