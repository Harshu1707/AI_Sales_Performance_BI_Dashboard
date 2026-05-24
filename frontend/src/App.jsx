import { AnimatePresence, motion } from "framer-motion";
import html2canvas from "html2canvas";
import {
  Activity,
  Bot,
  BrainCircuit,
  ChevronRight,
  Download,
  LineChart,
  Moon,
  RefreshCw,
  Search,
  Sparkles,
  Sun,
  Upload,
  WalletCards
} from "lucide-react";
import { useEffect, useMemo, useRef, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ComposedChart,
  Legend,
  Line,
  Pie,
  PieChart,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import { askInsightIQ, getDashboardData, uploadDataset } from "./services/api";

const currency = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", notation: "compact" });
const number = new Intl.NumberFormat("en-US", { notation: "compact" });
const colors = ["#14b8a6", "#f97316", "#a855f7", "#22c55e", "#38bdf8", "#f43f5e"];

const demoData = {
  kpis: {
    totalSales: 2300000,
    totalProfit: 286397,
    profitMargin: 12.47,
    averageOrderValue: 458.61,
    customerCount: 793,
    totalOrders: 5009,
    salesGrowth: 8.4
  },
  charts: {
    monthlyTrend: [
      { month: "Jul 2014", sales: 45644, profit: 6422 },
      { month: "Aug 2014", sales: 63120, profit: 7810 },
      { month: "Sep 2014", sales: 87866, profit: 10924 },
      { month: "Oct 2014", sales: 77776, profit: 9273 },
      { month: "Nov 2014", sales: 118448, profit: 14761 },
      { month: "Dec 2014", sales: 83829, profit: 10240 }
    ],
    regionSales: [
      { Region: "West", sales: 725458, profit: 108418 },
      { Region: "East", sales: 678781, profit: 91523 },
      { Region: "Central", sales: 501239, profit: 39706 },
      { Region: "South", sales: 391721, profit: 46749 }
    ],
    categoryProfit: [
      { Category: "Technology", profit: 145454, sales: 836154 },
      { Category: "Office Supplies", profit: 122491, sales: 719047 },
      { Category: "Furniture", profit: 18451, sales: 741999 }
    ],
    topProducts: [
      { product: "Canon imageCLASS 2200", sales: 61600, profit: 25199 },
      { product: "Fellowes PB500", sales: 27453, profit: 7753 },
      { product: "Cisco TelePresence", sales: 22638, profit: 3671 },
      { product: "HON 5400 Series", sales: 21871, profit: 3971 }
    ],
    discountScatter: [
      { Discount: 0, Profit: 24, Sales: 120, Category: "Technology" },
      { Discount: 0.2, Profit: 8, Sales: 230, Category: "Furniture" },
      { Discount: 0.7, Profit: -84, Sales: 180, Category: "Office Supplies" }
    ],
    segmentAnalysis: [
      { Segment: "Consumer", sales: 1161401, profit: 134119 },
      { Segment: "Corporate", sales: 706146, profit: 91979 },
      { Segment: "Home Office", sales: 429653, profit: 60298 }
    ],
    stateHeatmap: [
      { State: "California", sales: 457688, profit: 76381 },
      { State: "New York", sales: 310876, profit: 74038 },
      { State: "Texas", sales: 170188, profit: -25729 },
      { State: "Washington", sales: 138641, profit: 33402 }
    ],
    lossProducts: []
  },
  forecast: {
    history: [
      { month: "Oct 2014", sales: 77776 },
      { month: "Nov 2014", sales: 118448 },
      { month: "Dec 2014", sales: 83829 }
    ],
    forecast: [
      { month: "Jan 2015", predictedSales: 90120 },
      { month: "Feb 2015", predictedSales: 92880 },
      { month: "Mar 2015", predictedSales: 95640 }
    ],
    predictedGrowth: 14.1
  },
  insights: {
    source: "demo",
    insights: [
      { title: "West leads profitable growth", body: "Protect the West region with targeted inventory and high-value retention campaigns.", tag: "Region" },
      { title: "Technology carries margin", body: "Technology produces the strongest profit pool and should anchor cross-sell programs.", tag: "Category" },
      { title: "Discount leakage needs rules", body: "Large discounts correlate with negative profit in weak product pockets.", tag: "Margin" }
    ]
  }
};

function Card({ className = "", children }) {
  return <div className={`rounded-lg border border-white/10 bg-white/[0.055] shadow-glow backdrop-blur-xl ${className}`}>{children}</div>;
}

function KpiCard({ icon: Icon, label, value, suffix = "", tone, format = "number" }) {
  const [shown, setShown] = useState(0);
  useEffect(() => {
    const raw = Number(value) || 0;
    let frame = 0;
    const frames = 32;
    const timer = setInterval(() => {
      frame += 1;
      setShown(raw * Math.min(frame / frames, 1));
      if (frame >= frames) clearInterval(timer);
    }, 20);
    return () => clearInterval(timer);
  }, [value]);
  const formatted = format === "currency" ? currency.format(shown) : number.format(shown);
  return (
    <motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} whileHover={{ y: -4 }}>
      <Card className="p-4">
        <div className="flex items-center justify-between gap-3">
          <div>
            <p className="text-xs uppercase tracking-[0.18em] text-slate-400">{label}</p>
            <p className="mt-2 text-2xl font-semibold text-white">{formatted}{suffix}</p>
          </div>
          <div className={`grid h-11 w-11 place-items-center rounded-lg ${tone}`}>
            <Icon className="h-5 w-5 text-white" />
          </div>
        </div>
      </Card>
    </motion.div>
  );
}

