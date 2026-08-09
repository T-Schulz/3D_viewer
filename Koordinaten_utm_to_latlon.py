import math

def utm_to_latlon(easting, northing, zone, northern_hemisphere=True):
    # Mathematical conversion for UTM Zone 32N to WGS84
    # Datum: WGS84 / GRS80
    a = 6378137
    f = 1 / 298.257223563
    b = a * (1 - f)
    e = math.sqrt(1 - (b / a) ** 2)
    e_prime = math.sqrt((a ** 2 - b ** 2) / b ** 2)
    
    k0 = 0.9996
    false_easting = 500000
    false_northing = 0 if northern_hemisphere else 10000000
    
    x = easting - false_easting
    y = northing - false_northing
    
    lon0 = ((zone - 1) * 6 - 180 + 3) * math.pi / 180
    
    M = y / k0
    
    n = (a - b) / (a + b)
    alpha = (a + b) / 2 * (1 + (n ** 2) / 4 + (n ** 4) / 16)
    beta = 3 * n / 2 - 27 * (n ** 3) / 32
    gamma = 21 * (n ** 2) / 16 - 55 * (n ** 4) / 32
    delta = 151 * (n ** 3) / 96
    
    # Precise calculation for footprint latitude (phi1)
    phi1 = M / alpha
    for _ in range(5):
        phi1 = (M + beta * math.sin(2 * phi1) - gamma * math.sin(4 * phi1) + delta * math.sin(6 * phi1)) / alpha
        
    p1 = phi1
    
    rho1 = a * (1 - e ** 2) / (1 - e ** 2 * math.sin(p1) ** 2) ** 1.5
    nu1 = a / math.sqrt(1 - e ** 2 * math.sin(p1) ** 2)
    
    D = x / (nu1 * k0)
    
    lat = p1 - (nu1 * math.tan(p1) / rho1) * (D ** 2 / 2 - (5 + 3 * math.tan(p1) ** 2 + 10 * e_prime ** 2 * math.cos(p1) ** 2 - 4 * e_prime ** 4 * math.cos(p1) ** 4 - 9 * e_prime ** 2 * math.tan(p1) ** 2) * D ** 4 / 24 + (61 + 90 * math.tan(p1) ** 2 + 298 * e_prime ** 2 * math.cos(p1) ** 2 + 45 * math.tan(p1) ** 4 - 252 * e_prime ** 2 * math.tan(p1) ** 2 - 3 * e_prime ** 4 * math.cos(p1) ** 4) * D ** 6 / 720)
    
    lon = lon0 + (D - (1 + 2 * math.tan(p1) ** 2 + e_prime ** 2 * math.cos(p1) ** 2) * D ** 3 / 6 + (5 - 2 * e_prime ** 2 * math.cos(p1) ** 2 + 28 * math.tan(p1) ** 2 - 3 * e_prime ** 4 * math.cos(p1) ** 4 + 8 * e_prime ** 2 * math.tan(p1) ** 2 + 24 * math.tan(p1) ** 4) * D ** 5 / 120) / math.cos(p1)
    
    return math.degrees(lat), math.degrees(lon)

lat, lon = utm_to_latlon(400000, 5706000, 32)
print(f"Lat: {lat:.6f}, Lon: {lon:.6f}")