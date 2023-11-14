from flask import Flask, render_template, request
from e_service.models.data import Trader, UserLocation, TraderLocation, Product
from haversine import haversine

app = Flask(__name__)

# ... (existing code)

@app.route('/fetch_user_and_trader_locations/<int:user_id>', methods=['GET'])
def fetch_user_and_trader_locations(user_id):
    # Fetch the user's location
    user_location = UserLocation.query.filter_by(user_id=user_id).first()
    if user_location is None:
        return render_template('error.html', error='User location not found')

    user_lat, user_lon = user_location.latitude, user_location.longitude

    # Fetch nearby traders within 1km along with their services
    nearby_traders = []

    for trader_location in TraderLocation.query.all():
        trader_lat, trader_lon = trader_location.latitude, trader_location.longitude
        distance = haversine(user_lat, user_lon, trader_lat, trader_lon)

        if distance <= 1:
            # Fetch services offered by the trader
            trader_services = Product.query.filter_by(trader_id=trader_location.trader_id).all()

            nearby_traders.append({
                'trader_id': trader_location.trader_id,
                'full_name': trader_location.trader.full_name,
                'phone_number': trader_location.trader.phone_number,
                'distance': distance,
                'services': [{
                    'category': service.category,
                    'description': service.description,
                    'product_name': service.product_name
                } for service in trader_services]
            })

    # Organize traders into categories based on their services
    categorized_traders = {}
    for trader in nearby_traders:
        for service in trader['services']:
            category = service['category']
            if category not in categorized_traders:
                categorized_traders[category] = []

            categorized_traders[category].append(trader)

    return render_template('nearby_traders.html', userLat=user_lat, userLon=user_lon, categorized_traders=categorized_traders)
