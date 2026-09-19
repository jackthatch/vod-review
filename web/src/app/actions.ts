"use server";

import { createClient } from "@/lib/supabase/server";
import { revalidatePath } from "next/cache";
import type { Preferences } from "@/lib/types";

export async function savePreferences(input: Preferences) {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) {
    return { error: "Not authenticated" };
  }

  const { error } = await supabase
    .from("preferences")
    .upsert({ id: user.id, ...input, updated_at: new Date().toISOString() });

  if (error) {
    return { error: error.message };
  }

  revalidatePath("/dashboard");
  return { ok: true };
}

export async function saveRiotId(riotId: string) {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) {
    return { error: "Not authenticated" };
  }

  // Parse "name#TAG" into its parts.
  let name = riotId.trim();
  let tag = "";
  const hash = name.indexOf("#");
  if (hash !== -1) {
    tag = name.slice(hash + 1).trim();
    name = name.slice(0, hash).trim();
  }

  const { error } = await supabase
    .from("profiles")
    .upsert({
      id: user.id,
      riot_id: riotId.trim() || null,
      riot_name: name || null,
      riot_tag: tag || null,
      updated_at: new Date().toISOString(),
    });

  if (error) {
    return { error: error.message };
  }

  revalidatePath("/dashboard");
  return { ok: true };
}
