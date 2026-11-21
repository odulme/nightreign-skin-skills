# Porting an existing model (PMX, FBX, VRM)

The secondary route: put a finished character model on a Nightreign hero instead of building one from reference images (hajiwo_case.md). The one worked case is an MMD (PMX) model of an anime-game character ported onto the Recluse. It reached play after dozens of test versions, and the owner judges the result rough. These are field notes from one hard port, not a recipe.

## 0. Gate

SKILL.md Step 0 applies: models from publicly released games only, from a copy the user owns. Then read the model's own licence and readme before touching it. Many MMD distributions forbid use in other games' mods and forbid any redistribution. A public download is not permission. If the terms forbid the port, stop.

## 1. Inventory the source first

First record the counts of vertices, bones, rigid bodies, joints and materials, plus the textures, transparency and rest pose. Case: tens of thousands of vertices, several hundred bones, a few hundred rigid bodies and joints, a few dozen materials [data].

- Import PMX with mmd_tools. Import FBX or VRM with an importer that really reads their materials; opening is not full support.
- Use one uniform‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ scale plus an axis swap, and no local reshaping. Case: 0.08 suited that PMX's units; it is not a default [data].
- MMD helper bones and vertex groups (IK, twist, D-bones) are not game bones. Resolve them in the export copy.
- Render front, back, side and face previews to find missing textures, black eye whites, coplanar overlay layers and flipped faces. Case: a wrong alpha mode dropped a patch, and coplanar overlays drew black blocks on hair and eyes [sim]. Fix in an export copy; never edit the source files.

## 2. Target baseline

Extract the hero's vanilla high and low parts from the user's install: FLVER, TPF, anibnd / skeleton.hkx and cloth HKX. Check which equipment slot carries the visible arms. Case: the Recluse body part holds the arms, and there is no separate arm part to add dummies to [data]. Confirm from params and files, not file names. Base every param edit on the regulation of the user's real pack, not vanilla. Rows and links: costume_params.md.

## 3. Export to FLVER

- Map source bone names to target names and keep the map in the project.
- Keep at most 4 weights per vertex, normalised, with indices in range.
- Case transform: position (x, z, y), UV v -> 1 - v, reversed triangle winding, tangent handedness flipped [code]. It depends on the importer's axes. Re-derive it for another importer and do not flip twice.
- Rebuild the vertex buffers in the vanilla FLVER's native layout, not a merged layout.
- Give every material its own MATBIN with a correct SourcePath and Key. Make Material.Index run 0..n-1 with no gaps.
- Nodes, BaseSkeleton, AllSkeletons and the HKA skeleton are separate index spaces. HKA links to the FLVER by bone name only. AllSkeletons keeps vanilla parent differences for control and ragdoll bones. Do not force it to equal Nodes, and do not reorder it by HKA order.
- Order the FLVER bone tables parent before child, then re-run every index-based audit on the final file.
- Flag skinning bones as bones, not as disabled, mesh or dummy nodes.
- Check the final FLVER, not the Blender scene (geometry_rigging.md).

The case hit these defects in game, and each needed its own fix:

| In-game symptom | Cause found | Fix | Evidence |
|---|---|---|---|
| White model, flicker, long spikes | merged vertex buffer, missing control data | native buffer layout | [data]; symptoms stayed |
| Grey model | wrong bone flags, texture references | bone flags, one MATBIN per material | [data]; still grey |
| Grey model | MATBIN Key not matching SourcePath, wrong Material.Index, skeleton tables out of sync with Nodes | all three fixed in one version | [game] colours back |
| Huge triangle spikes and flicker at one hand | four finger bones in the highest bone slots | moved to unused low slots, same names and weights | [game] gone; mechanism [inferred] |
| Swollen pinky, even empty-handed | child bones listed before their parents | topological order in Nodes, BaseSkeleton and AllSkeletons | [game] |

Case: the Key was the Adler-32 of the UTF-16LE SourcePath [data].

## 4. Proportions and weapon grip

The hardest problem. Weapons follow the hero's native hand bones [inferred]. When the source arms are shorter or longer than the hero's, the visible hand and the weapon drift apart, and the weapon floats beside the hand. Case: the source and vanilla hands drifted 3-17 cm apart during motion [sim]. Case attempts:

