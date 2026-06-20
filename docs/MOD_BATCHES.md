# Mod batches (kitchen-sink rollout)

Mods are grouped for incremental compat testing. A batch is **done** when the instance boots, joins a world, and `/kubejs errors` (if present) is clean.

## Batch 0 — Platform

- Minecraft 1.20.1, Forge 47.4.x
- **omni32_loader** (required)
- JEI, Cloth Config, Architectury
- Embeddium + Oculus, FerriteCore, ModernFix, ImmediatelyFast
- Mouse Tweaks, Controlling, Searchables

## Batch 1 — Create stack

- Create, Create Addition, Connected, Deco, Big Cannons, Railways, Slice and Dice, Copycats, Trackwork
- Valkyrien Skies, Clockwork, Valkyrien Portals (compat pass required)

## Batch 2 — Industry & logistics

- AE2, Mekanism (+ generators/tools), Thermal suite, Refined Storage
- Sophisticated Backpacks/Storage, Storage Drawers, Modular Routers

## Batch 3 — Colony & structure

- MineColonies, Structurize, Domum Ornamentum, BlockUI

## Batch 4 — Magic & farming

- Ars Nouveau, Botania, Mystical Agriculture, Productive Bees/Trees, Occultism

## Batch 5 — Adventure & dimensions

- Twilight Forest, The Undergarden, Biomes We've Gone, Alex's Caves, Ice and Fire

## Batch 6 — Decoration & QoL

- Supplementaries, Quark, Macaw suite, Handcrafted, Beautify

---

Run `python scripts/generate_manifest.py --batch 0` (future flag) or edit the generated manifest manually while batches are introduced.