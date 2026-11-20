import React, { useEffect, useMemo, useState } from "react";
import axios from "axios";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { TableBlock } from "../components/runtime/TableBlock";
import { FormBlock } from "../components/runtime/FormBlock";
import { BarChartComponent } from "../components/charts/BarChartComponent";
import { backendUrl } from "../components/runtime/bindingData";
import { useDataVersion } from "../components/runtime/dataVersion";

type Category = "Book" | "Film" | "Place" | "Article" | "Restaurant" | "Podcast" | "Product" | "Recipe" | "App" | "Other";
type Status = "ToTry" | "Done" | "Dropped";
type RecordItem = { id: number; title: string; category: Category; status: Status; note: string | null; added_on: string };
const categories: Category[] = ["Book", "Film", "Place", "Article", "Restaurant", "Podcast", "Product", "Recipe", "App", "Other"];
const statuses: Status[] = ["ToTry", "Done", "Dropped"];
const categoryIcons: Record<Category, string> = { Book: "📚", Film: "🎬", Place: "📍", Article: "📰", Restaurant: "🍽️", Podcast: "🎙️", Product: "🎁", Recipe: "🍲", App: "📱", Other: "✨" };
const categoryColors: Record<Category, string> = { Book: "var(--tracker-indigo)", Film: "var(--tracker-sky)", Place: "var(--tracker-teal)", Article: "var(--tracker-amber)", Restaurant: "var(--tracker-violet)", Podcast: "var(--tracker-coral)", Product: "var(--tracker-slate)", Recipe: "var(--tracker-coral)", App: "var(--tracker-sky)", Other: "var(--tracker-slate)" };
const tableOptions = {
  showHeader: true, stripedRows: false, showPagination: true, rowsPerPage: 5,
  actionButtons: true, hideCreateButton: true,
  columns: [
    { label: "Title", column_type: "field", field: "title", type: "str", required: true },
    { label: "Category", column_type: "field", field: "category", type: "enum", options: categories, required: true },
    { label: "Status", column_type: "field", field: "status", type: "enum", options: statuses, required: true },
    { label: "Note", column_type: "field", field: "note", type: "str", required: false },
    { label: "Added on", column_type: "field", field: "added_on", type: "date", required: true },
  ],
  formColumns: [
    { label: "Title", column_type: "field", field: "title", type: "str", required: true },
    { label: "Category", column_type: "field", field: "category", type: "enum", options: categories, required: true },
    { label: "Status", column_type: "field", field: "status", type: "enum", options: statuses, required: true },
    { label: "Note", column_type: "field", field: "note", type: "str", required: false },
    { label: "Added on", column_type: "field", field: "added_on", type: "date", required: true },
  ],
};

