"use client";

import { useState, useTransition } from "react";
import { saveRiotId } from "@/app/actions";
import type { Profile } from "@/lib/types";

export default function RiotIdForm({ profile }: { profile: Profile }) {
  const [riotId, setRiotId] = useState(profile.riot_id ?? "");
  const [message, setMessage] = useState("");
  const [pending, startTransition] = useTransition();

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    startTransition(async () => {
      const res = await saveRiotId(riotId);
      setMessage(res.error ?? "Saved.");
    });
  }

  return (
    <section className="card">
      <h2 className="section-title" style={{ marginBottom: 12 }}>
        Your Riot ID
      </h2>
      <p className="muted" style={{ fontSize: 14, marginBottom: 16 }}>
        Link your League account so we can pull and analyze your match history.
      </p>

      <form onSubmit={onSubmit} style={{ display: "flex", gap: 10 }}>
        <input
          type="text"
          className="input"
          placeholder="summoner#TAG"
          value={riotId}
          onChange={(e) => setRiotId(e.target.value)}
          style={{ maxWidth: 360 }}
        />
        <button type="submit" className="btn btn--dark" disabled={pending}>
          {pending ? "Saving…" : "Save"}
        </button>
      </form>

      {message && (
        <p className="muted" style={{ marginTop: 12, fontSize: 13 }}>
          {message}
        </p>
      )}
    </section>
  );
}
