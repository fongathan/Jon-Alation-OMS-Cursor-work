# BDC on OMS — Persona Review (one-slide talking sheet)

**Use when:** Data Foundations argues “just use OMS” instead of a separate Business Data Catalog experience.

---

## Opening (15 sec)

> We are **not** asking for a second metadata store. OMS stays the **system of record and API backbone**. The question is who owns the **business and governance experience** for Alation exit — especially for users who are **not OMS-first today**.

---

## One-line frame

**626 improves metadata supply · OMS stores and serves it · BDC is the governed business-metadata experience for the right persona.**

---

## Two personas, two optimized surfaces (same data)

| **OMS — Data Foundations** | **BDC — Data Governance** |
|----------------------------|---------------------------|
| Engineers, platform, integrators | Business consumers, stewards, privacy/compliance |
| *How is it built? Lineage? SQL?* | *What does it mean? Can I trust it? Who owns it?* |
| Technical + operational metadata | Descriptions, glossary, trust flags, policy context |
| Platform completeness | Alation-exit adoption (~531 users) |

**Architecture compromise:** one metadata API / one store — **two shells (UX only)** + **Open in OMS** for full technical detail.

---

## Why “just OMS” is incomplete

1. **Different jobs** — OMS optimizes platform users; BDC optimizes governed discovery and stewardship.
2. **Density** — stewards drown in ops/profiling chrome unless someone owns a **business-first** surface.
3. **Migration risk** — inventory in OMS ≠ glossary, endorse/deprecate, and business search parity for Alation exit.

---

## The ask (RACI)

| Own | Do **not** own |
|-----|----------------|
| **Business metadata experience** — descriptions, glossary, trust, steward UX, persona defaults | Metadata store, ingestion, scanners (626/MCI) |
| **Adoption & Alation-exit success** for non-engineer personas | Duplicate backends or dual-write |

**Foundations owns store and serve. Governance owns business-metadata experience backed by OMS.**

---

## If they insist on one UI only

> Then OMS must explicitly commit to **business-first defaults**, glossary/stewardship parity, and **Alation-exit metrics** — with Governance in the design loop. Otherwise we bet the migration on a UI built for a different persona.

---

## Close (10 sec)

> I’m asking to **own the business-metadata experience** on OMS — not compete with Foundations on the platform. Same spine; optimized surfaces; deep links for engineers.
