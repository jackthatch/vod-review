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
    <section
      style={{
        border: "1px solid #333",
        borderRadius: 8,
        padding: 16,
        marginBottom: 24,
      }}
    >
      <h2 style={{ fontSize: 18, marginBottom: 8 }}>Your Riot ID</h2>
      <form onSubmit={onSubmit} style={{ display: "flex", gap: 8 }}>
        <input
          type="text"
          placeholder="summoner#TAG"
          value={riotId}
          onChange={(e) => setRiotId(e.target.value)}
          style={{ flex: 1, padding: 10, fontSize: 16, borderRadius: 6, border: "1px solid #444" }}
        />
        <button
          type="submit"
          disabled={pending}
          style={{ padding: "10px 16px", fontSize: 16, borderRadius: 6, cursor: "pointer" }}
        >
          {pending ? "Saving…" : "Save"}
        </button>
      </form>
      {message && <p style={{ marginTop: 8, opacity: 0.7 }}>{message}</p>}
    </section>
  );
}