const useRecommendations = () => {
  const [rows, setRows] = useState<RecordItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const version = useDataVersion();
  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    axios.get<RecordItem[]>(backendUrl("/recommendation/"))
      .then(({ data }) => { if (active) setRows(data); })
      .catch(() => { if (active) setError("Could not load recommendations. Please try again."); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [version]);
  return { rows, loading, error };
};

const Recommendation: React.FC<{ view?: "home" | "list" | "add" }> = ({ view = "list" }) => {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const category = searchParams.get("category") || "";
  const [status, setStatus] = useState("");
  const { rows, loading, error } = useRecommendations();
  const chartData = useMemo(() => categories.map(name => ({ name, count: rows.filter(row => row.category === name).length })), [rows]);
  const recent = useMemo(() => [...rows].sort((a, b) => b.added_on.localeCompare(a.added_on) || b.id - a.id).slice(0, 5), [rows]);
  const filtered = useMemo(() => (row: RecordItem) => (!category || row.category === category) && (!status || row.status === status), [category, status]);
  return (
    <div id="page-recommendation-0" className="ds-page">
      <div id="iba7" className="tracker-page">
        <main id="i8s4f" className="ds-container tracker-main">
          {view === "home" ? <>
            <header className="ds-hero tracker-hero">
              <div className="tracker-hero-content">
                <div><h1 className="ds-heading">Recommendations Tracker</h1><p>All your recommendations, organised by type</p>
                  <div className="tracker-total"><strong>{loading ? "…" : rows.length}</strong><span>Total recommendations</span></div>
                </div>
                <Link className="ds-btn ds-btn-primary tracker-hero-action" to="/recommendation/new">Add recommendation</Link>
              </div>
            </header>
            {error && <p className="ds-notice" role="alert">{error}</p>}
            <section className="tracker-section" aria-labelledby="category-heading">
              <div className="tracker-section-heading"><h2 id="category-heading" className="ds-heading">Browse by category</h2><p>Find the ideas you saved for later.</p></div>
              {loading ? <p className="ds-notice" role="status">Loading categories…</p> : error ? <p className="ds-notice" role="alert">Categories are unavailable right now.</p> : <div className="tracker-category-grid">
                {categories.map(name => { const matching = rows.filter(row => row.category === name); return (
                  <Link key={name} className="ds-card tracker-category-card" to={`/recommendation?category=${encodeURIComponent(name)}`}>
                    <span className="tracker-category-icon" aria-hidden="true">{categoryIcons[name]}</span>
                    <h3>{name}</h3><strong className="tracker-category-count">{matching.length}</strong>
                    <span className="tracker-muted">{matching.length === 1 ? "recommendation" : "recommendations"}</span>
                    <div className="tracker-card-stats"><span>To try <b>{matching.filter(row => row.status === "ToTry").length}</b></span><span>Done <b>{matching.filter(row => row.status === "Done").length}</b></span></div>
                  </Link>
                ); })}
              </div>}
            </section>
            <section className="tracker-section" aria-labelledby="recent-heading"><div className="tracker-section-heading"><h2 id="recent-heading" className="ds-heading">Recently added</h2><p>The latest additions to your collection.</p></div>
              <div className="ds-card">{loading ? <p className="ds-notice" role="status">Loading recommendations…</p> : error ? <p className="ds-notice" role="alert">Recently added recommendations are unavailable right now.</p> : recent.length ? <ul className="tracker-recent-list">{recent.map(row => <li key={row.id}><strong>{row.title}</strong><span className="ds-badge">{row.category}</span><time dateTime={row.added_on}>{row.added_on}</time></li>)}</ul> : <p className="tracker-muted">Nothing here yet. Add your first recommendation to get started!</p>}</div>
            </section>
            <section className="tracker-section" aria-labelledby="distribution-heading"><div className="ds-card"><h2 id="distribution-heading" className="ds-heading">Distribution by category</h2>
              {loading ? <p className="ds-notice" role="status">Loading chart…</p> : error ? <p className="ds-notice" role="alert">Chart data is unavailable right now.</p> : <BarChartComponent id="recommendation-distribution" data={chartData} labelField="name" dataField="count" options={{ orientation: "vertical", showLegend: false, integerTicks: true, categoryColors, valueLabels: true }} />}
            </div></section>
          </> : view === "add" ? <section className="tracker-section tracker-form-section"><h1 className="ds-heading">Add recommendation</h1><p className="tracker-muted">Keep a new recommendation in one place.</p>
            <FormBlock id="add-recommendation-form" className="ds-card tracker-form" endpoint="/recommendation/" entity="Recommendation" submitLabel="Save" submitClassName="ds-btn ds-btn-primary" onSaved={() => navigate("/recommendation")} fields={[
              { name: "title", field: "title", type: "str" }, { name: "category", field: "category", type: "enum" }, { name: "status", field: "status", type: "enum" }, { name: "note", field: "note", type: "str" }, { name: "added_on", field: "added_on", type: "date" },
            ]}>
              <div className="ds-field"><label className="ds-label" htmlFor="rec-title">Title</label><input className="ds-input" id="rec-title" name="title" type="text" required maxLength={100} /></div>
              <div className="ds-grid-2"><div className="ds-field"><label className="ds-label" htmlFor="rec-category">Category</label><select className="ds-input" id="rec-category" name="category" required defaultValue=""><option value="" disabled>Select a category</option>{categories.map(item => <option key={item} value={item}>{item}</option>)}</select></div>
              <div className="ds-field"><label className="ds-label" htmlFor="rec-status">Status</label><select className="ds-input" id="rec-status" name="status" required defaultValue=""><option value="" disabled>Select a status</option>{statuses.map(item => <option key={item} value={item}>{item === "ToTry" ? "To try" : item}</option>)}</select></div></div>
              <div className="ds-field"><label className="ds-label" htmlFor="rec-note">Note (optional)</label><textarea className="ds-input" id="rec-note" name="note" rows={4} maxLength={100} /></div>
              <div className="ds-field"><label className="ds-label" htmlFor="rec-date">Added on</label><input className="ds-input" id="rec-date" name="added_on" type="date" required /></div>
            </FormBlock>
          </section> : <section className="tracker-section"><div className="tracker-list-heading"><div><h1 id="iwr1h" className="ds-heading">Recommendations</h1><p id="ifus2" className="tracker-muted">Browse, sort and manage everything you’ve saved.</p></div><Link className="ds-btn ds-btn-primary" to="/recommendation/new">Add recommendation</Link></div>
            <div className="ds-card tracker-filter-panel"><div className="ds-field"><label className="ds-label" htmlFor="filter-category">Category</label><select className="ds-input" id="filter-category" value={category} onChange={event => setSearchParams(event.target.value ? { category: event.target.value } : {})}><option value="">All categories</option>{categories.map(item => <option key={item} value={item}>{item}</option>)}</select></div>
              <div className="ds-field"><label className="ds-label" htmlFor="filter-status">Status</label><select className="ds-input" id="filter-status" value={status} onChange={event => setStatus(event.target.value)}><option value="">All statuses</option>{statuses.map(item => <option key={item} value={item}>{item === "ToTry" ? "To try" : item}</option>)}</select></div></div>
            <TableBlock id="table-recommendation-0" className="has-data-binding tracker-table" title="Recommendation list" options={tableOptions} filter={filtered} dataBinding={{ entity: "Recommendation", endpoint: "/recommendation/", row_key_fields: ["id"] }} />
          </section>}
        </main>
      </div>
    </div>
  );
};

export default Recommendation;

