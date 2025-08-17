# EsiClient Cache design

EsiClient caches get responses to avoid unnecessary network calls.
The response data is stored in two objects, CacheMetadata, and EsiResponse, that are linked by the cache_key field.

```python
class CacheMetadata(Basemodel):
    expires: str
    etag: str
    last_modified: str
    last_requested: str 
    cache_key: UUID

class EsiResponse(Basemodel):
    request_id: UUID
    """The UUID of the request."""
    request_url: str
    """The url of the request."""
    source: Literal["esi_cache", "esi_api"]
    """The source of the response, from the ESI api, or loaded from the cache."""
    cache_key: UUID | None
    """The cache key for the GET request/response, if available. Cache key can be None for non-get requests. cache_key will be present for all cached results."""
    text: list[str] = []
    """The response body as a list of strings. A list is used to support paged requests in one response."""

class EsiRequest(BaseModel):
    """Base class for ESI requests."""
    request_id: UUID
    op_id: str
    method: Literal["GET", "POST", "PUT", "DELETE"]
    path_params: dict[str, str | int | float] = {}
    query_params: dict[str, str | int | float] = {}
    headers: dict[str, str | None] = {}
    parent_id: UUID | None = None
    """The parent request ID, if this is a sub-request."""

class EsiAction(BaseModel):
    """Collection class to organize a single request and its response."""
    request: EsiRequest
    response: EsiResponse | None = None
    cache_metadata: CacheMetadata | None = None

class EsiClientProtocol(Protocol):
    """Protocol for ESI client operations."""

    def get_op(
        self,
        action: EsiAction,
        cache_results: bool = True,
        override_cached: bool = False,
    ) -> EsiAction:
        """Perform a get operation against eve ESI."""
        ...

class EsiCacheProtocol(Protocol):
    """Protocol for ESI cache operations."""

    def get(self, key: str) -> EsiResponse | None:
        """Get an EsiResponse from the cache, None if missing."""
        ...

    def get_metadata(self,key:str) -> CacheMetadata | None:
        """Get the cache metadata from the cache, None if missing."""
        ...

    def set(self, metadata: CacheMetadata, value: EsiResponse) -> None:
        """Set an EsiResponse in the cache."""
        ...

    def remove(self, key: str) -> None:
        """Remove an EsiResponse from the cache."""
        ...

    def clear(self) -> None:
        """Clear the cache."""
        ...

```

cache_key is a uuid based on the request url. generation of the cache_key is not part of the scope of this document.

Two objects are used in order to check the cache without loading EsiResponse data, and to allow easy discrete updating in the case of a status 304 from an etag match.

It is possible for action.cache_metadata to be supplied from an outside data store. In this case, the expires field can be checked, and an api request with {"If-None-Match":etag} header can be attempted. A matched etag returns a status 304, and the get_op function should return EsiAction(EsiRequest,None,CacheMetadata) signalling that the outside data is still valid.

EsiAction classes are used to store the requeest, and response data. The get_op function of an esi_client:

1. checks the cache for valid data
2. performs the api request if needed
3. performs any addtional paged requests if needed.
3. updates the action.response and action.cache_metadata as needed.
4. updates the cache as needed.

Possible cache situations are:

1. No cache hit, no supplied cache_metadata
    - make api request
    - update cache
    - return action(request,response,cache_metadata)

2. No cache hit, supplied metadata
    - check supplied metadata for expiration
        - if expired, make api call with etag
            - if 200
                - update cache
                - use api for response
                - return action(request,response,cache_metadata)
            - if 304
                - update supplied metadata
                - return action(request,None,cache_metadata)
        - if not expired
            - return action(request,None,cache_metadata)

3. cache hit, no supplied metadata
    - check cache for expiration
        - if expired, make api call with etag
            - if 200
                - update cache
                - use api for response
                - return action(request,response,cache_metadata)
            - if 304
                - update cache metadata
                - use cache hit for response
                - return action(request,response,cache_metadata)
        - if not expired
            - use cache hit for response
            - return action(request,response,cache_metadata)

 4. cache hit, supplied metadata
    - check cache and supplied metadata for matching etag
        - if etags match
            - check supplied metadata for expiration
                - if expired, make api call with etag
                    - if 200
                        - update cache
                        - use api for response
                        - return action(request,response,cache_metadata)
                    - if 304
                        - update supplied metadata
                        - return action(request,None,cache_metadata)
                - if not expired
                    - return action(request,None,cache_metadata)
    - if not etags match
        - make api request
        - update cache
        - return action(request,response,cache_metadata)
