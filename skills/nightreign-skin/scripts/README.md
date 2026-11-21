# Helper script

## validate_face_png.py

A read-only check for flat face images before they are projected onto face cards
([../references/materials_faces.md](../references/materials_faces.md)). It needs Python 3 with‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ Pillow and NumPy.

```
python validate_face_png.py --template template.png --mask effective_mask.png --image face_a.png --image face_b.png --report faces.json
```

For every `--image` it checks:

- the size against the template (`--width` / `--height`, if given, must equal it);
- that pixels outside the editable mask are unchanged (`--outside-tolerance`, default 0);
- alpha;
- the SHA-256 of each file, written to the JSON report.

The editable area is where the mask brightness is above `--mask-threshold` (default 127) and alpha is non-zero. A greyscale
mask with a different convention needs its own threshold.

Exit codes: 0 = all‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ images pass, 1 = an image breaks the contract (an unreadable or non-PNG `--image` counts as one),
2 = invalid template, mask, options or report path. A missing Pillow or NumPy exits 1 with a message.

The JSON report and the printed output record the absolute paths of the files, even if you passed relative ones. Remove them
before you share a report.

It checks pixels, nothing more. It does not draw, resize or repair. It cannot see a skin-colour halo‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ left over from an older
face, a cropped eye corner inside the mask, a wrong UV projection or how the face looks in game. Review every face at full
size and in game; treat a pass as permission to look, never as approval.
