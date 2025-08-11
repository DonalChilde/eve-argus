from eve_argus.esi_client.eve_openapi import EveOpenApi


def test_get_url(esi_schema):
    client = EveOpenApi(spec=esi_schema)
    base_url = "https://esi.evetech.net/latest/"
    op_id = "GetMarketsRegionIdHistory"
    path_params = {"region_id": 10000002}
    query_params = {"type_id": 34}
    url_with_query = client.get_url(
        base_url=base_url,
        op_id=op_id,
        path_params=path_params,
        query_params=query_params,
        include_query=True,
    )
    assert (
        url_with_query
        == "https://esi.evetech.net/latest/markets/10000002/history?type_id=34"
    )
    url_without_query = client.get_url(
        base_url=base_url,
        op_id=op_id,
        path_params=path_params,
        query_params=query_params,
        include_query=False,
    )
    assert (
        url_without_query == "https://esi.evetech.net/latest/markets/10000002/history"
    )
