import type { Match } from "@/lib/types";

export default function MatchList({ matches }: { matches: Match[] }) {
  if (matches.length === 0) {
    return (
      <section
        style={{ border: "1px solid #333", borderRadius: 8, padding: 16 }}
      >
        <h2 style={{ fontSize: 18, marginBottom: 8 }}>Recent games</h2>
        <p style={{ opacity: 0.6 }}>
          No games processed yet. The backend will fetch and analyze your matches
          once your Riot ID is saved.
        </p>
      </section>
    );
  }

  return (
    <section style={{ border: "1px solid #333", borderRadius: 8, padding: 16 }}>
      <h2 style={{ fontSize: 18, marginBottom: 12 }}>Recent games</h2>
      <div style={{ display: "grid", gap: 8 }}>
        {matches.map((m) => (
          <div
            key={m.id}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 12,
              padding: "10px 12px",
              borderRadius: 6,
              background: m.win ? "rgba(70,167,88,0.15)" : "rgba(229,72,77,0.15)",
            }}
          >
            <span style={{ fontWeight: 600 }}>{m.champion}</span>
            <span style={{ opacity: 0.7 }}>{m.kda}</span>
            <span style={{ opacity: 0.7 }}>{m.duration_min.toFixed(0)}min</span>
            <span style={{ marginLeft: "auto", fontWeight: 600 }}>
              {m.win ? "W" : "L"}
            </span>
          </div>
        ))}
      </div>
    </section>
  );
}
