from shapely import wkb, wkt , ops, Polygon, geometry
from shapely.geometry import Polygon, mapping

qq = '010300000001000000050000000000000000003e4000000000000024400000000000004440000000000000444000000000000034400000000000004440000000000000244000000000000034400000000000003e400000000000002440'

def convert_poly(wkb_poly):
    poly = wkb.loads(bytes.fromhex(wkb_poly))
    poly_mapped = mapping(poly)
    poly_coordinates = poly_mapped['coordinates'][0]

    return poly_coordinates

print(convert_poly(qq))