// Central, loud failure for missing Supabase env vars.
//
// Next.js inlines NEXT_PUBLIC_* vars at BUILD time. If either is missing,
// @supabase/ssr throws a generic "URL and API key are required" error from
// deep in the stack. This helper throws instead, naming the exact variable
// (and whether it was unset vs. empty) so a failed build is self-diagnosing.

function requireEnv(name: string): string {
  const value = process.env[name];
  if (value === undefined) {
    throw new Error(
      `Missing environment variable "${name}". ` +
        `Set it in Vercel → Project → Settings → Environment Variables, ` +
        `and make sure the "Production" scope is checked. Then redeploy.`,
    );
  }
  if (value.trim() === "") {
    throw new Error(
      `Environment variable "${name}" is set but empty. ` +
        `Check Vercel → Settings → Environment Variables for a blank value.`,
    );
  }
  return value;
}

export function getSupabaseEnv() {
  return {
    url: requireEnv("NEXT_PUBLIC_SUPABASE_URL"),
    anonKey: requireEnv("NEXT_PUBLIC_SUPABASE_ANON_KEY"),
  };
}
