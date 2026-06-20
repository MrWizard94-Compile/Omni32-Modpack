#!/usr/bin/env python3
"""Generate a CurseForge-style manifest draft from Omni32 upscaled namespaces."""
from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

PACK_NAME = "Omni32"
PACK_VERSION = "0.1.0-alpha"
MC_VERSION = "1.20.1"
FORGE_VERSION = "47.4.10"

# Batch 0 platform mods (CurseForge project IDs) — always included
PLATFORM_PROJECT_IDS = [
    238222,   # JEI
    419699,   # Architectury API
    348521,   # Cloth Config
    890405,   # Embeddium
    581495,   # Oculus
    429235,   # FerriteCore
    790626,   # ModernFix
    627557,   # ImmediatelyFast
    60089,    # Mouse Tweaks
    250398,   # Controlling
    459701,   # Searchables
]

SLUG_ALIASES = {
    "applied-energistics-2": "ae2",
    "farmers-delight": "farmersdelight",
    "twilight-forest": "twilightforest",
    "the-twilight-forest": "twilightforest",
    "biomes-o-plenty": "biomesoplenty",
    "create": "create",
    "mekanism": "mekanism",
    "refined-storage": "refinedstorage",
    "valkyrien-skies": "valkyrienskies",
    "jei": "jei",
    "quark": "quark",
    "supplementaries": "supplementaries",
    "minecolonies": "minecolonies",
    "sophisticated-backpacks": "sophisticatedbackpacks",
    "sophisticated-storage": "sophisticatedstorage",
    "ars-nouveau": "ars_nouveau",
    "botania": "botania",
    "thermal-expansion": "thermal_expansion",
    "thermal-foundation": "thermal_foundation",
    "thermal-core": "thermal_core",
    "thermal-innovation": "thermal_innovation",
}


def load_registry(ac_root: Path):
    ac_root = ac_root.resolve()
    if str(ac_root) not in sys.path:
        sys.path.insert(0, str(ac_root))
    spec = importlib.util.spec_from_file_location(
        "ac_registry", ac_root / "config" / "registry.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def namespace_to_mod_ids(registry) -> dict[str, set[str]]:
    mapping: dict[str, set[str]] = {}
    for mod_id in registry.MOD_REPOS:
        ns = registry.texture_namespace(mod_id)
        mapping.setdefault(ns, set()).add(mod_id)
    return mapping


def upscaled_namespaces(ac_root: Path) -> set[str]:
    assets = ac_root / "output" / "assets"
    if not assets.is_dir():
        return set()
    result = set()
    for child in assets.iterdir():
        tex = child / "textures"
        if child.is_dir() and tex.is_dir() and any(tex.rglob("*.png")):
            result.add(child.name)
    return result


def load_atm10(ac_root: Path) -> list[dict]:
    path = ac_root / "data" / "atm10_mods_raw.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def slug_to_mod_id(slug: str) -> str:
    slug = slug.lower().strip()
    if slug in SLUG_ALIASES:
        return SLUG_ALIASES[slug]
    return slug.replace("-", "_")


def build_curse_index(atm10: list[dict]) -> dict[str, int]:
    index: dict[str, int] = {}
    for entry in atm10:
        curse = (entry.get("curse_info") or {}).get("curse_id")
        if not curse:
            continue
        slug = entry.get("slug", "")
        index[slug_to_mod_id(slug)] = curse
        index[slug.replace("-", "_")] = curse
    return index


def main() -> int:
    ac_root = Path(os.environ.get("ASSETCONVERTER_ROOT", r"C:\Projects\AssetConverter"))
    pack_root = Path(__file__).resolve().parents[1]
    manifest_dir = pack_root / "manifest"
    manifest_dir.mkdir(exist_ok=True)

    if not (ac_root / "config" / "registry.py").is_file():
        print(f"[!] AssetConverter not found at {ac_root}")
        print("    Set ASSETCONVERTER_ROOT to your AssetConverter clone.")
        return 1

    registry = load_registry(ac_root)
    ns_map = namespace_to_mod_ids(registry)
    namespaces = upscaled_namespaces(ac_root)
    atm10 = load_atm10(ac_root)
    curse_index = build_curse_index(atm10)

    mod_ids: set[str] = set()
    unresolved_ns: list[str] = []
    unresolved_mods: list[str] = []

    for ns in sorted(namespaces):
        candidates = ns_map.get(ns, {ns})
        mod_ids.update(candidates)
        if ns not in ns_map and ns not in registry.MOD_REPOS:
            unresolved_ns.append(ns)

    project_ids: set[int] = set(PLATFORM_PROJECT_IDS)
    for mod_id in sorted(mod_ids):
        pid = curse_index.get(mod_id)
        if pid:
            project_ids.add(pid)
        else:
            unresolved_mods.append(mod_id)

    files = [{"projectID": pid, "fileID": 0, "required": True} for pid in sorted(project_ids)]

    manifest = {
        "minecraft": {
            "version": MC_VERSION,
            "modLoaders": [{"id": "forge", "primary": True}],
        },
        "manifestType": "minecraftModpack",
        "manifestVersion": 1,
        "name": PACK_NAME,
        "version": PACK_VERSION,
        "author": "MrWizard94",
        "files": files,
        "overrides": "overrides",
    }

    pack_path = manifest_dir / "pack.json"
    with open(pack_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    modlist_path = manifest_dir / "modlist.txt"
    with open(modlist_path, "w", encoding="utf-8") as f:
        f.write(f"Omni32 upscaled namespaces: {len(namespaces)}\n")
        f.write(f"Resolved mod ids: {len(mod_ids)}\n")
        f.write(f"CurseForge project entries: {len(files)}\n")
        f.write("\n--- Namespaces on disk ---\n")
        f.write("\n".join(sorted(namespaces)))
        f.write("\n\n--- Unresolved namespaces (no registry mod_id) ---\n")
        f.write("\n".join(unresolved_ns) or "(none)")
        f.write("\n\n--- Mod ids without CF projectID ---\n")
        f.write("\n".join(unresolved_mods) or "(none)")
        f.write("\n")

    print(f"[*] Wrote {pack_path}")
    print(f"[*] {len(namespaces)} namespaces -> {len(mod_ids)} mod ids -> {len(files)} CF projects")
    print(f"[*] fileID is 0 (placeholder) — resolve before CurseForge publish")
    if unresolved_ns:
        print(f"[!] {len(unresolved_ns)} namespaces without registry mapping")
    if unresolved_mods:
        print(f"[!] {len(unresolved_mods)} mod ids without CurseForge projectID")
    return 0


if __name__ == "__main__":
    sys.exit(main())