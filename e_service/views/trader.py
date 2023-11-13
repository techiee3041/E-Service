from e_service.app import app
from flask import jsonify, request
from e_service.models.data import Trader, Cords , User
from haversine import haversine
import sys
print(sys.path)

# ...

@app.route('/fetch_traders/<int:id_user>', methods=['GET'])
def fetch_nearby_traders(id_user):
    # Fetch the user's location
    user_location = Cords.query.filter_by(id_user=id_user).first()
    if user_location is None:
        return jsonify({'error': 'User location not found'})

    user_lat, user_lon = Cords.latitude, user_location.longitude

    # Fetch the selected traders_services from the user's request
    selected_services = request.args.get('traders_services')

    # Fetch nearby traders matching the selected traders_services
    nearby_traders = []

    for trader in Trader.query.filter_by(traders_services=selected_services).all():
        trader_lat, trader_lon = trader.latitude, trader.longitude
        distance = haversine(user_lat, user_lon, trader_lat, trader_lon)
        if distance <= 1:  # Within 1 kilometer
            nearby_traders.append({'name': trader.name, 'distance': distance})

    return jsonify({'nearby_traders': nearby_traders})