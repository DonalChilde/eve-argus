from eve_argus.eve_argus_esi.esi_cache.esi_cache_protocol import EsiCacheProtocol
from eve_argus.eve_argus_esi.esi_models import EsiAction
from eve_argus.eve_argus_esi.snippets.aiohttp.queue_simple import AiohttpAction


def handle_get_response(
    esi_action: EsiAction,
    aiohttp_action: AiohttpAction,
    cache: EsiCacheProtocol,
    cache_results: bool = True,
    override_cached: bool = False,
) -> None:
    pass
    if aiohttp_action.response is None:
        # this signals that the action was skipped, likely a 400+ status code.
        # TODO refine the handling here.
        raise ValueError(
            f"Aiohttp action response is None for key {key}, cannot process response."
        )
