import type { Match } from "@/lib/types";

export default function MatchList({ matches }: { matches: Match[] }) {
  if (matches.length === 0) {
    return (
      <section className="card">
        <h2 className="section-title">Recent games</h2>
        <div className="empty-state">
          <p style={{ margin: 0 }}>
            No games processed yet. Once your Riot ID is saved and the backend
            runs, your analyzed matches will appear here.
          </p>
        </div>
      </section>
    );
  }

  return (
    <section>
      <h2 className="section-title">Recent games</h2>
      <div>
        {matches.map((m) => (
          <div key={m.id} className="match-row">
            <span className="match-champ">{m.champion}</span>
            <div className="match-meta">
              <span className="match-kda">{m.kda}</span>
              <span>{m.duration_min.toFixed(0)} min</span>
              <span className="mono">{m.role}</span>
            </div>
            <span className={`badge ${m.win ? "badge--win" : "badge--loss"}`}>
              {m.win ? "W" : "L"}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}
