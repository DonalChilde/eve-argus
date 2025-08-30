"""Esi client for retrieving data from the Eve Online ESI API.

Multiple query conditions must be handled.
Get requests might be cached.
Get and post requests might be paged.
Given that some operations might involve 10000 queries, concurrent requests should be considered.
For paged requests, only the first page is cached after collecting all pages and adding them to the first page response.
"""

import logging
from copy import deepcopy
from uuid import UUID

from eve_argus.esi_link.esi_link import EsiLink, EsiQuery, QueryResponse
from eve_argus.esi_link.header_funcs import last_modified, page_count
from eve_argus.esi_link.link_cache_protocol import CacheStatus, LinkCacheProtocol
from eve_argus.eve_argus_esi.esi_schema.eve_openapi_protocol import EveOpenApiProtocol
from eve_argus.helpers.cache_id_from_url import cache_id_from_url

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def _make_cache_key(query: EsiQuery, schema: EveOpenApiProtocol) -> UUID:
    url = schema.get_url(
        op_id=query["operation"],
        path_params=query["path_parameters"],
        query_params=query["query_parameters"],
        include_query=True,
    )
    cache_key = cache_id_from_url(url)
    return cache_key


def _validate_query(query: EsiQuery, schema: EveOpenApiProtocol) -> bool:
    valid = schema.validate_operation(
        op_id=query["operation"],
        path_params=query["path_parameters"],
        query_params=query["query_parameters"],
    )
    return valid


def _inject_etag(
    query: EsiQuery, cache: LinkCacheProtocol, schema: EveOpenApiProtocol
) -> None:
    # get the etag from the cache
    cache_key = _make_cache_key(query, schema)
    metadata = cache.get_cache_metadata(cache_key)
    etag = metadata.etag if metadata else ""
    if etag:
        query["headers"]["If-None-Match"] = etag


def _build_pages_queries(
    query: EsiQuery, response: QueryResponse
) -> dict[UUID, EsiQuery]:
    paged_queries = []
    pages = page_count(response.headers)
    for page in range(2, pages + 1):
        paged_query = deepcopy(query)
        paged_query["query_parameters"] = {**query["query_parameters"], "page": page}
        paged_queries.append(paged_query)
    return {query["query_id"]: query for query in paged_queries}


def paged_query(
    query: EsiQuery,
    cache: LinkCacheProtocol,
    schema: EveOpenApiProtocol,
    link: EsiLink,
    fail_on_error: bool = False,
) -> QueryResponse:
    _validate_query(query, schema)
    response: QueryResponse | None = None
    if schema.is_cached(query["operation"]):
        cache_key = _make_cache_key(query, schema)
        cache_status = cache.get(cache_key)
        if cache_status is CacheStatus.HIT:
            return cache.get_response(cache_key)
        elif cache_status is CacheStatus.STALE:
            # If the cache is stale, we need to revalidate it
            _inject_etag(query, cache, schema)
            response = link.do_query(query)
            if response.status_code == 304:
                # If we get a 304 response, we can return the cached response
                cache.update_304(cache_key, response)
                response = cache.get_response(cache_key)
                return response
    if response is None:
        response = link.do_query(query)
    if response.status_code != 200:
        logger.error(f"Bad response for {query!r}: {response!r}")
        if fail_on_error:
            raise ValueError(
                f"Unexpected status code: {response.status_code} for {query['query_id']}"
            )
    paged_queries = _build_pages_queries(query, response)
    responses = link.do_queries(paged_queries)
    parent_last_modified = last_modified(response.headers)
    for key, resp in responses.items():
        if resp.status_code != 200:
            logger.error(f"Bad response for {key}: {resp!r}")
            if fail_on_error:
                raise ValueError(
                    f"Unexpected status code: {resp.status_code} for {key}"
                )
        if parent_last_modified != last_modified(resp.headers):
            logger.error(f"Last-Modified header mismatch for {key}: {resp.real_url}")
            if fail_on_error:
                raise ValueError(f"Last-Modified header mismatch for {key}")
        response.paged_text.append(resp.text)

    if schema.is_cached(query["operation"]):
        # add the completed response to the cache.
        cache_key = _make_cache_key(query, schema)
        metadata = cache.build_metadata(response)
        cache.set(cache_key, metadata, response)
    return response


def esi_batch_query(
    queries: dict[UUID, EsiQuery],
    cache: LinkCacheProtocol,
    schema: EveOpenApiProtocol,
    link: EsiLink,
    fail_on_error: bool = False,
) -> dict[UUID, QueryResponse]:
    results: dict[UUID, QueryResponse] = {}
    one_pass = set[UUID]()
    for key, query in queries.items():
        _validate_query(query, schema)
        one_pass.add(key)
        if schema.is_paged(query["operation"]):
            results[key] = paged_query(
                query=query,
                cache=cache,
                schema=schema,
                link=link,
                fail_on_error=fail_on_error,
            )
            one_pass.remove(key)
        if schema.is_cached(query["operation"]):
            cache_key = _make_cache_key(query, schema)
            cache_status = cache.get(cache_key)
            if cache_status is CacheStatus.HIT:
                results[key] = cache.get_response(cache_key)
                one_pass.remove(key)
            elif cache_status is CacheStatus.STALE:
                # If the cache is stale, we need to revalidate it
                _inject_etag(query, cache, schema)
    responses = link.do_queries({k: queries[k] for k in one_pass})
    for key, response in responses.items():
        if schema.is_cached(queries[key]["operation"]):
            if response.status_code == 304:
                # If we get a 304 response, we can return the cached response
                cache_key = _make_cache_key(queries[key], schema)
                cache.update_304(cache_key, response)
                response = cache.get_response(cache_key)
            elif response.status_code == 200:
                # If we get a 200 response, we need to update the cache
                cache_key = _make_cache_key(queries[key], schema)
                metadata = cache.build_metadata(response)
                cache.set(cache_key, metadata, response)
        results[key] = response
        if response.status_code != 200 and response.status_code != 304:
            logger.error(f"Bad response for {key}: {response!r}")
            if fail_on_error:
                raise ValueError(
                    f"Unexpected status code: {response.status_code} for {key}"
                )
    return results