function ChartCard({ title, subtitle, children }) {
  return (
    <Card className="p-4">
      <div className="mb-4 flex items-start justify-between gap-3">
        <div>
          <h3 className="text-sm font-semibold text-white">{title}</h3>
          <p className="mt-1 text-xs text-slate-400">{subtitle}</p>
        </div>
        <Sparkles className="h-4 w-4 text-teal-300" />
      </div>
      <div className="h-72">{children}</div>
    </Card>
  );
}

function InsightCards({ insights }) {
  const cards = insights?.insights || [];
  const narrative = insights?.narrative;
  return (
    <div className="grid gap-4 lg:grid-cols-3">
      {narrative ? (
        <Card className="p-5 lg:col-span-3">
          <p className="text-xs uppercase tracking-[0.18em] text-teal-300">Gemini Executive Brief</p>
          <p className="mt-3 whitespace-pre-line text-sm leading-6 text-slate-200">{narrative}</p>
        </Card>
      ) : cards.map((item, index) => (
        <motion.div key={item.title} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: index * 0.08 }}>
          <Card className="h-full p-5">
            <span className="rounded-full border border-teal-300/30 bg-teal-300/10 px-3 py-1 text-xs text-teal-200">{item.tag}</span>
            <h3 className="mt-4 text-lg font-semibold text-white">{item.title}</h3>
            <p className="mt-2 text-sm leading-6 text-slate-300">{item.body}</p>
          </Card>
        </motion.div>
      ))}
    </div>
  );
}

