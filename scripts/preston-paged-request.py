# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
from collections.abc import Sequence
from preston import Preston


def main() -> None:
    print("Hello from preston-paged-request.py!")
    esi = Preston(user_agent="Eve Argus testing")
    region_id = 10000002  # The Forge region ID
    # Example of a paged request
    paged_data: Sequence[Sequence[int]] = []
    data = esi.get_op("get_markets_region_id_types", region_id=str(region_id))
    paged_data.append(data)  # type: ignore
    page_count = int(esi.stored_headers[0].get("x-pages", 1))
    print(
        f"Retrieved {len(data)} market types for region {region_id}, page 1 of {page_count}"
    )

    print(f"Total pages: {page_count}")
    for page in range(2, page_count + 1):
        data = esi.get_op(
            "get_markets_region_id_types", region_id="10000002", page=str(page)
        )
        print(
            f"Retrieved {len(data)} market types for page {page} in  region {region_id}."
        )
        paged_data.append(data)  # type: ignore
    print(f"Total market types retrieved: {sum(len(page) for page in paged_data)}")
    print("Paged request completed successfully.")


if __name__ == "__main__":
    main()
