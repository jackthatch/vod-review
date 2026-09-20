// Central, loud failure for missing Supabase env vars.
//
// These are SERVER-SIDE only. After the server-action refactor, no Supabase
// value is ever read in the browser, so the vars are plain (no NEXT_PUBLIC_
// prefix) and are injected by Vercel at runtime into server components, server
// actions, and the Edge proxy. References are written out explicitly so the
// failure message names the exact missing variable.

export function getSupabaseEnv() {
  const url = process.env.SUPABASE_URL;
  const anonKey = process.env.SUPABASE_ANON_KEY;

  if (url === undefined) {
    throw new Error(
      'Missing environment variable "SUPABASE_URL". ' +
        "Set it in Vercel → Project → Settings → Environment Variables " +
        "(as a Secret, not NEXT_PUBLIC_). Then redeploy.",
    );
  }
  if (url.trim() === "") {
    throw new Error('Environment variable "SUPABASE_URL" is set but empty.');
  }

  if (anonKey === undefined) {
    throw new Error(
      'Missing environment variable "SUPABASE_ANON_KEY". ' +
        "Set it in Vercel → Project → Settings → Environment Variables " +
        "(as a Secret, not NEXT_PUBLIC_). Then redeploy.",
    );
  }
  if (anonKey.trim() === "") {
    throw new Error('Environment variable "SUPABASE_ANON_KEY" is set but empty.');
  }

  return { url, anonKey };
}
