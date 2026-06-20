# Omni32 Modpack — Architecture

## Design intent

**Base Wars** optimizes for a specific war/economy loop. **Omni32 Modpack** optimizes for **coverage**: every mod with Omni32 textures should be viable in one instance, with compat layered incrementally.

## Data flow

```
AssetConverter output/assets/<namespace>/
        ↓  (no monolithic pack copy)
Omni32 Loader mod — active namespace mount
        ↓
Minecraft client resource manager (TOP position)
```

## Manifest generation

`scripts/generate_manifest.py`:

1. Lists namespaces under `output/assets/*/textures/`
2. Maps namespaces → registry `mod_id` via AssetConverter `config/registry.py`
3. Joins ATM10 CurseForge metadata (`data/atm10_mods_raw.json`) for `projectID`
4. Emits `manifest/pack.json` draft + `manifest/modlist.txt`

`fileID` pins require a second pass (CurseForge API or manual) before CF export.

## Overrides layout

```
overrides/
├── config/
│   └── omni32_loader-client.toml   # default asset store path
├── defaultconfigs/                  # first-run configs
├── kubejs/                          # recipes, tags, unification
├── mods/                            # custom jars (omni32_loader); not committed
└── resourcepacks/                   # optional — avoid Omni32 monolith when loader is used
```

## Compat strategy

| Phase | Focus |
|-------|-------|
| 0 | Forge 47.x, Embeddium/Oculus, FerriteCore, ModernFix, JEI |
| 1 | Create ecosystem + VS + Clockwork |
| 2 | Storage (AE2, RS, Sophisticated) |
| 3 | Power (Mekanism, Thermal, Powah, IF) |
| 4 | Magic (Ars, Botania, Occultism, …) |
| 5 | World/adventure (Twilight, Undergarden, BWG, …) |
| 6 | Decoration / Macaw / Supplementaries |

Each phase: add mods → launch → read `latest.log` → KubeJS/config/glue fixes.

## Version discipline

Upscaled textures match the AssetConverter `sources/<mod>/` revision. Manifest pins should track the same mod versions used during upscale, or expect texture drift.