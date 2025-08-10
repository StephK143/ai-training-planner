from flask import jsonify

def register_health_routes(app):
    @app.route('/api/health')
    def health_check():
        return jsonify({"status": "healthy"}), 200
