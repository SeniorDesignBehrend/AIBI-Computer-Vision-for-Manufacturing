# Test Case Implementation Status Audit

Generated: 2026-03-22
Source of truth: `tests/defined_tests.md`
Code evidence checked: `tests/test_unit_requirements.py`, `tests/test_comprehensive.py`, other `tests/test_*.py`
Execution check run: `pytest tests/test_unit_requirements.py tests/test_comprehensive.py`
Result: **35 passed, 4 failed**

---

## Summary

- Defined test cases in `defined_tests.md`: **44 unique IDs**
- Defined test cases with direct coded test ID match: **10**
- Defined test cases with requirement-level coded coverage (manual case covered by related AUTO case): **8**
- Defined test cases currently implemented through code (direct + requirement-level): **18**
- Defined test cases **not implemented through code**: **26**
- Coded IDs currently failing in requirements suite: **TC-SFR2-AUTO-01**, **TC-EISR6-AUTO-01**
- ID rename update completed: **ETSR → EISR** in requirement test code

---

## A) Implemented Through Code and Up to Date

These are implemented through code and currently passing in the requirement-focused suite.

### Direct ID match (defined ID exists exactly in code)

- TC-SFR1-AUTO-01
- TC-SFR5-AUTO-01
- TC-SFR11-AUTO-01
- TC-SFR15-AUTO-01
- TC-SFR16-AUTO-01
- TC-SFR17-AUTO-01
- TC-PPSR2-AUTO-01
- TC-PPSR5-AUTO-01
- TC-EISR3-AUTO-01

### Requirement-level coverage (manual case covered by passing coded AUTO case)

- TC-SFR4-MAN-01 (covered by TC-SFR4-AUTO-01)
- TC-SFR12-MAN-01 (covered by TC-SFR12-AUTO-01)
- TC-SFR18-MAN-01 (covered by TC-SFR18-AUTO-01)
- TC-PDSR1-MAN-01 (covered by TC-PDSR1-AUTO-01)
- TC-PDSR2-MAN-01 (covered by TC-PDSR2-AUTO-01)
- TC-ODSR2-MAN-01 (partially aligned via TC-QDSR1-AUTO-01 dependency audit)

---

## B) Implemented Through Code but Not Up to Date

These are implemented through code but currently not up to date because their related coded tests are failing.

- TC-SFR2-MAN-01
  - Covered by TC-SFR2-AUTO-01 (failing: `WorkstationConfig.__init__()` unexpected `barcode_fields` argument).
- TC-EISR6-MAN-01
  - Covered by TC-EISR6-AUTO-01 (failing: same constructor mismatch).
- TC-EISR6-AUTO-01
  - Exact coded ID exists, currently failing (same constructor mismatch).

---

## C) Not Implemented Through Code (as of now)

No clear automated implementation was found for these IDs.

- TC-SFR1-MAN-01 (manual live-camera variant not automated end-to-end)
- TC-SFR5-MAN-01 (manual Excel-target keystroke behavior not automated end-to-end)
- TC-SFR6-MAN-01
- TC-SFR7-MAN-01
- TC-SFR8-MAN-01
- TC-SFR9-MAN-01
- TC-SFR10-MAN-01
- TC-SFR11-MAN-01 (manual consecutive-run scenario not explicitly automated as written)
- TC-SFR14-MAN-01
- TC-SFR15-MAN-01 (manual factory-lighting scenario not automated as written)
- TC-SFR16-MAN-01 (manual live multi-code scenario not automated as written)
- TC-SFR19-MAN-01
- TC-SFR20-MAN-01
- TC-SFR21-MAN-01
- TC-SFR22-MAN-01
- TC-SFR26-MAN-01
- TC-SFR28-MAN-01
- TC-PUSR1-MAN-01
- TC-PUSR2-MAN-01
- TC-PUSR3-MAN-01
- TC-PUSR4-MAN-01
- TC-PUSR10-MAN-01
- TC-PPSR2-MAN-01 (operator-perception portion remains manual)
- TC-PPSR5-MAN-01 (real hardware/lighting condition as written remains manual)
- TC-PDSR4-MAN-01
- TC-SFR14-AUTO-01

---

## D) Extra Coded Tests Not Declared in `defined_tests.md`

These coded IDs exist but are not listed as test case IDs in `defined_tests.md`.

- TC-SFR2-AUTO-01
- TC-SFR4-AUTO-01
- TC-SFR12-AUTO-01
- TC-SFR18-AUTO-01
- TC-PDSR1-AUTO-01
- TC-PDSR2-AUTO-01
- TC-QDSR1-AUTO-01
- TC-EISR5-AUTO-01

---

## Recommended Next Updates

1. Fix constructor usage in SFR2/EISR6 tests to match current `WorkstationConfig` signature.
2. Add explicit coded test for TC-SFR14-AUTO-01 (`serialize_process`/`deserialize_process` cycle).
3. Decide whether to formally add extra coded IDs in Section D into `defined_tests.md` or keep them as internal support tests.
4. Keep manual usability/operator tests (`PUSR*`) explicitly marked as manual-only in traceability artifacts.
