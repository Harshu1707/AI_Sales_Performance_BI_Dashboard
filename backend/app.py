from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from routes.api import api_bp


def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/")
    def home():
        return jsonify({
            "message": "InsightIQ Backend Running"
        })

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "service": "InsightIQ API"})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