function Chatbot() {
  const [messages, setMessages] = useState([
    { role: "assistant", text: "Ask me about profit, discounts, products, regions, or growth recommendations." }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
  const suggestions = ["Which category generated highest profit?", "Why did profit decrease in some regions?", "Show top-performing products."];

  useEffect(() => bottomRef.current?.scrollIntoView({ behavior: "smooth" }), [messages, loading]);

  async function send(question = input) {
    if (!question.trim() || loading) return;
    const next = [...messages, { role: "user", text: question }];
    setMessages(next);
    setInput("");
    setLoading(true);
    const answer = await askInsightIQ(question, next).catch(() => "The AI service is unavailable. Check that the Flask API is running and Gemini is configured.");
    setMessages([...next, { role: "assistant", text: answer }]);
    setLoading(false);
  }

  return (
    <Card className="flex h-[560px] flex-col p-4">
      <div className="flex items-center gap-3 border-b border-white/10 pb-4">
        <div className="grid h-10 w-10 place-items-center rounded-lg bg-violet-500/25"><Bot className="h-5 w-5 text-violet-200" /></div>
        <div>
          <h3 className="font-semibold text-white">InsightIQ AI Analyst</h3>
          <p className="text-xs text-slate-400">Gemini-powered business Q&A</p>
        </div>
      </div>
      <div className="flex-1 space-y-3 overflow-y-auto py-4 pr-1">
        {messages.map((message, index) => (
          <div key={index} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`max-w-[86%] rounded-lg px-4 py-3 text-sm leading-6 ${message.role === "user" ? "bg-teal-500 text-slate-950" : "bg-white/10 text-slate-100"}`}>
              {message.text}
            </div>
          </div>
        ))}
        {loading && <div className="w-fit rounded-lg bg-white/10 px-4 py-3 text-sm text-slate-300">InsightIQ is thinking...</div>}
        <div ref={bottomRef} />
      </div>
      <div className="mb-3 flex flex-wrap gap-2">
        {suggestions.map((item) => (
          <button key={item} onClick={() => send(item)} className="rounded-full border border-white/10 px-3 py-1 text-xs text-slate-300 transition hover:border-teal-300/50 hover:text-teal-100">
            {item}
          </button>
        ))}
      </div>
      <div className="flex gap-2">
        <input value={input} onChange={(event) => setInput(event.target.value)} onKeyDown={(event) => event.key === "Enter" && send()} className="min-w-0 flex-1 rounded-lg border border-white/10 bg-slate-950/70 px-4 py-3 text-sm text-white outline-none ring-teal-400/30 placeholder:text-slate-500 focus:ring-4" placeholder="Ask a business question..." />
        <button onClick={() => send()} className="grid h-12 w-12 place-items-center rounded-lg bg-teal-400 text-slate-950 transition hover:bg-teal-300" aria-label="Send question"><ChevronRight /></button>
      </div>
    </Card>
  );
}

export default function App() {
  const [data, setData] = useState(demoData);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");
  const [theme, setTheme] = useState("dark");
  const dashboardRef = useRef(null);

  async function refresh() {
    setLoading(true);
    const next = await getDashboardData().catch(() => demoData);
    setData(next);
    setLoading(false);
  }

  useEffect(() => { refresh(); }, []);

  const filteredProducts = useMemo(() => {
    const q = query.toLowerCase();
    return (data.charts.topProducts || []).filter((item) => item.product.toLowerCase().includes(q));
  }, [data, query]);

  async function exportScreenshot() {
    if (!dashboardRef.current) return;
    const canvas = await html2canvas(dashboardRef.current, { backgroundColor: "#020617" });
    const link = document.createElement("a");
    link.download = "insightiq-dashboard.png";
    link.href = canvas.toDataURL("image/png");
    link.click();
  }

  async function onUpload(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    await uploadDataset(file);
    refresh();
  }

  return (
    <div className={`${theme === "dark" ? "dark" : ""} min-h-screen bg-slate-950 text-slate-100`}>
      <div className="fixed inset-0 -z-10 bg-[radial-gradient(circle_at_top_left,rgba(20,184,166,0.24),transparent_32%),radial-gradient(circle_at_80%_10%,rgba(249,115,22,0.16),transparent_30%),linear-gradient(135deg,#020617,#111827_48%,#171717)]" />
      <aside className="fixed left-0 top-0 hidden h-full w-20 border-r border-white/10 bg-slate-950/70 p-4 backdrop-blur-xl lg:block">
        <div className="grid h-12 w-12 place-items-center rounded-lg bg-teal-400 text-slate-950"><BrainCircuit /></div>
        <nav className="mt-10 grid gap-4">
          {[LineChart, WalletCards, Activity, Bot].map((Icon, index) => (
            <button key={index} className="grid h-11 w-11 place-items-center rounded-lg text-slate-400 transition hover:bg-white/10 hover:text-white"><Icon className="h-5 w-5" /></button>
          ))}
        </nav>
      </aside>

      <main ref={dashboardRef} className="mx-auto max-w-[1500px] px-4 py-5 lg:pl-28 lg:pr-8">
        <header className="flex flex-col gap-4 border-b border-white/10 pb-5 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="flex items-center gap-2 text-sm text-teal-200"><Sparkles className="h-4 w-4" /> AI Sales Intelligence Dashboard</p>
            <h1 className="mt-2 text-3xl font-semibold text-white md:text-5xl">InsightIQ</h1>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400">Executive retail analytics with interactive dashboards, local forecasting, CSV upload, and Gemini-powered business recommendations.</p>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <label className="grid h-11 w-11 cursor-pointer place-items-center rounded-lg border border-white/10 bg-white/5 transition hover:bg-white/10" title="Upload CSV">
              <Upload className="h-5 w-5" />
              <input type="file" accept=".csv" className="hidden" onChange={onUpload} />
            </label>
            <button onClick={exportScreenshot} className="grid h-11 w-11 place-items-center rounded-lg border border-white/10 bg-white/5 transition hover:bg-white/10" title="Download screenshot"><Download className="h-5 w-5" /></button>
            <button onClick={() => setTheme(theme === "dark" ? "light" : "dark")} className="grid h-11 w-11 place-items-center rounded-lg border border-white/10 bg-white/5 transition hover:bg-white/10" title="Toggle theme">{theme === "dark" ? <Moon className="h-5 w-5" /> : <Sun className="h-5 w-5" />}</button>
            <button onClick={refresh} className="grid h-11 w-11 place-items-center rounded-lg bg-teal-400 text-slate-950 transition hover:bg-teal-300" title="Refresh data"><RefreshCw className={`h-5 w-5 ${loading ? "animate-spin" : ""}`} /></button>
          </div>
        </header>

        <AnimatePresence>
          {loading && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="my-5 rounded-lg border border-teal-300/20 bg-teal-300/10 p-3 text-sm text-teal-100">
              Loading live analytics from Flask API...
            </motion.div>
          )}
        </AnimatePresence>

        <section className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <KpiCard icon={WalletCards} label="Total Sales" value={data.kpis.totalSales} tone="bg-teal-500/25" format="currency" />
          <KpiCard icon={Activity} label="Total Profit" value={data.kpis.totalProfit} tone="bg-emerald-500/25" format="currency" />
          <KpiCard icon={LineChart} label="Profit Margin" value={data.kpis.profitMargin} suffix="%" tone="bg-orange-500/25" />
          <KpiCard icon={Sparkles} label="Avg Order Value" value={data.kpis.averageOrderValue} tone="bg-violet-500/25" format="currency" />
          <KpiCard icon={WalletCards} label="Customers" value={data.kpis.customerCount} tone="bg-sky-500/25" />
          <KpiCard icon={Activity} label="Total Orders" value={data.kpis.totalOrders} tone="bg-rose-500/25" />
          <KpiCard icon={LineChart} label="Sales Growth" value={data.kpis.salesGrowth} suffix="%" tone="bg-lime-500/25" />
          <Card className="p-4">
            <p className="text-xs uppercase tracking-[0.18em] text-slate-400">3 Month Forecast</p>
            <p className="mt-2 text-2xl font-semibold text-white">{data.forecast.predictedGrowth}%</p>
            <p className="mt-2 text-sm text-slate-400">Predicted growth by final forecast month</p>
          </Card>
        </section>

        <section className="mt-6 grid gap-4 xl:grid-cols-2">
          <ChartCard title="Monthly Sales Trend" subtitle="Sales and profit trajectory">
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={data.charts.monthlyTrend}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
                <XAxis dataKey="month" stroke="#94a3b8" tick={{ fontSize: 11 }} />
                <YAxis stroke="#94a3b8" tickFormatter={(v) => number.format(v)} />
                <Tooltip contentStyle={{ background: "#020617", border: "1px solid rgba(255,255,255,.12)", borderRadius: 8 }} />
                <Legend />
                <Bar dataKey="profit" fill="#14b8a6" radius={[6, 6, 0, 0]} />
                <Line type="monotone" dataKey="sales" stroke="#f97316" strokeWidth={3} dot={false} />
              </ComposedChart>
            </ResponsiveContainer>
          </ChartCard>
          <ChartCard title="Region-wise Sales" subtitle="Revenue and profit by region">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.charts.regionSales}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
                <XAxis dataKey="Region" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" tickFormatter={(v) => number.format(v)} />
                <Tooltip contentStyle={{ background: "#020617", border: "1px solid rgba(255,255,255,.12)", borderRadius: 8 }} />
                <Legend />
                <Bar dataKey="sales" fill="#38bdf8" radius={[6, 6, 0, 0]} />
                <Bar dataKey="profit" fill="#22c55e" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
          <ChartCard title="Category Profit Mix" subtitle="Profit contribution by category">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={data.charts.categoryProfit} dataKey="profit" nameKey="Category" innerRadius={65} outerRadius={105} paddingAngle={3}>
                  {data.charts.categoryProfit.map((_, index) => <Cell key={index} fill={colors[index % colors.length]} />)}
                </Pie>
                <Tooltip contentStyle={{ background: "#020617", border: "1px solid rgba(255,255,255,.12)", borderRadius: 8 }} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </ChartCard>
          <ChartCard title="Profit vs Discount" subtitle="Sampled product-order margin behavior">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
                <XAxis type="number" dataKey="Discount" name="Discount" stroke="#94a3b8" />
                <YAxis type="number" dataKey="Profit" name="Profit" stroke="#94a3b8" />
                <Tooltip cursor={{ strokeDasharray: "3 3" }} contentStyle={{ background: "#020617", border: "1px solid rgba(255,255,255,.12)", borderRadius: 8 }} />
                <Scatter data={data.charts.discountScatter} fill="#a855f7" />
              </ScatterChart>
            </ResponsiveContainer>
          </ChartCard>
        </section>

        <section className="mt-6 grid gap-4 xl:grid-cols-[1.1fr_.9fr]">
          <ChartCard title="Top Products" subtitle="Searchable top 10 products by sales">
            <div className="mb-3 flex items-center gap-2 rounded-lg border border-white/10 bg-slate-950/60 px-3 py-2">
              <Search className="h-4 w-4 text-slate-500" />
              <input value={query} onChange={(event) => setQuery(event.target.value)} className="w-full bg-transparent text-sm text-white outline-none placeholder:text-slate-500" placeholder="Search products" />
            </div>
            <ResponsiveContainer width="100%" height="82%">
              <BarChart data={filteredProducts} layout="vertical" margin={{ left: 10, right: 10 }}>
                <XAxis type="number" stroke="#94a3b8" tickFormatter={(v) => number.format(v)} />
                <YAxis type="category" dataKey="product" stroke="#94a3b8" width={150} tick={{ fontSize: 10 }} />
                <Tooltip contentStyle={{ background: "#020617", border: "1px solid rgba(255,255,255,.12)", borderRadius: 8 }} />
                <Bar dataKey="sales" fill="#f97316" radius={[0, 6, 6, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
          <ChartCard title="State Sales Heatmap" subtitle="Highest-volume states">
            <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
              {data.charts.stateHeatmap.map((item, index) => (
                <div key={item.State} className="rounded-lg border border-white/10 p-3" style={{ backgroundColor: `rgba(20,184,166,${0.08 + Math.min(index, 10) * 0.018})` }}>
                  <p className="text-sm font-medium text-white">{item.State}</p>
                  <p className="mt-1 text-xs text-slate-300">{currency.format(item.sales)}</p>
                  <p className={`mt-1 text-xs ${item.profit >= 0 ? "text-emerald-300" : "text-rose-300"}`}>{currency.format(item.profit)}</p>
                </div>
              ))}
            </div>
          </ChartCard>
        </section>

        <section className="mt-6 grid gap-4 xl:grid-cols-[1.35fr_.65fr]">
          <ChartCard title="Forecasting" subtitle="Linear regression next 3 months">
            <ResponsiveContainer width="100%" height="100%">
              <ComposedChart data={[...data.forecast.history.map((d) => ({ ...d, type: "actual" })), ...data.forecast.forecast.map((d) => ({ month: d.month, sales: d.predictedSales, type: "forecast" }))]}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
                <XAxis dataKey="month" stroke="#94a3b8" tick={{ fontSize: 11 }} />
                <YAxis stroke="#94a3b8" tickFormatter={(v) => number.format(v)} />
                <Tooltip contentStyle={{ background: "#020617", border: "1px solid rgba(255,255,255,.12)", borderRadius: 8 }} />
                <Line type="monotone" dataKey="sales" stroke="#14b8a6" strokeWidth={3} dot />
              </ComposedChart>
            </ResponsiveContainer>
          </ChartCard>
          <ChartCard title="Customer Segment Analysis" subtitle="Segment revenue mix">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.charts.segmentAnalysis}>
                <XAxis dataKey="Segment" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" tickFormatter={(v) => number.format(v)} />
                <Tooltip contentStyle={{ background: "#020617", border: "1px solid rgba(255,255,255,.12)", borderRadius: 8 }} />
                <Bar dataKey="sales" fill="#a855f7" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        </section>

        <section className="mt-6">
          <div className="mb-4 flex items-center gap-3">
            <BrainCircuit className="h-5 w-5 text-teal-300" />
            <h2 className="text-xl font-semibold text-white">AI-Powered Business Insights</h2>
          </div>
          <InsightCards insights={data.insights} />
        </section>

        <section className="mt-6 grid gap-4 xl:grid-cols-[.95fr_1.05fr]">
          <Chatbot />
          <Card className="p-5">
            <h3 className="text-lg font-semibold text-white">Executive Recommendations</h3>
            <div className="mt-4 space-y-3">
              {[
                "Tighten high-discount approvals for products with repeated negative profit.",
                "Double down on top-region playbooks with targeted segment campaigns.",
                "Use forecast demand to align inventory before seasonal peaks.",
                "Build weekly exception reports for loss-making products and low-margin states."
              ].map((item) => (
                <div key={item} className="flex gap-3 rounded-lg border border-white/10 bg-white/[0.04] p-4">
                  <Sparkles className="mt-1 h-4 w-4 shrink-0 text-orange-300" />
                  <p className="text-sm leading-6 text-slate-300">{item}</p>
                </div>
              ))}
            </div>
          </Card>
        </section>
      </main>
    </div>
  );
}
