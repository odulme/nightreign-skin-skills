#!/usr/bin/env python3
# Part of Nightreign Skin Skills - CC BY-NC-SA 4.0, see LICENSE and NOTICE (non-commercial, attribution required).
"""Read-only PNG/template-mask validation. Requires Pillow and NumPy.
Exit 0: all images pass; 1: image contract failure; 2: invalid inputs/report path.
This checks pixels, not UV projection, art fidelity, skin halos, or in-game behavior.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

try:
    import numpy as np
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Requires Pillow and NumPy in the selected Python environment: " + str(exc))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rgba(path):
    with Image.open(path) as image:
        image.load()
        return np.array(image.convert("RGBA")), image.format, image.mode, list(image.size)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--template", type=Path, required=True)
    p.add_argument("--mask", type=Path, required=True)
    p.add_argument("--image", type=Path, action="append", required=True)
    p.add_argument("--mask-threshold", type=int, default=127)
    p.add_argument("--outside-tolerance", type=int, default=0)
    p.add_argument("--width", type=int)
    p.add_argument("--height", type=int)
    p.add_argument("--report", type=Path)
    return p.parse_args()


def run(args):
    if not 0 <= args.mask_threshold <= 255 or not 0 <= args.outside_tolerance <= 255:
        raise ValueError("Threshold and tolerance must be in [0, 255].")
    if (args.width is None) != (args.height is None):
        raise ValueError("Supply both --width and --height, or neither.")
    base, base_format, _, size = rgba(args.template)
    if base_format != "PNG":
        raise ValueError("Template must be a PNG.")
    expected = [args.width, args.height] if args.width is not None else size
    if min(expected) <= 0 or expected != size:
        raise ValueError("Template size does not match the required dimensions.")
    with Image.open(args.mask) as image:
        image.load()
        if list(image.size) != size:
            raise ValueError("Mask and template sizes differ.")
        brightness = np.array(image.convert("L"))
        mask_alpha = np.array(image.convert("RGBA"))[:, :, 3]
    allowed = (brightness > args.mask_threshold) & (mask_alpha > 0)
    if not allowed.any():
        raise ValueError("Mask contains no editable pixels under this threshold.")
    # Refuse reports that would replace an input asset.
    protected = {p.resolve() for p in [args.template, args.mask] + args.image}
    if args.report is not None and args.report.resolve() in protected:
        raise ValueError("Report path must not overwrite an input asset.")
    results = []
    for path in args.image:
        entry = {"path": str(path.resolve()), "pass": False, "errors": []}
        try:
            data, fmt, mode, image_size = rgba(path)
            entry.update(sha256=sha256(path), format=fmt, mode=mode, size=image_size)
            if fmt != "PNG":
                entry["errors"].append("Image is not a PNG.")
            if image_size != size:
                entry["errors"].append("Image size differs from template.")
            else:
                delta = np.abs(data.astype(np.int16) - base.astype(np.int16))
                outside_delta = delta[~allowed]
                outside_changed = np.any(delta > args.outside_tolerance, axis=2) & ~allowed
                alpha_changed = data[:, :, 3] != base[:, :, 3]
                entry.update(
                    outside_mask_changed_pixels=int(outside_changed.sum()),
                    max_outside_channel_delta=int(outside_delta.max()) if outside_delta.size else 0,
                    alpha_changed_pixels=int(alpha_changed.sum()),
                    changed_inside_mask_pixels=int((np.any(delta != 0, axis=2) & allowed).sum()),
                )
                if outside_changed.any():
                    entry["errors"].append("Pixels outside mask differ beyond tolerance.")
                if alpha_changed.any():
                    entry["errors"].append("Alpha differs from template.")
            entry["pass"] = not entry["errors"]
        except (OSError, ValueError) as exc:
            entry["errors"].append(str(exc))
        results.append(entry)
    result = {
        "schema_version": 1,
        "pass": all(x["pass"] for x in results),
        "template": str(args.template.resolve()),
        "template_sha256": sha256(args.template),
        "mask": str(args.mask.resolve()),
        "mask_sha256": sha256(args.mask),
        "required_size": size,
        "mask_rule": "luminance > threshold and alpha > 0",
        "mask_threshold": args.mask_threshold,
        "outside_tolerance": args.outside_tolerance,
        "editable_pixels": int(allowed.sum()),
        "assets": results,
        "limitations": "Pixel contract only; does not validate face semantics, color projection, skin halos, UV, or game rendering.",
    }
    if args.report is not None:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = parse_args()
    try:
        result = run(args)
    except (OSError, ValueError) as exc:
        print(json.dumps({"pass": False, "input_error": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
