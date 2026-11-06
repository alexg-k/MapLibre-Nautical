#!/usr/bin/env python3
"""Checks the Python symbology port against njord's golden fixtures.

    python3 tools/check_njord_port.py --njord /path/to/njord [--only BOYLAT,LIGHTS] [--no-style]

Runs every ``testdata/symbology/pre_tile_encode[_cell]/*.json`` case through the ported
``pre_tile_encode`` and diffs the generated styles against ``testdata/symbology/style/*.json``
(modulo the base URL, which the fixtures record as ``https://njord.test``).
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nautical.symbology.colors import ColorLibrary, Depth, Theme, ThemeMode  # noqa: E402
from nautical.symbology.factory import LayerFactory  # noqa: E402
from nautical.symbology.feature import ChartFeature  # noqa: E402
from nautical.symbology.style import style  # noqa: E402

BASE_URL = "https://njord.test"


def load(path):
    with open(path) as f:
        return json.load(f)


def feature(layer, case_input):
    return ChartFeature(
        layer=layer,
        props=dict(case_input.get("props", {})),
        geometry_type=case_input.get("geometry_type"),
        associated_layer_names=list(case_input.get("assoc", [])),
    )


def expected_of(case):
    port = case.get("port")
    if port and "expected" in port:
        return port["expected"]
    return case["expected"]


def diff(expected, actual, path="$"):
    """The first difference between two JSON values, or None."""
    if isinstance(expected, dict) and isinstance(actual, dict):
        for k in expected:
            if k not in actual:
                return f"{path}.{k}: missing (expected {json.dumps(expected[k])})"
            d = diff(expected[k], actual[k], f"{path}.{k}")
            if d:
                return d
        extra = [k for k in actual if k not in expected]
        if extra:
            return f"{path}: unexpected keys {extra} = {json.dumps({k: actual[k] for k in extra})}"
        return None
    if isinstance(expected, list) and isinstance(actual, list):
        if len(expected) != len(actual):
            return f"{path}: length {len(expected)} != {len(actual)}"
        for i, (e, a) in enumerate(zip(expected, actual)):
            d = diff(e, a, f"{path}[{i}]")
            if d:
                return d
        return None
    if isinstance(expected, bool) or isinstance(actual, bool):
        if expected is actual or expected == actual and type(expected) is type(actual):
            return None
        return f"{path}: {json.dumps(expected)} != {json.dumps(actual)}"
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        if expected == actual:
            return None
        return f"{path}: {expected!r} != {actual!r}"
    if expected == actual:
        return None
    return f"{path}: {json.dumps(expected)} != {json.dumps(actual)}"


def check_pre_tile_encode(factory, testdata, only, failures):
    checked = 0
    for subdir in ["pre_tile_encode", "pre_tile_encode/custom_key", "pre_tile_encode_cell"]:
        d = testdata / "symbology" / subdir
        for path in sorted(d.glob("*.json")):
            key = path.stem
            if only and key not in only:
                continue
            entry = factory.get(key)
            if entry is None:
                if subdir == "pre_tile_encode_cell":
                    # An unregistered layer passes through unchanged.
                    for i, case in enumerate(load(path)["cases"]):
                        checked += 1
                        d = diff(expected_of(case), dict(case["input"]["props"]))
                        if d:
                            failures.append(f"{subdir}/{key}[{i}]: {d}")
                else:
                    failures.append(f"{subdir}/{key}: fixture for an unregistered layerable")
                continue
            try:
                layerable = entry.layerable
            except Exception as e:  # noqa: BLE001
                failures.append(f"{subdir}/{key}: cannot load layerable: {e!r}")
                continue
            for i, case in enumerate(load(path)["cases"]):
                checked += 1
                f = feature(key, case["input"])
                try:
                    layerable.pre_tile_encode(f, factory.cx)
                except Exception as e:  # noqa: BLE001
                    failures.append(f"{subdir}/{key}[{i}] {json.dumps(case['input'])[:200]}: raised {e!r}")
                    continue
                d = diff(expected_of(case), f.props)
                if d:
                    failures.append(f"{subdir}/{key}[{i}] input={json.dumps(case['input'])[:300]}\n    {d}")
    # A layerable without a fixture must leave a minimal feature unchanged.
    with_fixture = {p.stem for sub in ["pre_tile_encode", "pre_tile_encode/custom_key"] for p in (testdata / "symbology" / sub).glob("*.json")}
    for entry in factory.entries:
        if entry.key in with_fixture or (only and entry.key not in only):
            continue
        for geometry in ["POINT", "LINESTRING", "POLYGON"]:
            checked += 1
            f = feature(entry.key, {"props": {}, "geometry_type": geometry, "assoc": []})
            try:
                entry.layerable.pre_tile_encode(f, factory.cx)
            except Exception as e:  # noqa: BLE001
                failures.append(f"{entry.key} ({geometry}): raised {e!r}")
                continue
            if f.props:
                failures.append(f"{entry.key} ({geometry}): no fixture but props changed: {f.props}")
    return checked


def check_styles(factory, testdata, only, failures):
    checked = 0
    for path in sorted((testdata / "symbology" / "style").glob("*.json")):
        checked += 1
        case = load(path)["cases"][0]
        inp = case["input"]
        depth = Depth(inp["depth"])
        theme_name = inp["theme"]
        custom = inp.get("custom") or inp.get("c")
        theme = Theme(ThemeMode(theme_name.upper()), custom)
        expected = case["expected"]
        if only:
            d = None
            for key in sorted(only):
                entry = factory.get(key)
                if entry is None:
                    d = f"{key}: not registered"
                    break
                try:
                    act_layers = entry.layers(factory.cx, depth, theme, factory.source)
                except Exception as e:  # noqa: BLE001
                    d = f"{key}: raised {e!r}"
                    break
                ids = {l["id"] for l in act_layers}
                exp_layers = [l for l in expected["layers"] if l["id"] in ids]
                d = diff_layers(exp_layers, act_layers)
                if d:
                    d = f"{key}: {d}"
                    break
        else:
            try:
                actual = style(
                    factory,
                    depth,
                    theme,
                    sources={"src_senc": {"type": "vector", "url": f"{BASE_URL}/v1/tile_json", "promoteId": "LNAM"}},
                    sprite=f"{BASE_URL}/v1/content/sprites/{theme.mode.path_name}_simplified",
                    glyphs=f"{BASE_URL}/v1/content/fonts/{{fontstack}}/{{range}}.pbf",
                )
            except Exception as e:  # noqa: BLE001
                failures.append(f"style {path.stem}: raised {e!r}")
                continue
            d = diff({k: v for k, v in expected.items() if k != "layers"}, {k: v for k, v in actual.items() if k != "layers"})
            d = d or diff_layers(expected["layers"], actual["layers"])
        if d:
            failures.append(f"style {path.stem}: {d}")
    return checked


def diff_layers(expected, actual):
    exp_ids = [l["id"] for l in expected]
    act_ids = [l["id"] for l in actual]
    if exp_ids != act_ids:
        for i, (e, a) in enumerate(zip(exp_ids, act_ids)):
            if e != a:
                return f"layer order/ids differ at index {i}: expected {e!r}, got {a!r} (expected {len(exp_ids)} layers, got {len(act_ids)})"
        return f"layer count differs: expected {len(exp_ids)}, got {len(act_ids)} (missing: {sorted(set(exp_ids) - set(act_ids))[:10]}, extra: {sorted(set(act_ids) - set(exp_ids))[:10]})"
    for e, a in zip(expected, actual):
        d = diff(e, a, e["id"])
        if d:
            return d
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--njord", required=True, help="path to a njord checkout")
    ap.add_argument("--only", default="", help="comma separated layerable keys to check")
    ap.add_argument("--no-style", action="store_true")
    ap.add_argument("--no-encode", action="store_true")
    args = ap.parse_args()
    testdata = Path(args.njord) / "testdata"
    only = {k.strip() for k in args.only.split(",") if k.strip()}

    colors = ColorLibrary.load(Path(args.njord) / "crates/njord-server/resources/colors.json")
    factory = LayerFactory(colors=colors)
    failures = []
    checked = 0
    if not args.no_encode:
        checked += check_pre_tile_encode(factory, testdata, only, failures)
    if not args.no_style:
        checked += check_styles(factory, testdata, only, failures)
    for f in failures:
        print("FAIL", f)
    print(f"{checked} checks, {len(failures)} failures")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
