// riot.ts — Riot Games API client (server-side only).
//
// Ports the `Riot` class from fetch_match.py. Uses native fetch + the
// X-Riot-Token header, with Retry-After backoff on 429 rate limits.
//
// match-v5 uses regional routing; summoner-v4 uses platform routing. We only
// talk to account-v1 (regional) and match-v5 (regional) here, so `regionHost`
// is what matters for our calls — `platformHost` is kept for parity/future use.

import type { RiotMatch, RiotTimeline } from "@/lib/riot-types";

export const REGION_ROUTING: Record<string, string> = {
  na1: "americas",
  br1: "americas",
  la1: "americas",
  la2: "americas",
  oc1: "americas",
  euw1: "europe",
  eun1: "europe",
  tr1: "europe",
  ru: "europe",
  kr: "asia",
  jp1: "asia",
  sg2: "sea",
  tw2: "sea",
  vn2: "sea",
  ph2: "sea",
};

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

export class Riot {
  private key: string;
  private platform: string;
  private region: string;
  private platformHost: string;
  private regionHost: string;

  constructor(apiKey: string, region: string) {
    this.key = apiKey;
    this.platform = region;
    this.region = REGION_ROUTING[region] ?? region;
    this.platformHost = `https://${this.platform}.api.riotgames.com`;
    this.regionHost = `https://${this.region}.api.riotgames.com`;
  }

  /** Reconfigure routing for a platform region (e.g. 'na1', 'kr'). */
  setRegion(region: string): void {
    this.platform = region;
    this.region = REGION_ROUTING[region] ?? region;
    this.platformHost = `https://${this.platform}.api.riotgames.com`;
    this.regionHost = `https://${this.region}.api.riotgames.com`;
  }

  private async get<T>(host: string, path: string): Promise<T> {
    const res = await fetch(`${host}${path}`, {
      headers: { "X-Riot-Token": this.key },
      cache: "no-store",
    });

    // Rate limit — honor Retry-After and retry (mirrors fetch_match.py).
    if (res.status === 429) {
      const retryAfter = parseInt(res.headers.get("Retry-After") ?? "1", 10);
      await sleep((Number.isFinite(retryAfter) ? retryAfter : 1) * 1000);
      return this.get<T>(host, path);
    }

    if (!res.ok) {
      const body = await res.text().catch(() => "");
      throw new Error(`Riot API ${res.status}: ${body.slice(0, 300)}`);
    }

    return (await res.json()) as T;
  }

  async puuid(name: string, tag: string): Promise<string> {
    if (name.includes("#")) {
      const idx = name.indexOf("#");
      tag = name.slice(idx + 1);
      name = name.slice(0, idx);
    }
    const p = await this.get<{ puuid: string }>(
      this.regionHost,
      `/riot/account/v1/accounts/by-riot-id/${encodeURIComponent(name)}/${encodeURIComponent(tag)}`,
    );
    return p.puuid;
  }

  async matchIds(puuid: string, count: number): Promise<string[]> {
    return this.get<string[]>(
      this.regionHost,
      `/lol/match/v5/matches/by-puuid/${puuid}/ids?start=0&count=${count}`,
    );
  }

  async match(matchId: string): Promise<RiotMatch> {
    return this.get<RiotMatch>(
      this.regionHost,
      `/lol/match/v5/matches/${matchId}`,
    );
  }

  async timeline(matchId: string): Promise<RiotTimeline> {
    return this.get<RiotTimeline>(
      this.regionHost,
      `/lol/match/v5/matches/${matchId}/timeline`,
    );
  }
}
