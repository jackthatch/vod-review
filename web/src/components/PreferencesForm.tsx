"use client";

import { useState, useTransition } from "react";
import { savePreferences } from "@/app/actions";
import type { Preferences } from "@/lib/types";

const ROLES = ["JUNGLE", "TOP", "MIDDLE", "BOTTOM", "UTILITY"];

// Suggested comparison targets (mirrors pros.json roster).
const PRO_ROSTER = ["Kanavi", "Canyon", "Sheiden"];

export default function PreferencesForm({ prefs }: { prefs: Preferences }) {
  const [role, setRole] = useState(prefs.role);
  const [champions, setChampions] = useState(prefs.main_champions.join(", "));
  const [targets, setTargets] = useState<string[]>(
    prefs.comparison_targets.length ? prefs.comparison_targets : [],
  );
  const [overstay, setOverstay] = useState(prefs.overstay_gold);
  const [range, setRange] = useState(prefs.contest_range);
  const [windowSec, setWindowSec] = useState(prefs.objective_window);
  const [gapMin, setGapMin] = useState(prefs.spike_gap_min);
  const [message, setMessage] = useState("");
  const [pending, startTransition] = useTransition();

  function toggleTarget(name: string) {
    setTargets((prev) =>
      prev.includes(name) ? prev.filter((t) => t !== name) : [...prev, name],
    );
  }

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    const championsArr = champions
      .split(",")
      .map((c) => c.trim())
      .filter(Boolean);
    startTransition(async () => {
      const res = await savePreferences({
        role,
        main_champions: championsArr,
        comparison_targets: targets,
        overstay_gold: overstay,
        contest_range: range,
        objective_window: windowSec,
        spike_gap_min: gapMin,
      });
      setMessage(res.error ?? "Preferences saved.");
    });
  }

  const fieldStyle = { padding: 8, fontSize: 15, borderRadius: 6, border: "1px solid #444" };
  const labelStyle = { display: "grid", gap: 4, fontSize: 14 } as const;

  return (
    <section
      style={{ border: "1px solid #333", borderRadius: 8, padding: 16, marginBottom: 24 }}
    >
      <h2 style={{ fontSize: 18, marginBottom: 12 }}>Preferences</h2>

      <form onSubmit={onSubmit} style={{ display: "grid", gap: 16 }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
          <label style={labelStyle}>
            Role
            <select value={role} onChange={(e) => setRole(e.target.value)} style={fieldStyle}>
              {ROLES.map((r) => (
                <option key={r} value={r}>
                  {r}
                </option>
              ))}
            </select>
          </label>

          <label style={labelStyle}>
            Main champions (comma-separated)
            <input
              type="text"
              value={champions}
              onChange={(e) => setChampions(e.target.value)}
              placeholder="Graves, Sejuani"
              style={fieldStyle}
            />
          </label>
        </div>

        <div>
          <p style={{ fontSize: 14, marginBottom: 6 }}>Compare against</p>
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
            {PRO_ROSTER.map((name) => (
              <button
                key={name}
                type="button"
                onClick={() => toggleTarget(name)}
                style={{
                  padding: "6px 12px",
                  borderRadius: 999,
                  cursor: "pointer",
                  border: "1px solid #444",
                  background: targets.includes(name) ? "#46a758" : "transparent",
                  color: targets.includes(name) ? "#fff" : "inherit",
                }}
              >
                {name}
              </button>
            ))}
          </div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12 }}>
          <label style={labelStyle}>
            Overstay gold
            <input
              type="number"
              value={overstay}
              onChange={(e) => setOverstay(Number(e.target.value))}
              style={fieldStyle}
            />
          </label>
          <label style={labelStyle}>
            Contest range
            <input
              type="number"
              value={range}
              onChange={(e) => setRange(Number(e.target.value))}
              style={fieldStyle}
            />
          </label>
          <label style={labelStyle}>
            Objective window (s)
            <input
              type="number"
              value={windowSec}
              onChange={(e) => setWindowSec(Number(e.target.value))}
              style={fieldStyle}
            />
          </label>
          <label style={labelStyle}>
            Spike gap (min)
            <input
              type="number"
              step="0.5"
              value={gapMin}
              onChange={(e) => setGapMin(Number(e.target.value))}
              style={fieldStyle}
            />
          </label>
        </div>

        <button
          type="submit"
          disabled={pending}
          style={{ padding: "10px 16px", fontSize: 16, borderRadius: 6, cursor: "pointer" }}
        >
          {pending ? "Saving…" : "Save preferences"}
        </button>
      </form>

      {message && <p style={{ marginTop: 12, opacity: 0.7 }}>{message}</p>}
    </section>
  );
}
