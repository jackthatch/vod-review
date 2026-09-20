"use client";

import { useState, useTransition } from "react";
import { signInWithEmail } from "@/app/actions";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "sent" | "error">("idle");
  const [message, setMessage] = useState("");
  const [pending, startTransition] = useTransition();

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("idle");
    setMessage("");
    startTransition(async () => {
      const res = await signInWithEmail(email, window.location.origin);
      if (res.error) {
        setStatus("error");
        setMessage(res.error);
        return;
      }
      setStatus("sent");
      setMessage("Check your email for a magic link.");
    });
  }

  return (
    <main className="auth-hero">
      <div className="auth-card">
        <h1 className="auth-title">vod-review</h1>
        <p className="auth-sub">
          AI VOD review for League of Legends. Enter your email and we&apos;ll send
          a magic link — no password.
        </p>

        <form onSubmit={handleSubmit} style={{ display: "grid", gap: 16, marginTop: 8 }}>
          <label className="label">
            Email
            <input
              type="email"
              required
              className="input"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </label>

          <button
            type="submit"
            className="btn btn--dark"
            disabled={pending || status === "sent"}
            style={{ width: "100%", padding: "14px 20px", fontSize: 16 }}
          >
            {status === "sent"
              ? "Sent — check your inbox"
              : pending
                ? "Sending…"
                : "Send magic link"}
          </button>
        </form>

        {message && (
          <p
            style={{
              marginTop: 16,
              fontSize: 14,
              color: status === "error" ? "var(--loss)" : "var(--win)",
            }}
          >
            {message}
          </p>
        )}
      </div>
    </main>
  );
}
