---
name: higher-ed-tam-research
description: Research and validate US higher education market data, non-traditional student enrollment, and TAM/SAM metrics for pitch decks. Returns verified statistics with sources, growth rates, and future projections.
argument-hint: <topic: tam|sam|growth|projections|definitions> [--validate]
---

You are researching US higher education market data for Boostability pitch decks (especially Morgan Stanley MSISV).

Load context:
@context/work.md
@context/current-priorities.md

---

## Quick Data Reference

**TAM: Total Addressable Market (US Higher Ed - 2023)**
- Students: 18.3M undergraduates
- Institutions: 4,000 degree-granting
- Source: NSC Research Center, NCES

**SAM: Non-Traditional Students Age 25+**
- Students: 5.9-6.3M (34-37% of total)
- Institutions: ~3,500-3,700 (91% offer online)
- YoY Growth: 16.7-19.7% (Fall 2024)

**Why Now**
- HS grad decline: 13% (2023-2041) — WICHE
- 1/3 of students by 2030 will be 25+ — NCES Projections
- Adult learners NOW the growth engine — NSC/EAB

---

## Key Sources (Verified)

| Resource | Use | Link |
|----------|-----|------|
| NSC Research Center | Current growth, YoY rates | https://nscresearchcenter.org/current-term-enrollment-estimates/ |
| NCES Projections | 2030 forecasts | https://nces.ed.gov/programs/projections/ |
| WICHE | HS grad decline (13%) | https://findingequilibriumfutureshighered.substack.com/p/a-look-at-the-enrollment-cliff |
| Higher Ed Dive | Fall 2024 breakdown | https://www.highereddive.com/news/3-charts-that-tell-the-story-of-spring-2025-enrollment/752211/ |
| EAB | Adult market analysis | https://eab.com/resources/blog/adult-education-blog/ |

---

## Usage Examples

`/higher-ed-tam-research tam` — Get TAM breakdown and sources

`/higher-ed-tam-research sam` — Get SAM (non-traditional) data with growth rates

`/higher-ed-tam-research growth` — Show verified YoY growth statistics

`/higher-ed-tam-research projections` — Get 2030 forecasts

`/higher-ed-tam-research definitions` — NCES non-traditional definition + characteristics

`/higher-ed-tam-research --validate` — Validate all statistics and flag any unverified claims

---

## Key Findings

### Growth (Fall 2024 - YoY)
- Non-traditional undergrads: +16.7-19.7%
- First-year students 25+: +19.7%
- First-year students 21-24: +16.7%
- Traditional first-year: +3.4%

### Market Definition (NCES)
Non-traditional = ANY of these 7:
1. Delayed enrollment (>1 year)
2. Part-time attendance
3. Works full-time (35+ hrs/week)
4. Financially independent
5. Has dependents (other than spouse)
6. Single parent
7. GED/certificate instead of diploma

### Projections (2030)
- Adult learners (25+): 35% of enrollment
- Overall growth: +8% (2020-2030)
- 1/3 of students will be 25+

---

## Pitch Deck Bullets (Ready to Use)

✓ First-year students 25+ grew 19.7% in fall 2024
✓ 1/3 of students by 2030 will be age 25+
✓ 13% decline in HS graduates through 2041
✓ 5.9-6.3M non-traditional students currently underserved
✓ ~3,500-3,700 institutions need better tools for this segment

---

## Verification Status

**Verified ✓**
- 19.7% YoY growth (first-year 25+)
- 13% HS grad decline (WICHE)
- 5.9-6.3M students 25+
- 35% projection for 2030

**Unverified ❌**
- "600 institutions" — source not found
- Fall 2025 decline (-15.5%) — conflicts with growth narrative, needs clarification

**Recommended Before Finalizing Pitch:**
- Confirm fall 2025 decline vs. growth narrative with NSC Research Center
- Double-check NCES 2031 projections (most recent available)

---

## Related Files

- `/research/boostability-morgan-stanley-research-final.md` — Complete research with all quotes and sources
- `/research/higher-ed-tam-2025.md` — TAM/SAM data (2023 baseline)
- `/research/higher-ed-tam-25plus-validated.md` — Age 25+ detailed breakdown