| Attempt | Result | Evidence |
|---|---|---|
| Best uniform scale (offline, 13 animations, 834 frames) | hand error 10.9 -> 10.7 cm RMS, about 1.6 % better | [sim] |
| Whole character +15 % through character scale | bigger, grip no better; rolled back | [game] |
| Extra dummies in the costume FLVER, bound to its hands | no change | [game] |
| Shift the weapon bone in the skeleton | no proven effect | [game] |
| Attachment param experiment | starting staff vanished, casting crashed; rolled back | [game] |
| Move only the palm and fingers | wrist badly stretched; not shipped | [sim] |
| Stretch the arms to vanilla length | hands matched offline [sim]; owner rejected it | [game] |
| Native per-hand plug-in that moves the weapon attachment onto the visible hand | accepted | [game] |

The plug-in first tracked only the player present at startup, so after a hero swap it held a stale owner and weapons floated again. Re-checking the current local owner and rebinding fixed‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ this [game]. Module rules: runtime_module.md. Test a cold start, a hero swap and the swap back.

Lesson: pick a hero whose proportions are close. Decide early whether you keep the source proportions, which costs a runtime fix, or keep the vanilla grip, which costs reshaped arms. Test grip in game in the first playable build: staff, one-handed and two-handed weapons.

## 5. Physics

PMX rigid bodies and joints are not Nightreign Havok cloth; the case found no direct converter. The case built project-side Havok 2018 read and write support. It loads the missing hk2018 types in-process, writes with the source file's own type schema, refuses unknown types and compares object graphs after a round trip [code]. It then rebuilt hcl cloth for the hair chains and skirt panels from a vanilla-compatible template, with simulated chains mapped from the source chains, proxies, anchors, constraints and body collision capsules [data]. The older claim "a custom mesh cannot get physics" is outdated, but this is expert work.

- **Cost.** Case: about a dozen simulations, each at 8 substeps x 32 iterations, where vanilla Recluse cloth uses 1 x 1 [data]. At 2 x 4 per sim the motion stayed and FPS recovered [game]. That the solver settings were the main cost is [inferred].
- **No fake fixes.** A version with the simulation removed froze the skirt [game]. Never report that as a fix.
- **Previews.** Offline PBD previews show stretch and fold trends; they are not Havok [sim].
- **Thin belts.** Long thin belts need their own chains. Case: several thin belts shared the wide skirt bones and flew about [game]. A later candidate pinned most of each belt to the spine with a token weight at the tips [data]; no in-game verdict was recorded.
- **High and low parts.** Use the same physics data in both, and test a cold start without swapping hero.
- **Later rounds** drove braid and skirt bones from a runtime plug-in, with mixed results [game]. Not covered here.

## 6. Materials

Match the real shader, sampler names and vertex inputs; look-alike names are not interchangeable. Test high and low parts. See materials_faces.md.

- **Eye whites** went black in shade, and blanket emission is not the fix. Added glow made the eyes glow [game]. Removing it brought the black eye whites back [game]. Weaker glow went black again, so a brighter compromise was kept [game]. A later non-emissive variant was accepted only with SSAO switched off [game]. No general recipe came out of this.
- **Hair.** A native hair shader swapped in without‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ its extra vertex input made the hair vanish; adding the input restored it [game].
- **Back of the head.** A hard-edged dark patch there was never solved. It survived graphics settings and material rollbacks [game]. Textures, normals, material borders and weights showed no matching edge [data].

## 7. Status of the case

Works in play [game]: look and colours, hand and finger deformation, braid and skirt cloth at acceptable FPS, weapons following both hands after a hero swap, a costume entry and portrait.

Stayed rough:

- the back-of-head patch is unsolved;
- the eye whites trade too bright against black in shade;
- the grip plug-in is bound to one game version and must be re-validated after every patch. In its first co-op test build it served only the local player, so teammates did not get its effects [game-MP].

See acceptance.md for the in-game checks.

## 8. Recommendation

For a first costume, use the Hajiwo-style route (hajiwo_case.md). If you port anyway, choose a model whose proportions are close to the hero's and that has no long cloth. Settle the grip question before anything else, and get a static playable version before physics. Shared rig and export steps: geometry_rigging.md.
