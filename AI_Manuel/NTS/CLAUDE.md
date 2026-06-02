# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This directory contains tools and document corpus for working with the Spanish Grid Code supervision standard (NTS 631) and related power system standards. Primary use case: extract text and figures from regulatory PDFs for further analysis and LLM consumption.

## Scripts

### small_signal_2gen.py (planned, not yet created)

Small-signal eigenvalue analysis for the two-machine test system in NTS §5.10.2.1 (without MPE). Will sweep line reactance XL from 0.01 to 0.6 pu and plot electromechanical modes on the complex plane with 3% and 5% damping cones.

**Dependencies:** `numpy`, `scipy`, `matplotlib`

## Document corpus

| File | Source document |
|------|-----------------|
| `NormaTecnicaSupervision631_v2_publicada.md` | REE NTS 631 v2 (2020) — Spanish TSO conformity supervision standard for power generation modules under EU Regulation 2016/631 |
| `4215-2016.md` | IEEE Std 421.5-2016 — Excitation system models for power system stability studies |
| `KUNDUR_OCR.md` | Kundur, *Power System Stability and Control* — OCR quality is low (headers mostly empty); treat as a figure-reference index rather than readable text |

Each document has a corresponding `<stem>_fig/` directory of PNG figures extracted by `pdf_to_markdown.py`.

## Key domain concepts

- **MGE** (Módulo de Generación de Electricidad) — power generation module, the entity being certified under NTS 631
- **PEC** — conformity evaluation procedure (por Certificado / por Prueba / por Simulación)
- **CAMGE** — ancillary services module (STATCOM, PPC, synchronous compensator, BESS)
- **NTS §5.10.2.1** — the two-machine test system section that `small_signal_2gen.py` implements
