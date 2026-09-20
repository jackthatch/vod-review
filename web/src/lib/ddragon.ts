// Data Dragon static asset URLs (Riot's CDN for champion/item icons).
// `championName` from the Riot API is already the DDragon key (e.g. "Graves",
// "MonkeyKing"), so it maps 1:1 to the icon filename.
//
// Bump VERSION occasionally — DDragon keeps old versions hosted, so only
// brand-new champions/items would 404 on a stale version.

const VERSION = "16.18.1";
const CDN = `https://ddragon.leagueoflegends.com/cdn/${VERSION}/img`;

export function championIcon(champion: string): string {
  return `${CDN}/champion/${champion}.png`;
}

export function itemIcon(itemId: number): string {
  return `${CDN}/item/${itemId}.png`;
}
