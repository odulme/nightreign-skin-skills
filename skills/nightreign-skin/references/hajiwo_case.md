# Hajiwo case: v001 to 1.0.1

Hajiwo is a meme-style standalone Revenant costume: a big head, a tiny body, and flat printed faces that change with the situation. This
is the dated record of what was tried, what the owner saw in game, and what was kept, so the next costume can skip the dead ends. Dates
are 2026. The method lives in the sibling files: reference_generation.md, geometry_rigging.md, materials_faces.md, costume_params.md,
runtime_module.md, release_installer.md and acceptance.md.

## Phase 1: from meme to model (10-25)

**Reference images.** The owner supplied four meme images: a smug happy face, shock, crying and near death. The original model was
studied (14 materials, 9 cloth systems, a real face rig). Design decision: a round 3D head with flat printed features, no eyeballs or
mouth cavity. An image-generation model then produced a turnaround sheet and a four-face sheet. Nothing paid ran before the owner
approved them.

**Tripo, 40 credits.** One multiview-to-model job from the approved front and back views, with a textured PBR output [data]. That was
the whole AI-3D spend: there were no re-rolls, and later faces did not use Tripo.

**Blender.** The AI mesh was audited, stray 3D features were removed, and‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ the four faces were baked as full-body 4K colour maps.

## Phase 2: first game builds (10-25 to 10-26)

| Version | Tried | Owner saw in game | Kept / rejected |
|---|---|---|---|
| v001 | Overrode the vanilla body file and renamed the vanilla garb text. "Doll parts": a body on the pelvis, plus short rigid capped hands and feet. Vanilla cloth files dropped. No plug-in. | Too dark; hands separated from the sleeves; leg cut faces visible [game] | Override and doll parts both rejected later |
| v002 | No-light material to brighten it | A glowing, overexposed blob [game] | Rejected |
| v003 | Ordinary lit character material | Too dark at the highest shadow / SSAO settings [game] | Rejected |
| v004 | Exposure-compensated emissive route (materials_faces.md); sleeve roots tucked in | Lighting accepted, confirmed on the v005 build [game] | Kept to the end |
| v005 | Three alternate full-body copies, one per face, hidden inside the main body, scaled out by a plug-in through private bone matrices; switching by HP | Stretch flicker even standing at full HP; faces never switched; the log showed READY / WAIT, never BOUND [game] | Idea kept, build rejected |
| v006 | New bones moved into the active render prefix (they sat after the disabled tail); identity no longer needs a cloth instance; **standalone costume** with its own rows and model | Flicker gone; faces still stuck [game] | Kept |
| v007 | Removed a hard gate on a per-player field that read 6, then 29 in the Roundtable | Faces switch [game]. Then: about 30 FPS, white patches at the sleeve roots [game] | Kept |
| v008 | Doll parts replaced by one continuous closed surface (body, sleeves, hands, feet) with four limb control bones; callback 14.49 to 2.00 us offline | Still heavy stutter; the log showed a 19-21 ms callback [game] | Mesh kept; perf not fixed |
| v009 | Chin-line cleanup by local smoothing and texel remapping | Owner, from renders: the more it was changed, the weirder it got | **Rejected, never installed.** The number is skipped; never use it as a base |

Lessons in the order they came:
1. Offline previews do not prove lighting.
2. A render-slot prefix and an identity gate can each silently disable a plug-in.
3. Capped doll parts read as broken; a continuous surface does not.
4. Offline micro-benchmarks do not prove frame time.

## Phase 3: performance and motion (10-26)

| Version | Tried | Owner saw | Result |
|---|---|---|---|
| v010 | Moved the per-frame `VirtualQuery` off the render path (runtime_module.md) | FPS recovered [game] | Kept; closed the stutter hunt |
| v011 | Limbs swing around a slowly following neutral pose; foot lift; waddle; live ini tuning | Arms too small; the real sprint lean lifts the veil and shows skirt and feet [game] | Revised. The preview had used walk clips as "sprint" |
| v012 | Bigger arm gain; sprint upright correction pivoting on the pelvis | Approved ("great work") [game] | Kept |
| v013 | Wardrobe icon atlas rendered from the model | Not separately reported | Kept for release |
| v014 | Veil split into two halves on damped springs pushed by the hands; body twist; the owner saw a rendered comparison first | Ran from v015 on; no veil-specific verdict recorded | Kept |
| v015 | Every machine drives every Hajiwo wearer; trigger and profile split; read-only id recorder; a two-player test kit | Solo logs fine [game]; the two-player test never came back | Kept; co-op unproven |

## Phase 4: faces and menus (10-27)

- **v016: face cards.** The alternates had been full-body bakes, but only about 900 front-face triangles really differ. Each face
  became a small card over those triangles, grown a few rings so the borders match, angle-unwrapped into one shared 2048 atlas. The
  model package fell from 38 to 12 MB per LOD [data]. Four manga symbols (!, sweat, Zzz, anger vein) face the camera. New faces from
  here on were drawn by an image-generation model on a fixed template and mask, then projected, with no new 3D generation. No
  separate owner verdict on v016 is recorded.
- **v017: in-game menu.** It hooked the wardrobe talk script, stored choices in event flags, and sent each player's table to
  teammates over Steam. It was first used in game in v018.
