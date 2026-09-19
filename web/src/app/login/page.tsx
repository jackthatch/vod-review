"use client";

import { useState } from "react";
import { createClient } from "@/lib/supabase/client";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "sent" | "error">("idle");
  const [message, setMessage] = useState("");
  const router = useRouter();
  const supabase = createClient();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("idle");
    setMessage("");

    const { error } = await supabase.auth.signInWithOtp({
      email,
      options: {
        emailRedirectTo: `${window.location.origin}/auth/callback`,
      },
    });

    if (error) {
      setStatus("error");
      setMessage(error.message);
      return;
    }

    setStatus("sent");
    setMessage("Check your email for a magic link.");
    router.refresh();
  }

  return (
    <main style={{ maxWidth: 420, margin: "80px auto", padding: "0 20px" }}>
      <h1>vod-review</h1>
      <p style={{ color: "var(--foreground)", opacity: 0.7 }}>
        Log in with your email — we&apos;ll send a magic link.
      </p>

      <form onSubmit={handleSubmit} style={{ display: "grid", gap: 12, marginTop: 20 }}>
        <input
          type="email"
          required
          placeholder="you@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{ padding: 10, fontSize: 16, borderRadius: 6, border: "1px solid #444" }}
        />
        <button
          type="submit"
          disabled={status === "sent"}
          style={{ padding: 12, fontSize: 16, borderRadius: 6, cursor: "pointer" }}
        >
          {status === "sent" ? "Sent — check your inbox" : "Send magic link"}
        </button>
      </form>

      {message && (
        <p style={{ marginTop: 16, color: status === "error" ? "#e5484d" : "#46a758" }}>
          {message}
        </p>
      )}
    </main>
  );
}
