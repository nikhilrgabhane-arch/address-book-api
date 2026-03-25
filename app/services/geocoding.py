from geopy.distance import geodesic
from app.core.logger import setup_logger

logger = setup_logger(__name__)

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculates the geodesic distance between two coordinate pairs (in kilometers),
    using the geopy library which implements the accurate Vincenty algorithm.
    
    Args:
        lat1, lon1: Coordinates of the first point.
        lat2, lon2: Coordinates of the second point.
        
    Returns:
        float: The distance in kilometers between the two points.
    """
    try:
        point1 = (lat1, lon1)
        point2 = (lat2, lon2)
        # geodesic returns a distance object; .kilometers extracts the float
        distance_km = geodesic(point1, point2).kilometers
        return distance_km
    except ValueError as e:
        logger.error(f"Geocoding error. Invalid coordinates provided: {(lat1, lon1)} and {(lat2, lon2)}. Error: {e}")
        raise ValueError("Invalid coordinates provided for distance calculation.")
