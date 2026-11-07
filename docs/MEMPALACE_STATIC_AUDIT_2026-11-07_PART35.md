# SECA — MemPalace static audit, part 35

Date: 2026-11-07. Source repository: MemPalace/mempalace. Fixed commit: `f8e35362189bd0a5abf4c0df1dd5bf90ba059176`.

## Scope and evidence
- `mempalace/backends/registry.py`: entire text retrieved and inspected; **complete static reading for this file**, pending Git blob SHA reconciliation.
- `mempalace/backends/base.py`: retrieved (39,075 characters; 983 lines) and inspected structurally and in selected ranges; **partial analytical coverage**, not yet counted complete.
- No execution, installation, dependency resolution, or testing.
- Historical Git inventory: 851 blobs reported in previous audits; **not independently reconciled in this part**. No certified global percentage.

## Registry findings
- Process-wide maps `_registry`, `_instances`, `_explicit` and flag `_discovered`. A lock serializes register/unregister, entry-point discovery and instance creation.
- `metadata.entry_points()` discovers plugins and `ep.load()` imports third-party code; merely selecting an installed plugin can execute import-time behavior. This was **not executed** in this audit.
- Explicit registration overrides entry points; failures to load a plugin are logged and skipped. Built-in registration imports Chroma, Milvus, Qdrant, SQLiteExact and pgvector implementations.
- `get_backend` caches one backend instance per name, not per palace. The isolation contract therefore depends on each backend honoring `PalaceRef.id` and namespace.
- `detect_backend_for_path` returns the alphabetically first backend when multiple artifacts match; its own documentation warns that protection logic should use the multi-result variant. This is a potential migration ambiguity, not a proven exploit.
- `reset_backends` invokes `close()` under the global lock; if an implementation re-enters registry methods, deadlock is possible. Requires call-graph review before treating as a confirmed defect.
- `available_backends` and detection traverse shared dictionaries outside the lock after discovery. Concurrent mutation warrants race analysis.
- `resolve_backend_for_palace` selects explicit > palace config > environment > disk detection > default; it returns the name without validating availability until a later lookup.

## Base contract findings (partial review)
- `PalaceRef.id` is the mandatory isolation key; namespaces are optional and must be rejected when unsupported.
- `validate_write_batch` checks column lengths and optionally unique IDs, but is not a full schema/type validator.
- Default `BaseCollection.update` is get/merge/upsert, explicitly non-atomic across the read/write boundary; backends advertising atomic update must override it.
- Default `get_recent` sorts only an initial bounded storage window, potentially omitting globally newest records.
- Default full-record pagination can become O(n²) for implementations that materialize and slice on every page.
- Embedder identity compatibility is specific to vector-model systems and is **not** a design requirement for SECA's biological offline core.

## SECA research relevance — documentation only
1. Define memory storage interfaces independently of cognition and learning, with mandatory per-organism isolation.
2. Require explicit ambiguity errors when more than one persistence format is detected.
3. Avoid dynamic plugin imports in the protected offline biological core; use auditable, explicitly approved adapters if ever needed.
4. Require atomic updates/checkpoints and deterministic failure behavior for critical memory.
5. Separate storage metadata recency from actual causal/event ordering; do not infer neural learning from vector retrieval.
6. No pretrained models, no language teaching, no external backends, and no implementation in this phase.

## Next audit
Finish line-by-line review of `base.py`, obtain blob SHAs from the fixed commit, and reconcile every audited path with the 851-file tree before reporting any coverage percentage. Ruflo remains blocked until MemPalace is fully certified.
