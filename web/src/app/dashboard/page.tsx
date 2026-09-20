import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";
import RiotIdForm from "@/components/RiotIdForm";
import MatchList from "@/components/MatchList";
import LogoutButton from "@/components/LogoutButton";
import type { Profile, Match } from "@/lib/types";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) {
    redirect("/login");
  }

  const { data: profile } = await supabase
    .from("profiles")
    .select("*")
    .eq("id", user.id)
    .single();

  const { data: matches } = await supabase
    .from("matches")
    .select("*")
    .eq("user_id", user.id)
    .order("fetched_at", { ascending: false })
    .limit(20);

  const p: Profile = profile ?? {
    id: user.id,
    email: user.email ?? null,
    riot_id: null,
    riot_name: null,
    riot_tag: null,
    riot_region: null,
  };

  return (
    <main style={{ maxWidth: 900, margin: "0 auto", padding: "24px 20px" }}>
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 24,
        }}
      >
        <h1>vod-review</h1>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <span style={{ opacity: 0.7 }}>{user.email}</span>
          <LogoutButton />
        </div>
      </header>

      <RiotIdForm profile={p} />

      <MatchList matches={(matches as Match[] | null) ?? []} />
    </main>
  );
}
