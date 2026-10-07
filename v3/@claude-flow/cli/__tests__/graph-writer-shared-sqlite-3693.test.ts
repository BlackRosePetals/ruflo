/**
 * #3693: a CLI-owned better-sqlite3 handle opened through a DIFFERENT installed
 * copy than AgentDB's must not delete the -wal/-shm sidecars of a live AgentDB
 * handle when the graph writer's idle release closes it.
 *
 * Deterministic: real native modules (a second copy of the built binary is
 * placed in a temp "agentdb" tree), fake timers drive the idle close.
 */
import { afterAll, afterEach, beforeAll, describe, expect, it, vi } from 'vitest';
import { createRequire } from 'node:module';
import { cpSync, existsSync, mkdirSync, mkdtempSync, rmSync, statSync, symlinkSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { tmpdir } from 'node:os';

const req = createRequire(import.meta.url);
const root = mkdtempSync(join(tmpdir(), 'ruflo-3693-'));
const agentdbDir = join(root, 'node_modules', 'agentdb');
const agentdbEntry = join(agentdbDir, 'index.js');
let HolderCtor: any;
let native = true;

beforeAll(() => {
  try {
    const pkgDir = dirname(req.resolve('better-sqlite3/package.json'));
    const nm = join(agentdbDir, 'node_modules');
    mkdirSync(nm, { recursive: true });
    writeFileSync(agentdbEntry, '');
    cpSync(pkgDir, join(nm, 'better-sqlite3'), { recursive: true });
    for (const dep of ['bindings', 'file-uri-to-path']) {
      try { symlinkSync(dirname(req.resolve(`${dep}/package.json`)), join(nm, dep)); } catch { /* optional */ }
    }
    HolderCtor = createRequire(agentdbEntry)('better-sqlite3');
    const probe = new HolderCtor(':memory:'); probe.close();
  } catch { native = false; }
});

afterEach(() => { vi.useRealTimers(); vi.resetModules(); vi.doUnmock('../src/memory/shared-sqlite.js'); });

const ino = (f: string) => (existsSync(f) ? statSync(f).ino : null);

async function scenario(useShared: boolean) {
  const dbPath = join(root, `m-${useShared}.db`);
  const holder = new HolderCtor(dbPath);
  holder.pragma('journal_mode=WAL');
  holder.exec('create table memory_entries(x)');
  holder.prepare('insert into memory_entries values(1)').run();
  const before = [ino(dbPath + '-wal'), ino(dbPath + '-shm')];

  process.env.CLAUDE_FLOW_GRAPH_EDGE_IDLE_MS = '50';
  if (useShared) {
    vi.doMock('../src/memory/shared-sqlite.js', () => ({
      loadBetterSqlite3: async () => HolderCtor,
      resolveAgentdbBetterSqlite3: () => HolderCtor,
    }));
  }
  vi.useFakeTimers();
  const gw = await import('../src/memory/graph-edge-writer.js');
  const db = await gw.getBridgeDb(dbPath);
  expect(db).not.toBeNull();
  db.prepare('insert into memory_entries values(2)').run();
  vi.advanceTimersByTime(60); // idle release fires: checkpoint(TRUNCATE) + close
  vi.useRealTimers();
  const after = [ino(dbPath + '-wal'), ino(dbPath + '-shm')];
  holder.prepare('insert into memory_entries values(3)').run();
  const integrity = holder.pragma('integrity_check');
  holder.close();
  return { before, after, integrity };
}

afterAll(() => { try { rmSync(root, { recursive: true, force: true }); } catch { /* */ } });

describe('#3693 graph writer idle close vs live AgentDB handle', () => {
  it('helper resolves the constructor from the agentdb dependency owner', async () => {
    if (!native) return;
    const { resolveAgentdbBetterSqlite3 } = await import('../src/memory/shared-sqlite.js');
    expect(resolveAgentdbBetterSqlite3(agentdbEntry)).toBe(HolderCtor);
  });

  it("control: a different native copy DOES strip the live holder's sidecars (the hazard)", async () => {
    if (!native) return;
    const r = await scenario(false);
    expect(r.before[0]).not.toBeNull();
    expect(r.after).toEqual([null, null]);
  });

  it('graph writer sharing the holder copy leaves the WAL/SHM sidecars intact', async () => {
    if (!native) return;
    const r = await scenario(true);
    expect(r.before[0]).not.toBeNull();
    expect(r.after).toEqual(r.before);
    expect(r.integrity).toEqual([{ integrity_check: 'ok' }]);
  });
});

