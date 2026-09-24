"use client";

import { useState, useTransition } from "react";
import { championIcon, itemIcon } from "@/lib/ddragon";
import { generateRecap } from "@/app/actions";
import type { Match, Participant } from "@/lib/types";

function fmtGold(n: number): string {
  return n.toLocaleString("en-US");
}

function kdaRatio(k: number, d: number, a: number): string {
  if (d === 0) return "Perfect";
  return `${((k + a) / d).toFixed(2)}:1`;
}

function fmtDuration(min: number): string {
  const total = Math.round(min * 60);
  const m = Math.floor(total / 60);
  const s = total % 60;
  return `${m}m ${s.toString().padStart(2, "0")}s`;
}

function ChampionIcon({
  champion,
  level,
  size = 48,
}: {
  champion: string;
  level?: number | null;
  size?: number;
}) {
  return (
    <div className="champ-icon" style={{ width: size, height: size }}>
      <img src={championIcon(champion)} alt={champion} loading="lazy" />
      {level != null && <span className="champ-icon__level">{level}</span>}
    </div>
  );
}

function MatchCard({
  match,
  selected,
  onSelect,
}: {
  match: Match;
  selected: boolean;
  onSelect: () => void;
}) {
  const d = match.detail;
  const kda = match.kda.split("/").map(Number);
  const [k, de, a] = [kda[0] ?? 0, kda[1] ?? 0, kda[2] ?? 0];

  return (
    <button
      className={`match-card ${match.win ? "match-card--win" : "match-card--loss"} ${
        selected ? "match-card--selected" : ""
      }`}
      onClick={onSelect}
    >
      <div className="match-card__result">
        <span>{match.win ? "W" : "L"}</span>
      </div>

      <ChampionIcon champion={match.champion} level={d?.level} size={52} />

      <div className="match-card__body">
        <div className="match-card__top">
          <span className="match-card__champ">{match.champion}</span>
          {d?.queue && <span className="match-card__queue">{d.queue}</span>}
        </div>
        <div className="match-card__kda">
          <span className="k">{k}</span>
          <span className="sep">/</span>
          <span className="d">{de}</span>
          <span className="sep">/</span>
          <span className="a">{a}</span>
          <span className="match-card__ratio">{kdaRatio(k, de, a)} KDA</span>
        </div>
        {d && (
          <div className="match-card__meta">
            <span>{d.cs} CS</span>
            <span>{fmtGold(d.gold)} gold</span>
          </div>
        )}
      </div>

      <div className="match-card__items">
        {d?.items?.map((id) => (
          <ItemIcon key={id} id={id} />
        ))}
        {d?.trinket && <ItemIcon id={d.trinket} trinket />}
      </div>

      <div className="match-card__right">
        <span className="match-card__duration">{fmtDuration(match.duration_min)}</span>
        <span className="match-card__verdict">{match.win ? "Victory" : "Defeat"}</span>
      </div>
    </button>
  );
}

function ItemIcon({
  id,
  trinket,
  size = 24,
}: {
  id: number;
  trinket?: boolean;
  size?: number;
}) {
  return (
    <img
      className={`item-icon ${trinket ? "item-icon--trinket" : ""}`}
      src={itemIcon(id)}
      alt=""
      loading="lazy"
      style={{ width: size, height: size }}
    />
  );
}

function ParticipantRow({ p }: { p: Participant }) {
  return (
    <div className={`participant-row ${p.is_me ? "participant-row--me" : ""}`}>
      <ChampionIcon champion={p.champion} size={30} />
      <div className="participant-row__info">
        <div className="participant-row__top">
          <span className="participant-row__name">{p.summoner || p.champion}</span>
          <span className="participant-row__kda">
            {p.kills}/{p.deaths}/{p.assists}
          </span>
        </div>
        {(p.items?.length > 0 || p.trinket) && (
          <div className="participant-row__items">
            {p.items?.map((id) => (
              <ItemIcon key={id} id={id} size={18} />
            ))}
            {p.trinket && <ItemIcon id={p.trinket} trinket size={18} />}
          </div>
        )}
      </div>
    </div>
  );
}

function ParticipantsPanel({ match }: { match: Match }) {
  const parts = match.detail?.participants ?? [];
  const me = parts.find((p) => p.is_me);
  const myTeam = me?.team;
  const mine = parts.filter((p) => p.team === myTeam);
  const enemy = parts.filter((p) => p.team !== myTeam);

  if (parts.length === 0) {
    return (
      <aside className="participants">
        <div className="participants__empty muted">Participant data not available yet.</div>
      </aside>
    );
  }

  return (
    <aside className="participants">
      <div className="participants__team">
        <span className={`team-label ${match.win ? "team-label--win" : "team-label--loss"}`}>
          {match.win ? "Victory" : "Defeat"}
        </span>
        {mine.map((p) => (
          <ParticipantRow key={p.participant_id} p={p} />
        ))}
      </div>
      <div className="participants__team">
        <span className="team-label">Enemy</span>
        {enemy.map((p) => (
          <ParticipantRow key={p.participant_id} p={p} />
        ))}
      </div>
    </aside>
  );
}

