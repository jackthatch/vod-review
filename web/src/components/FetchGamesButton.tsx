"use client";

import { useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import { fetchAndAnalyze } from "@/app/actions";

export default function FetchGamesButton() {
  const [message, setMessage] = useState("");
  const [pending, startTransition] = useTransition();
  const router = useRouter();

  function onClick() {
    startTransition(async () => {
      const res = await fetchAndAnalyze(3);
      if (res.error) {
        setMessage(res.error);
      } else {
        const n = res.count ?? 0;
        setMessage(n > 0 ? `Fetched ${n} game${n === 1 ? "" : "s"}.` : "No new games.");
        router.refresh(); // re-run the dashboard server component
      }
    });
  }

  return (
    <section className="card" style={{ display: "flex", alignItems: "center", gap: 12 }}>
      <button className="btn btn--dark" onClick={onClick} disabled={pending}>
        {pending ? "Fetching…" : "Fetch latest games"}
      </button>
      {message && (
        <span className="muted" style={{ fontSize: 13 }}>
          {message}
        </span>
      )}
    </section>
  );
}
