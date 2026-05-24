from flask import Blueprint, jsonify, request

from services.ai_service import generate_chat_answer, generate_insights
from services.data_service import (
    build_chart_payload,
    build_kpi_payload,
    load_superstore,
    save_uploaded_dataset,
)
from services.forecast_service import build_forecast

api_bp = Blueprint("api", __name__)


@api_bp.get("/kpis")
def kpis():
    df = load_superstore()
    return jsonify(build_kpi_payload(df))


@api_bp.get("/charts")
def charts():
    df = load_superstore()
    return jsonify(build_chart_payload(df))


@api_bp.get("/forecast")
def forecast():
    df = load_superstore()
    return jsonify(build_forecast(df))


@api_bp.get("/insights")
def insights():
    df = load_superstore()
    return jsonify(generate_insights(df))


@api_bp.post("/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    question = payload.get("question", "").strip()
    history = payload.get("history", [])
    if not question:
        return jsonify({"answer": "Ask a question about sales, profit, customers, products, or forecasting."})
    df = load_superstore()
    return jsonify({"answer": generate_chat_answer(df, question, history)})


@api_bp.post("/upload")
def upload():
    if "file" not in request.files:
        return jsonify({"error": "Upload a CSV file using the form field named 'file'."}), 400
    saved_path = save_uploaded_dataset(request.files["file"])
    df = load_superstore(saved_path)
    return jsonify({"message": "Dataset uploaded", "rows": len(df), "kpis": build_kpi_payload(df)})


@api_bp.get("/")
def home():
    return jsonify({"message": "Backend Running Successfully"})