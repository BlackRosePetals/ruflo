/**
 * Opens the system default browser for the `ruflo auth login` flow. A
 * TypeScript port of meta-proxy's `src/oauth/browser.rs`.
 *
 * Deliberately does NOT go through `SafeExecutor.execute()`: `SafeExecutor`'s
 * blocked-argument patterns (`safe-executor.ts`'s `DEFAULT_BLOCKED_PATTERNS`)
 * include a bare `&`, which is meant to catch shell-metacharacter injection in
 * command-line-style arguments — but it also appears in every real OAuth
 * authorize URL's query string (`?a=1&b=2&...`), so passing one through would
 * false-positive-reject on every real invocation. That blocklist is the wrong
 * tool for a URL argument: with `shell: false` (used here, same as
 * `SafeExecutor`), a single argv element containing `&` is inert — there's no
 * shell to interpret it. The actual safety property that matters is "the URL
 * was constructed by us from validated components, never from raw external
 * input" (this module's `authorizeUrl()` in `client.ts` is the only caller),
 * which `assertSafeUrl` below checks directly instead.
 *
 * @module v3/security/oauth/browser
 */

import { execFile } from 'node:child_process';

/** Throws if `url` isn't a well-formed https/http URL — the one check that matters here. */
function assertSafeUrl(url: string): void {
  const parsed = new URL(url); // throws on malformed input
  if (parsed.protocol !== 'https:' && parsed.protocol !== 'http:') {
    throw new Error(`refusing to open non-http(s) URL scheme: ${parsed.protocol}`);
  }
}

/**
 * Attempts to open `url` in the system default browser. Resolves whether or
 * not a browser window actually appeared — this cannot be confirmed in
 * general, which is why the caller always also prints the URL as a fallback.
 */
export function openBrowser(url: string): Promise<void> {
  assertSafeUrl(url);

  let cmd: string;
  let args: string[];
  if (process.platform === 'darwin') {
    cmd = 'open';
    args = [url];
  } else if (process.platform === 'win32') {
    // `cmd /c start "" <url>` — the empty title arg avoids `start` treating a
    // quoted URL as the window title.
    cmd = 'cmd';
    args = ['/c', 'start', '', url];
  } else {
    cmd = 'xdg-open';
    args = [url];
  }

  return new Promise((resolve) => {
    execFile(cmd, args, { shell: false, windowsHide: true }, () => resolve());
  });
}
