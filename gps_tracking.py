from flask_socketio import SocketIO

socketio = SocketIO()

def broadcast_gps_location(lat, lon):
    socketio.emit('gps_location', {'lat': lat, 'lon': lon})
    