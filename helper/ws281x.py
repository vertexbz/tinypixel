
def order_to_byte(order: str) -> int:
    if order == "RGB":
        return ((0 << 6) | (0 << 4) | (1 << 2) | (2))
    if order == "RBG":
        return ((0 << 6) | (0 << 4) | (2 << 2) | (1))
    if order == "GRB":
        return ((1 << 6) | (1 << 4) | (0 << 2) | (2))
    if order == "GBR":
        return ((2 << 6) | (2 << 4) | (0 << 2) | (1))
    if order == "BRG":
        return ((1 << 6) | (1 << 4) | (2 << 2) | (0))
    if order == "BGR":
        return ((2 << 6) | (2 << 4) | (1 << 2) | (0))

    if order == "WRGB":
        return ((0 << 6) | (1 << 4) | (2 << 2) | (3))
    if order == "WRBG":
        return ((0 << 6) | (1 << 4) | (3 << 2) | (2))
    if order == "WGRB":
        return ((0 << 6) | (2 << 4) | (1 << 2) | (3))
    if order == "WGBR":
        return ((0 << 6) | (3 << 4) | (1 << 2) | (2))
    if order == "WBRG":
        return ((0 << 6) | (2 << 4) | (3 << 2) | (1))
    if order == "WBGR":
        return ((0 << 6) | (3 << 4) | (2 << 2) | (1))

    if order == "RWGB":
        return ((1 << 6) | (0 << 4) | (2 << 2) | (3))
    if order == "RWBG":
        return ((1 << 6) | (0 << 4) | (3 << 2) | (2))
    if order == "RGWB":
        return ((2 << 6) | (0 << 4) | (1 << 2) | (3))
    if order == "RGBW":
        return ((3 << 6) | (0 << 4) | (1 << 2) | (2))
    if order == "RBWG":
        return ((2 << 6) | (0 << 4) | (3 << 2) | (1))
    if order == "RBGW":
        return ((3 << 6) | (0 << 4) | (2 << 2) | (1))

    if order == "GWRB":
        return ((1 << 6) | (2 << 4) | (0 << 2) | (3))
    if order == "GWBR":
        return ((1 << 6) | (3 << 4) | (0 << 2) | (2))
    if order == "GRWB":
        return ((2 << 6) | (1 << 4) | (0 << 2) | (3))
    if order == "GRBW":
        return ((3 << 6) | (1 << 4) | (0 << 2) | (2))
    if order == "GBWR":
        return ((2 << 6) | (3 << 4) | (0 << 2) | (1))
    if order == "GBRW":
        return ((3 << 6) | (2 << 4) | (0 << 2) | (1))

    if order == "BWRG":
        return ((1 << 6) | (2 << 4) | (3 << 2) | (0))
    if order == "BWGR":
        return ((1 << 6) | (3 << 4) | (2 << 2) | (0))
    if order == "BRWG":
        return ((2 << 6) | (1 << 4) | (3 << 2) | (0))
    if order == "BRGW":
        return ((3 << 6) | (1 << 4) | (2 << 2) | (0))
    if order == "BGWR":
        return ((2 << 6) | (3 << 4) | (1 << 2) | (0))
    if order == "BGRW":
        return ((3 << 6) | (2 << 4) | (1 << 2) | (0))

    raise ValueError('invalid order: ' + order)
