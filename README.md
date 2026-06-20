# Omni32 Modpack

Kitchen-sink Forge **1.20.1** modpack built around the [Omni32](https://github.com/MrWizard94-Compile/AssetConverter) texture catalog. Unlike [Base Wars](https://github.com/MrWizard94-Compile/NodeCore), this pack has no single progression fantasy — the goal is **broad mod coverage with consistent 32× textures**.

## Architecture

| Layer | Repo / path |
|-------|-------------|
| Textures | [AssetConverter](https://github.com/MrWizard94-Compile/AssetConverter) `output/assets/` |
| Texture delivery | [Omni32 Loader](https://github.com/MrWizard94-Compile/Omni32_Loader) mod |
| Pack manifest | This repo — `manifest/` + `scripts/generate_manifest.py` |
| Overrides | `overrides/` — configs, KubeJS, default loader config |

## Quick start (local)

```powershell
# 1. Generate draft manifest from upscaled namespaces
$env:ASSETCONVERTER_ROOT = "C:\Projects\AssetConverter"
python scripts/generate_manifest.py

# 2. Copy overrides + install mods from manifest into a Forge 1.20.1 instance
# 3. Place omni32_loader jar in mods/ (or overrides/mods/ for export)
# 4. Set assets.root in config/omni32_loader-client.toml
```

## Phased expansion

Mods are added in **batches** (performance → libraries → tech → magic → worldgen → decoration) with compat passes between each batch. See `docs/MOD_BATCHES.md`.

## CurseForge export

When ready for distribution:

1. Resolve `fileID` entries in `manifest/pack.json` (draft uses `projectID` only).
2. Zip `manifest.json`, `modlist.html`, and `overrides/` per CF spec.
3. Publish via CurseForge author dashboard (manual step).

## Related

- [Omni32 Loader](https://github.com/MrWizard94-Compile/Omni32_Loader)
- [JanusPrime orchestration](https://github.com/MrWizard94-Compile/JanusPrime)