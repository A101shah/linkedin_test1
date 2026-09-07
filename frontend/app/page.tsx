"use client";

import { FormEvent, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

type Result = { type: "person" | "topic"; query: string; data: any[] };

export default function Home() {
  const [query, setQuery] = useState("");
  const [type, setType] = useState<"person" | "topic">("person");
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(e: FormEvent) {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true); setError(""); setResult(null);
    try {
      const res = await fetch(`${API}/api/search`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ query, type, limit: 10 }) });
      const job = await res.json();
      if (!res.ok) throw new Error(job.detail || "Request failed");
      const dataRes = await fetch(`${API}/api/results/${job.job_id}`);
      const data = await dataRes.json();
      if (!dataRes.ok) throw new Error(data.detail || "Result unavailable");
      setResult(data);
    } catch (err) { setError(err instanceof Error ? err.message : "Unexpected error"); }
    finally { setLoading(false); }
  }

  return <main className="shell">
    <nav className="nav"><div className="brand">LinkedIn Insight</div><div className="badge">EPHEMERAL DATA MODE</div></nav>
    <section className="hero">
      <div className="eyebrow">Data acquisition · API · analysis</div>
      <h1>Search. Inspect. Forget.</h1>
      <p>A full-stack LinkedIn data pipeline that retrieves only the requested result, exposes it through an API, and keeps the response in a short-lived TTL cache instead of building a permanent archive.</p>
      <form className="search" onSubmit={submit}>
        <input value={query} onChange={e => setQuery(e.target.value)} placeholder={type === "person" ? "Search a person…" : "Search a topic…"} />
        <button disabled={loading}>{loading ? "Loading…" : "Search"}</button>
      </form>
      <div className="tabs"><button className={type === "person" ? "active" : ""} onClick={() => setType("person")} type="button">Person</button><button className={type === "topic" ? "active" : ""} onClick={() => setType("topic")} type="button">Topic / posts</button></div>
    </section>
    <section className="panel">
      {error && <div className="error">{error}</div>}
      {!result && !error && <div className="notice">Demo mode is active. The UI and API are fully wired; connect an approved LinkedIn API integration to replace the sample acquisition layer with live permitted data.</div>}
      {result?.type === "person" && result.data.map((p: any) => <div className="grid" key={p.id}>
        <div className="card"><h2>{p.name}</h2><p>{p.headline}</p><p className="muted">{p.location}</p><p className="muted">{p.about}</p><a href={p.profile_url} target="_blank">Source ↗</a></div>
        <div className="card"><h3>Experience</h3>{p.experience?.map((x: any, i: number) => <p key={i}><b>{x.title}</b><br/><span className="muted">{x.company} · {x.start} – {x.end}</span></p>)}</div>
        <div className="card"><h3>Education</h3>{p.education?.map((x: any, i: number) => <p key={i}><b>{x.school}</b><br/><span className="muted">{x.degree}</span></p>)}<h3>Skills</h3>{p.skills?.map((x: string) => <span className="pill" key={x}>{x}</span>)}</div>
      </div>)}
      {result?.type === "topic" && <div className="grid">{result.data.map((p: any) => <article className="card" key={p.id}><h3>{p.topic}</h3><p>{p.text}</p><p className="muted">{p.author} · {new Date(p.posted_at).toLocaleString()}</p><span className="pill">{p.engagement.reactions} reactions</span><span className="pill">{p.engagement.comments} comments</span></article>)}</div>}
    </section>
  </main>;
}
