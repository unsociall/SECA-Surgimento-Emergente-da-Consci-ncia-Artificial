# SECA — MemPalace static audit, part 47 (Chroma integration, partial)

Date: 2026-11-14. Source: MemPalace/mempalace, pinned commit `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.
File: `mempalace/backends/chroma.py`, blob SHA `ce2f88b15395a6f231bcfb39e9929a6c788c2d6a`; 3,374 lines returned by the source reader. **Coverage: targeted static inspection, NOT full-file certification.** No code was run, installed, or transferred to the user's device.

## Verified source observations

- Lines 28–32 import `open_reader`, `open_writer`, and `palace_db_lock` from `_inproc_sqlite`.
- Line 107 sets `_ChromaSettings(anonymized_telemetry=False)`; this is a local configuration declaration, not proof of the absence of every network path.
- Lines 834, 1032, 1087 call `open_palace_reader`; lines 1880 and 1936 call `open_palace_writer` for pre-open migrations. These call sites merit review of cleanup and transaction boundaries.
- Lines 2187–2192 combine `mine_palace_lock` and `palace_db_lock` for a write-critical section. Lines 2900–2903, 3115–3118, 3178–3180, 3239–3243 and 3284–3294 guard client lifecycle or collection operations using `palace_db_lock`.
- Lines 3003–3006 construct `chromadb.PersistentClient(... settings=_CLIENT_SETTINGS)`; lines 3075–3100 describe pre-open migration/quarantine safety passes.
- Lines 150–225 sniff HNSW binary header/pickle envelope without deserializing the pickle; envelope checks do **not** establish cryptographic integrity or safe downstream deserialization.
- Lines 280–322 document HNSW batching/synchronization assumptions and historical measurements in source comments. These figures were not independently reproduced.

## Static risk hypotheses / follow-up

1. Inspect lock ordering and reentrancy across `_client`, `_client_locked`, `get_collection`, `_prepare_palace_for_open`, and migrations; the current evidence does not prove a deadlock.
2. Inspect the exception/rollback paths in pre-open migrations and cleanup of open reader/writer handles.
3. Review filesystem quarantine and HNSW header heuristics for false positives, symlink races, and unexpected input formats. Do not label these as confirmed vulnerabilities.
4. Trace all embedding-function creation paths. Chroma supports pretrained embeddings; this is **not acceptable** as a SECA dependency. An offline biological SECA design may borrow only abstract persistence/integrity requirements, without embeddings, pretrained models, or language teaching.

## Coverage ledger

The historical Git tree manifest lists 851 blobs at the pinned commit, but is not a proof of reading. This part adds a **partial** inspection of `mempalace/backends/chroma.py`; it must not be marked fully read. Previous audit evidence and blob hashes still require reconciliation. Do not start Ruflo until every in-scope MemPalace blob has verifiable inspection evidence and all exclusions are explicit.

## Next step

Continue line-range inspection of `chroma.py` and its lock/migration tests; reconcile this report with the 851-entry tree manifest. No component adaptation or implementation authorized at this phase.
