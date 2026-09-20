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
    <>
      <nav className="nav">
        <div className="nav__inner">
          <a className="wordmark" href="/dashboard">
            vod-review
          </a>
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <span className="muted" style={{ fontSize: 14 }}>
              {user.email}
            </span>
            <LogoutButton />
          </div>
        </div>
      </nav>

      <main className="container">
        <RiotIdForm profile={p} />
        <MatchList matches={(matches as Match[] | null) ?? []} />
      </main>
    </>
  );
}
