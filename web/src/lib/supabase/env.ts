// Central, loud failure for missing Supabase env vars.
//
// Next.js inlines NEXT_PUBLIC_* vars at BUILD time — but ONLY when they are
// referenced statically (e.g. `process.env.NEXT_PUBLIC_SUPABASE_URL`). A dynamic
// lookup like `process.env[name]` is NOT inlined and returns `undefined` at
// runtime in the Edge middleware and browser bundle. So every reference here is
// written out explicitly.

export function getSupabaseEnv() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const anonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (url === undefined) {
    throw new Error(
      'Missing environment variable "NEXT_PUBLIC_SUPABASE_URL". ' +
        "Set it in Vercel → Project → Settings → Environment Variables, " +
        'and make sure the "Production" scope is checked. Then redeploy.',
    );
  }
  if (url.trim() === "") {
    throw new Error(
      'Environment variable "NEXT_PUBLIC_SUPABASE_URL" is set but empty.',
    );
  }

  if (anonKey === undefined) {
    throw new Error(
      'Missing environment variable "NEXT_PUBLIC_SUPABASE_ANON_KEY". ' +
        "Set it in Vercel → Project → Settings → Environment Variables, " +
        'and make sure the "Production" scope is checked. Then redeploy.',
    );
  }
  if (anonKey.trim() === "") {
    throw new Error(
      'Environment variable "NEXT_PUBLIC_SUPABASE_ANON_KEY" is set but empty.',
    );
  }

  return { url, anonKey };
}
