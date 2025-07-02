# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "preston",
# ]
# ///
import preston

def main() -> None:
    p = preston.Preston(useragent="preston-test")
    data = p.get_op('get_markets_region_id_history', region_id=10000002, type_id=34)
    print(data)

if __name__ == "__main__":
    main()