- **v018: face batch 1, 4 to 8 faces.** Panic, unimpressed, a half-dark manic grin and angry; the atlas grew to 4096x2048. The owner
  saw the menu working and the new faces showing, but colour blocks around them, and asked for the half-dark grin during the ultimate
  [game].
- **v019.** Skin fill by chroma in texture colour space; the template render's colour transform makes eye whites look like skin.
  Added an ultimate trigger. The owner saw it recognised, a 5.33 s animation, but the white blocks around the eyes stayed, and asked to
  keep the dark face for the whole ultimate [game]. The two effect ids guessed for it were wrong [data].
- **v020.** The real cause was a faint warm halo at the rim of the original happy face's eye whites, which the new drawings barely
  changed. Fix: a clean skin base made from what all four originals share, plus recompositing every pixel unique to the happy face.
  This showed up only on a high-pass detail image (luminance minus blur, times 12); flat renders hide it. The ultimate face now lasts
  as long as the 15 s immortality state. No owner check of the halo fix itself is recorded.
- **v021: face batch 2, 8 to 15 faces.** Seven more faces; atlas 4096x4096. The owner chose drool for standing still (with Zzz) and
  toothy panic for heavy attacks. The picker became two pages. Faces 8-14 needed a second flag range (the `8*t+f` trap,
  runtime_module.md). The rest and heavy-attack faces were seen in game‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ only in the final solo test [game].

## Phase 5: standalone release (11-19 to 11-21)

- **Goal (owner):** one package anyone can add to any me3 profile with minimum conflicts.
- **v022.**
  - The wardrobe went back to vanilla. The menu moved to a Hajiwo NPC in front of the Roundtable fireplace who shows the face being
    edited.
  - Placement took four test rounds [game]. Round one was misread: an NPC appended at the end of the part list never spawns; only
    those inserted inside the Enemy group do. The wardrobe mannequin wore the costume and took a binding slot. The NPC is not affected
    by gravity, and the world origin moves.
  - The owner confirmed the final spot [game].
- **v022f.** A thin bright streak on one cheek came from one vertex pair whose normal was 113 degrees off and had been copied into every
  face card. Neighbourhood-averaged normals on 30 vertices fixed it; the owner approved from comparison renders. The 28 other outlier
  normals the scan found were left alone by the owner's choice.
- **1.0.0 (11-20).** Install-time merging installer with a four-language UI and README. One independent audit found a blocker (empty
  `natives = []` lines) among 11 findings. They were fixed and re-checked once. Rehearsal 173/173 [sim]. The
  installer source shipped under GPL-3.0. The folder was frozen.
- **1.0.1 (11-21).** A player reported "NPC there, faces never change"; it is still open (release_installer.md). Reproducing it
  exposed a false "pack updated" warning: me3 redirects the plug-in's read of the game-folder regulation. Fixed in a new version
  folder; rehearsal 183/183 [sim]. The in-game check is pending, so it has no READY.
- **Launcher zip (11-21).** A build for a community launcher pack. The owner's solo test was all OK: player and NPC bound; calm, rest,
  heavy-attack and ultimate faces seen [game]. Co-op untested. The project then paused.

Never shown in a real co-op session: per-player sync, elimination pairing, three to six players. Treat them as design until two logs
from two machines exist.

## If you start a new costume

A face that only looks right on the template is a sticker, not an expression: judge every face on the model, in game.

**Copy these decisions:**
1. Make it a standalone costume from day one: own goods, chara, protector, model, shop row and texts. Scan the target pack for ids.
2. Get owner approval on reference images before any paid generation. Spend one AI-3D job, then fix it in Blender.
3. Build one continuous closed surface for body, sleeves, hands and feet. Keep new bones inside the active render prefix.
4. Settle the lighting route once (an exposure-compensated emissive for flat cartoon colour) and stop touching it.
5. Use flat faces as small cards in one atlas, with new faces drawn on a fixed template and mask. Check them on a high-pass detail
   image.
6. In the plug-in, keep the trigger apart from the profile, and the presets apart from local overrides and the menu. Calibrate every
   animation and effect id from a recorder log.
7. Measure frame time in the real game with phase‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ timing before touching polygons.
8. Put motion parameters in one source file with live ini scaling.
9. Merge at install time: effective copies, add only, a proven inverse, last in load order without moving anyone. Rehearse a case
   matrix and freeze each release folder.

**Avoid these mistakes:**
1. Overriding a vanilla costume file or text (v001).
2. Capped rigid doll parts for limbs (v001 to v007).
3. Brightening with a no-light material (v002).
4. Gating a plug-in on a field you have not proven (v005, v006), or on an asset part your model does not have.
5. Trusting an offline micro-benchmark or a polygon cut to fix stutter (v008).
6. Continuing a route the owner called worse (v009): stop, keep the old version, and do not let a higher number become the base.
7. Gaining limb rotation off the bind pose; previewing "sprint" with walk clips (v011).
8. Guessing effect ids from animation events (v019).
9. Extending a flag layout by bumping a count (v021).
10. Appending MSB parts at the list end; assuming NPC gravity; reading logged coordinates without a reference (v022).
11. Hashing "the base" from inside the game under me3 (1.0.0).
12. Claiming co-op works from solo logs.
