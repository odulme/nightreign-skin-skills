# Acceptance, checkpoints and hand-off hygiene

The owner is the final visual QA. Each layer answers a different question, and none answers the next one.

## 1. Layered acceptance

| Layer | Passes when (examples) | Does not prove |
|---|---|---|
| assets | face PNG check, geometry / UV report, textures decode back correctly | no halo, no flicker, right brightness in game |
| offline | worst frames of real clips, multi-angle renders, read-back of the packed candidate | GPU / SSAO / LOD look, cloth, thread timing, frame rate |
| first in game | the named me3 entry with its hashes loads; the vanilla costume is still there; shape and material visible | cold start, reload, every motion, co-op |
| full experience | real sprint, rolls, attacks, skills; change and reload; quality settings and distance; plug-in rules | player counts or game / pack versions not tested |
| release | the owner's scope; install, repair, uninstall and rollback rehearsed; readme | that an outdated candidate is still installable; anything outside the matrix |

Plug-in status lines in a log only show that a code path ran. Hajiwo case: "ready", "bound", "render confirmed" and "face selected" never stood in for the look or the frame rate.

## 2. Get the minimal loop into the game first

Put the smallest correct costume into the game early, rather than polishing dozens of studio renders. Hajiwo case: the first in-game build was too dark and showed sleeve and leg cuts no render had revealed [game]. High quality means faithful detail on a structure that moves, not more polygons or bigger textures. Show the owner real renders; never present‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ concept art or AI images as Blender renders or screenshots.

Install discipline: candidates go into a separate dev overlay with a manifest, a backup of the entry and a rollback to the last accepted combination (rejected and untested builds are research history). Replace loaded files or plug-ins only after the game has exited; a failed process query is not proof of exit, and never kill the game. Afterwards re-read the entry, re-hash the files, check me3 load order and that no second copy of the plug-in loads. Never launch or drive the game to "accept" a build for the owner. Release mechanics: release_installer.md.

## 3. The discriminating in-game test matrix

| Axis | Variants | Catches |
|---|---|---|
| reference | same spot and camera: vanilla costume, then yours | lighting and material against the scene |
| angle | front, side, back, from above, from below | cut faces, veil interior, hem, soles |
| light | bright outdoor, dark interior | too dark, or a glow blob |
| settings | SSAO and shadow quality low and max | AO and shadow darkening |
| distance | close, far (LOD switch); also seen as an NPC or another player | low-part textures and aliases |
| motion | idle, walk, real sprint, roll, raised arms, combos, skill, ultimate, getting up | stretching, exposed sections, grip |
| session | cold start already wearing it; change to vanilla and back; reload or restart; swap hero; change map | rebinding, leftover state |

Record each cell as passed, failed or untested; a cell not run is never written as passed.

## 4. Extra cells for plug-in features

The rules themselves are in runtime_module.md. The Hajiwo values below are examples.

| Feature | What to test | Hajiwo case |
|---|---|---|
| recovery after damage | the hurt face appears, then returns | held 900 ms, with a 250 ms re-trigger cooldown |
| low HP | enter and exit with hysteresis, no flicker at the edge | enter at 25 %, leave at 32 % |
| downed | top priority; it clears when revived | HP <= 1 used as a proxy, not real downed-animation detection |
| ultimate | the face holds for the whole effect, and ends when interrupted | follows the self buff (15 s) |
| reload, costume change, hero swap | rebinds cleanly; a wrong identity falls back to the default face | - |
| per-player profiles | each player sees each person's own choices; unknown or older teammates fall back to defaults | - |

Hajiwo evidence: ultimate detection and its face were seen in game [game]; the hold over the full 15 s is offline only [sim]; per-player isolation passed three-player offline cases [sim], but no real co-op session was recorded, so co-op stays untested.

## 5. Frame rate and frame time, separately

Measure in game, at the same spot, with the vanilla costume and then yours. A callback count is not an FPS counter.

Hajiwo case: a plug-in callback measured 2 us offline but averaged 19-21 ms in game (peak 42 ms); the owner saw about 30 fps on v007, and FPS recovered with the vanilla costume [game]. Cause: a per-frame memory-region query whose cost grows with the region's size, a GB-scale heap in game against a 12 KB offline fixture [data]. Moving it off the render path fixed it, confirmed by the owner [game]. The offline test was right about its fixture and wrong about the game.

Make each control isolate one factor: disabling the whole plug-in also stops the custom limb bones, so it is not a clean "no plug-in" look; a "force one face" setting still runs the callback, so it is no frame-time baseline.

## 6. Stop stacking fixes

When fixing one problem class, keep‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ what the owner already accepted in the others (such as the lighting). If new evidence cannot tell hypotheses apart, run one minimal A/B that changes one factor. If attempts keep failing while the hypothesis stays the same, stop: save screenshots, logs and the candidate diff, then change the diagnostic method, not the parameter.

Hajiwo case: the lighting swung between glow blob and too dark until the shader's real interface was read (materials_faces.md); the chin-line removal was stopped on the owner's word, never installed, and marked rejected; for the stutter, cutting polygons would not have fixed a CPU stall, but timing each stage found it.

## 7. What a costume CHECKPOINT.md holds

Keep the current state at the top and history below it. Never trust the biggest version number or a "latest" heading in an older document.

- **Current entry.** The me3 profile the owner launches: which packages and natives it loads, their load order, and hashes for the entry, resources and plug-in. State what is installed and what is only prepared.
- **Files.** Inputs, the selected outputs, the baseline and the backups, all with hashes, and where the id-reservation scan came from (costume_params.md).
- **Status, in three groups:** accepted by the owner in game; passed offline only; untested.
- **Rejected and withdrawn routes,** each with a do-not-install marker in its folder, plus the rollback entry.
- **The next smallest check:** where to stand, what to do, and which look or log line decides it.
- **Provenance.** The reference map (original name, new name, hash), generation parameters and task ids, and the delivery scope the owner set.

```text
# Checkpoint - v0NN (date, time zone)
Entry: <profile>.me3 -> packages [...], natives [...]; hashes ...
Installed: ...      Prepared only: ...
Owner-accepted [game]: ...   Offline only: ...   Untested: ...
Rejected (do not install): v0MM chin-line edit ...
Rollback: <entry> -> last accepted combination v0KK
Next check: <one concrete in-game test and what decides it>
```

## 8. Packaging hygiene

- **Model hand-off:** the editable‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ project and its build entry point.
- **Face hand-off:** one PNG per face; template, mask and camera; stable names with the original-name map; prompts, pixel-check reports and integration notes.
- **Import folder.** Put only the selected candidate there and keep old drafts elsewhere, so no rejected face is handed over by accident.
- **After packing,** check the entry count, paths, CRCs and content hashes.
- **Never include in a skill, hand-off or release pack:**
  - login tokens or API keys;
  - account data, user names or absolute paths;
  - unrelated game packs, such as extracted game archives or a third-party mod pack.

  Tool reports may carry absolute paths (the `validate_face_png.py` JSON does). Run the base skill's privacy scan before anything leaves the project.
- **Frozen releases.** A release folder marked ready is frozen; fixes go into a new version (release_installer.md).
