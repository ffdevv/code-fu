export function sleep(ms = null, powTenMs = 2) {
  ms ??= Math.random() * 10 ** powTenMs;
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function pickRandom(items) {
  return items[Math.floor(Math.random() * items.length)];
}
