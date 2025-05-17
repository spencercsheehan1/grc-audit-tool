# Branch Naming Guide

A concise convention for naming Git branches in this Python project. Following these rules keeps our history tidy, lets automation do its job, and helps new contributors ramp up quickly.

---

## 1 Primary Format

| Rule                  | Description                                                | Example                                               | Notes                       |
|----------------------|------------------------------------------------------------|-------------------------------------------------------|
| **kebab‑case**       | Lower‑case words separated by hyphens                      | `stone-mill-upgrade`                                   |
| **Prefix**           | Namespace that explains *why* the branch exists            | `feature/`, `bugfix/`, `hotfix/`, `chore/`, `docs/`    |
| **No spaces**        | Spaces break Git commands & URLs                           | ✅ `feature/first-harvest` ❌ `feature/first harvest`   |
| **Avoid punctuation**| Only hyphens (`-`) and forward‑slash prefix are allowed   | `bugfix/umami-boost-overflow`                          |

> **TL;DR** — `<prefix>/<kebab‑case-summary>`

---

## 2 Matcha‑Themed A–Z Stubs

Pick the next unused stub (or choose one that best fits your work). Combine it with a prefix to form the final branch name.

| Letter | Stub (kebab‑case)     | Quick Note                               |
| ------ | --------------------- | ---------------------------------------- |
| A      | **aerated-leaves**    | Air‑dried leaves; a light starting point |
| B      | **bitter-balance**    | Tweaking bitterness vs. sweetness        |
| C      | **ceremonial-grade**  | Highest matcha quality                   |
| D      | **deep-steam**        | Longer steaming step                     |
| E      | **emerald-powder**    | Vivid green tone                         |
| F      | **first-harvest**     | *Ichibancha* – prized first flush        |
| G      | **gyokuro-shade**     | Shaded tea used for premium matcha       |
| H      | **hand-ground**       | Traditional stone‑mill method            |
| I      | **ichibancha-batch**  | Another nod to first flush               |
| J      | **jade-blend**        | Evokes brilliant green                   |
| K      | **kamairi-twist**     | Pan‑fired style                          |
| L      | **leaf-to-life**      | Farm‑to‑cup ethos                        |
| M      | **matcha-mountain**   | High‑elevation farms                     |
| N      | **nishio-reserve**    | Famous growing region                    |
| O      | **okumidori-mix**     | Popular cultivar                         |
| P      | **powder-perfection** | Ultra‑fine grind                         |
| Q      | **quiet-whisk**       | Meditative ceremony moment               |
| R      | **rain-harvest**      | Seasonally rain‑fed                      |
| S      | **stone-mill**        | Granite millstones                       |
| T      | **tencha-raw**        | Leaf form before grinding                |
| U      | **umami-boost**       | Savory depth                             |
| V      | **vivid-green**       | Color metric for freshness               |
| W      | **whisked-clouds**    | Frothy crema                             |
| X      | **x-factor-grade**    | Playful mystery quality                  |
| Y      | **yame-shade**        | Premium Kyushu region                    |
| Z      | **zen-finish**        | Calm after the sip                       |

### Usage Example

```bash
# new feature work using the next stub (e.g. emerald-powder)
git checkout -b feature/emerald-powder
```

Prefer sequential order (A→Z) when possible; if the ideal word is out of order, just pick the best fit.

---

## 3 Optional snake\_case Mirror

If you *must* stick to underscores (e.g., organization policy), mirror the stub with underscores:

```
aerated_leaves  bitter_balance  ceremonial_grade  deep_steam  ...  zen_finish
```

> **Recommendation:** Keep branch names in kebab‑case; use snake\_case only for file or variable names inside the codebase.

---

## 4 Branch Protection & Hygiene

1. **Protected Branches** – `main` and anything matching `release/*` require passing CI and one approving review.
2. **Delete After Merge** – Enable "Automatically delete head branches" in repo settings to keep clutter down.
3. **One Purpose per Branch** – Small, focused branches make code reviews quicker and reduce merge conflicts.

---

## 5 Real‑World Samples

| Purpose                       | Final Name                  |
| ----------------------------- | --------------------------- |
| New CLI argument parser       | `feature/leaf-to-life-cli`  |
| Fix off‑by‑one in array slice | `bugfix/quiet-whisk-slice`  |
| Bump version for release      | `release/zen-finish-v1.4.0` |

---

## 6 How to Contribute

1. **Pick** an unused stub.
2. **Create** your branch following the format.
3. **Push** code & open a pull request linked to an issue (if applicable).
4. **Delete** the branch after merge.

Happy coding ☕️💚