function renderInline(text: string): React.ReactNode[] {
  // Minimal **bold** support.
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((part, i) => {
    if (part.startsWith("**") && part.endsWith("**") && part.length > 4) {
      return <strong key={i}>{part.slice(2, -2)}</strong>;
    }
    return <span key={i}>{part}</span>;
  });
}

// Tiny, safe markdown renderer (no dangerouslySetInnerHTML). Handles the
// headings/bullets/bold the coach produces.
function Markdown({ text }: { text: string }) {
  const lines = text.split("\n");
  const out: React.ReactNode[] = [];
  let key = 0;
  let bullets: string[] = [];

  const flushBullets = () => {
    if (bullets.length) {
      out.push(
        <ul key={`ul-${key++}`}>
          {bullets.map((b, i) => (
            <li key={i}>{renderInline(b)}</li>
          ))}
        </ul>,
      );
      bullets = [];
    }
  };

  for (const raw of lines) {
    const line = raw.trim();
    if (line.startsWith("### ")) {
      flushBullets();
      out.push(<h4 key={`h-${key++}`}>{renderInline(line.slice(4))}</h4>);
    } else if (line.startsWith("## ")) {
      flushBullets();
      out.push(<h3 key={`h-${key++}`}>{renderInline(line.slice(3))}</h3>);
    } else if (line.startsWith("- ") || line.startsWith("* ")) {
      bullets.push(line.slice(2));
    } else if (line === "") {
      flushBullets();
    } else {
      flushBullets();
      out.push(<p key={`p-${key++}`}>{renderInline(line)}</p>);
    }
  }
  flushBullets();
  return <div className="markdown">{out}</div>;
}

function Spinner({ size = 16 }: { size?: number }) {
  return (
    <svg
      className="spinner"
      width={size}
      height={size}
      viewBox="0 0 24 24"
      role="status"
      aria-label="Loading"
    >
      <circle className="spinner__track" cx="12" cy="12" r="10" />
      <circle className="spinner__head" cx="12" cy="12" r="10" />
    </svg>
  );
}

function ReviewPanel({ match }: { match: Match }) {
  // State is initialized from the server-provided recap and reset on match
  // change via `key={match.id}` on the parent (remounts the component).
  const moments = match.moments ?? [];
  const [summary, setSummary] = useState<string | null>(match.summary ?? null);
  const [error, setError] = useState("");
  const [pending, startTransition] = useTransition();

  function onGenerate() {
    startTransition(async () => {
      const res = await generateRecap(match.id);
      if (res.error) {
        setError(res.error);
      } else if (res.summary) {
        setSummary(res.summary);
      }
    });
  }

  return (
    <section className="card review-panel">
      <div className="review-panel__head">
        <h3 className="section-title">AI recap</h3>
        {!summary && (
          <button
            className="btn btn--dark btn--small"
            onClick={onGenerate}
            disabled={pending}
          >
            {pending ? (
              <>
                <Spinner size={14} /> Generating…
              </>
            ) : (
              "Get AI recap"
            )}
          </button>
        )}
      </div>

      {pending && (
        <div
          className="progress"
          role="progressbar"
          aria-label="Generating recap"
        >
          <div className="progress__bar" />
        </div>
      )}

      {summary ? (
        <Markdown text={summary} />
      ) : pending ? (
        <div className="recap-loading">
          <Spinner size={20} />
          <span className="muted">Analyzing this game… usually 10–20s.</span>
        </div>
      ) : (
        <p className="muted">
          Generate an AI recap for this game. It&rsquo;s saved once generated.
        </p>
      )}

      {error && <p className="review-panel__error">{error}</p>}

      {moments.length > 0 && (
        <>
          <h4 className="review-panel__subtitle">Flagged moments</h4>
          <ul className="review-panel__moments">
            {moments.map((m, i) => (
              <li key={i}>
                <span className="moment-time">{m.min}min</span>{" "}
                <span className="moment-type">{m.type}</span> — {m.detail}
              </li>
            ))}
          </ul>
        </>
      )}
    </section>
  );
}

export default function MatchList({ matches }: { matches: Match[] }) {
  const [selectedId, setSelectedId] = useState<string | null>(matches[0]?.id ?? null);
  const selected = matches.find((m) => m.id === selectedId) ?? matches[0];

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
      <div className="match-layout">
        <div className="match-list">
          {matches.map((m) => (
            <MatchCard
              key={m.id}
              match={m}
              selected={m.id === selected?.id}
              onSelect={() => setSelectedId(m.id)}
            />
          ))}
        </div>
        <div className="match-side">
          {selected && <ReviewPanel key={selected.id} match={selected} />}
          {selected && <ParticipantsPanel match={selected} />}
        </div>
      </div>
    </section>
  );
}
