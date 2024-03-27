from geopy.distance import distance

from core.apps.delivery.models import Location


def calculate_distance(first_loc: Location, second_loc: Location) -> float:
    """Считает расстояние между 2-мя локациями в милях"""
    return distance(first_loc.coordinates, second_loc.coordinates).miles