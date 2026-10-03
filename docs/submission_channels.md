# Submission Channel Reconnaissance — Paper 2 (2026-10-03, goal R5)

Automated probe results (curl, Chrome UA, 10-20s timeouts). Purpose: pick the
first reachable submission channel for the torque-arbitration paper and record
the full matrix so later papers skip dead ends.

## Matrix

| Journal (chain slot) | System | Probe result | Auto-submittable |
|---|---|---|---|
| IET SMT (main) | ScholarOne `mc.manuscriptcentral.com/iet-smt` | HTTP 403, `cf-mitigated: challenge` | NO (JS challenge) |
| COMPEL (backup 1) | ScholarOne `mc.manuscriptcentral.com/compel`; emerald.com | 403 challenge | NO |
| CES TEMS (backup 2) | ScholarOne `mc03.manuscriptcentral.com/tems` | 403 "Just a moment..." | NO |
| REE (Pleiades, backup 3) | pleiades.online reachable (200); per-journal system TBD | 200 | TBD (email route plausible) |
| Tsinghua Sci&Tech OA | journalx JSP `jst.tsinghuajournals.com` (2019-era, no CF) | 200 but lands on Chinese Tsinghua Acta; EN-edition entry TBD | TBD |
| JCST | jcst.ict.ac.cn | 200 | TBD (scope mismatch for Paper 2; target for B6/B7) |
| Editorial Manager generic | `editorialmanager.com/<guess>` | unknown codes 302→ariessys.com (code not configured) | EM proven automatable via EMSE-D-26-01301 |

## Facts

- All ScholarOne (Wiley-hosted IET, Emerald, CES TEMS mc03) sit behind
  Cloudflare Turnstile; headless clients get a challenge page. Do NOT retry in
  a loop (rate-limit risk, policy).
- EMSE (Editorial Manager) was fully submitted automatically 2026-10-03:
  EMSE-D-26-01301. So any EM-hosted journal is automatable once its exact
  manager code is known.
- Springer journal pages (link.springer.com) render submission links via JS;
  static curl cannot extract EM codes. Use search or the known-code list.

## Decision

1. Paper 2 keeps IET SMT as *primary* target, but submission waits for a
   human browser window (Cloudflare) — logged in pipeline/01 ledger.
2. Meanwhile the automated chain targets the next reachable channel:
   - resolve REE/Pleiades submission mechanism (email vs system), or
   - resolve a correct Editorial Manager code for an in-scope journal.
3. Manuscript (main.tex, 6 pp, 6 verified references) and replication package
   (tag v0.3.0) are ready; no content blocker remains.
