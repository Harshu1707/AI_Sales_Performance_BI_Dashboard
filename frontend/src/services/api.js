import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  timeout: 30000
});

export async function getDashboardData() {
  const [kpis, charts, forecast, insights] = await Promise.all([
    api.get("/kpis"),
    api.get("/charts"),
    api.get("/forecast"),
    api.get("/insights")
  ]);
  return {
    kpis: kpis.data,
    charts: charts.data,
    forecast: forecast.data,
    insights: insights.data
  };
}

export async function askInsightIQ(question, history) {
  const response = await api.post("/chat", { question, history });
  return response.data.answer;
}

export async function uploadDataset(file) {
  const form = new FormData();
  form.append("file", file);
  const response = await api.post("/upload", form, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return response.data;
}
