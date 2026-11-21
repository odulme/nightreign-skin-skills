# Geometry completeness, rigging and the export contract

Stages S3 and S4 of SKILL.md. "Hajiwo case" numbers are examples from one chibi costume, not defaults.

## 1. Isolate, then fix

Hide the other layers, show wireframe, material ids and weights, and split by connected component to see which piece is body, sleeve, hand, foot, veil, or leftover vanilla geometry (a donor costume's unwanted meshes must not be exported).

| Symptom | Discriminating check | False fix |
|---|---|---|
| double sleeve, lump behind the hand | isolate old part, new part, body remnants, inner caps; pose each with raised arms | another sleeve glued over the old one |
| white plate when the arm is raised | material id, normals, cap faces, still weighted to the torso? | a white cover over the cut |
| running legs look like cut-off columns | is the leg connected up inside the hem? soles, knees, occlusion in motion | shortening the visible part |
| "missing chunk" at the eye corner | mask clipping vs hair occlusion vs face-card border / UV vs real missing triangles | painting it all as missing colour |
| stretching flicker while standing still | final bone indices, the active render prefix (section 6), duplicate surfaces, runtime writes | recomputing normals, thickening the mesh |
| extra strap under the chin | back to the 2D reference: line or structure? | deleting and refilling the fused mesh until it distorts |
| thin bright streak under top light | stored normal vs its neighbours' average; copies of that vertex in overlays | sculpting a "dent", painting it out |

Hajiwo case, the streak: one vertex pair had a stored normal about 113 deg off its neighbours, copied into all 14 face cards [data]. Averaging the neighbourhood normals on 30 vertices removed it in renders the owner approved [sim]; an in-game check is not recorded.

**Completing a garment.** Bridge or retopologise the sleeve root into the body, keep armpit edge loops, weight continuously. Cuffs get thickness and an inside, no visible cap plate. Hands and sleeves may be separate pieces, but no motion may expose an amputation face or a second arm.

**Closed is not connected.** Closed doll parts can still come apart in motion; an open boundary at a garment opening or hair card is not automatically an error.

## 2. Continuous body versus closed doll parts (Hajiwo case)

**v001, doll parts.** Soft weights (long stretched strips) and a coarse triangle partition (ragged borders) were dropped first. The first in-game build then used five closed parts: body rigid to the Pelvis, short hands following their bone at 0.12, feet at 0.75, at most 2 influences. Offline it was perfect on paper: zero boundary‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ and non-manifold edges, maximum edge-length ratio about 1.003 [sim]. In game the owner saw cut faces and double sleeves: hands apart from the sleeves, legs ending in cut sections [game]. Removing shoulder spheres and 207 exposed cap faces [sim] still left white plates at the sleeve roots [game]. The owner's rule: body, sleeves, hands and feet are connected; never cut limbs off and cap them to move the arms.

**v008, continuous body**, rebuilt from the accepted Tripo outer surface as one closed surface: one component, zero boundary edges and degenerate triangles, consistent winding, identical weights across every UV seam, confirmed by read-back [data]; 29.4k vertices, 58.9k triangles. Posed renders looked right [sim], which is not an owner sign-off for every motion.

Lesson: watertight counts say nothing about cuts in motion; judge completeness posed, from behind and below.

## 3. Two rigging routes

**Proportions close to the vanilla hero.** Map to the vanilla skeleton (rest pose, units, root); transfer weights from the vanilla body by nearest neighbour, fill zero-weight vertices, smooth the armpit, hip and crotch transitions. Helper bones (Hip, Knee, Twist) move in game but not in a Blender preview; preview them at about half the main bone's angle (a heuristic, not a measured rule). Check the grip dummies with vanilla motions.

**Extreme chibi (head and body in one).** Try normal skinning first and look for a squashed face or stretched limbs. If needed, add a few custom control bones with limited local swing, keep cloth weights continuous and clamp the source motion's angles, instead of cutting limbs and floating spheres or cylinders. Custom drivers are the price of this shape, not a plug-in every skin should ship.

Hajiwo case:
- Four limb control bones pivot at the mascot's own shoulders and hips, driven by the plug-in from the hero's upper arms and thighs (runtime_module.md); the tall human's distal joints as pivots would drag the short sleeves.
- A static gain on the whole angle from bind pose let the arms' hanging offset eat the swing; the owner saw a body that "moved like one block" [game]. Amplifying only the swing around a slowly following neutral pose fixed it, and the owner approved the motion [game].
- The real sprint leans the pelvis far forward and lifted the veil off skirt and feet. A limited correction pulls the lean back within a band and fades out beyond it; rolls and downed poses are untouched. Any loss of grip accuracy is decided with the owner, together with the look.

**Faces.** Keep the flat‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ face on a stable surface. The vanilla face carries Jaw, lip and eye bones [data]; a printed face must not follow them. Veil and skirt may have secondary motion, but the face print never shares those weights.

**Physics.** The base skill's "a custom mesh cannot get physics" is outdated: a later port rebuilt Havok cloth for a custom mesh from a vanilla-compatible template [game]; it is expert work (model_port.md). Hajiwo shipped without Havok cloth: the vanilla `_c.hkx` / `_c.clm2` were left out, because the vanilla veil cloth does not fit the new mesh [data], so the veil hung rigid until the plug-in computed a spring sway on two added veil bones (runtime_module.md).

## 4. Check motion with real clips

Static and hand-made extreme poses complement real clips, but only real clips show what players see. **Identify each clip by measurement, not by its id.**

Hajiwo case [data]: `a000_020000` and `a000_020200` are walk and slow walk, yet an early preview used them as "running". The real sprint loop is `a000_020300` (about 0.5 s cycle, mean pelvis lean about 55 deg, thigh swing about 100 deg); `020210` is a jog (about 28 deg), `020310`-`020330` are sprint variants, `020500` leans to about 93 deg. Classifying clips by pelvis lean and thigh range settled this; the owner's in-game screenshot of the over-leaning sprint [game] was reproduced offline only with `020300` [sim].

Cover idle, turning, walk, jog, real sprint, raised arms and combos, roll, getting up, skill, ultimate, weapon switch. Save each class's worst frame; look at armpit, behind the sleeve, inside the veil, hem and soles. Compare edge-length and area ratios against bind pose with quantiles and report where the extremes are. No single threshold proves "no stretching": thick-cloth folds can be fine, needles, jumps, inverted triangles and exposed sections are not.

| Hajiwo case [sim] | max edge ratio | 99th percentile |
|---|---|---|
| offline test poses (v008) | 1.91 | 1.21 |
| real sprint (v012, plug-in limb motion on) | 2.32 | 1.37 |
| jog / walk (v012) | 2.35 / 1.82 | 1.36 / 1.16 |

## 5. The export contract

The exporter or builder you actually use defines axes, units, transforms, winding, UV direction, normal and tangent sign, material slots and weight limits. Settle each once, write it into the project, verify it by read-back.

| Item | Rule / check |
|---|---|
| axes | Blender Z-up facing -Y; FLVER Y-up. Hajiwo case [code]: position and normal written as (x, z, y) in model units (Blender metres / the hero's character scale, 0.85 for that build) |
| transforms | bake each object's world transform into its mesh (inverse armature world x object world), identity matrix, parent to the armature; FLVER Editor ignores node transforms |
| winding | an axis swap mirrors the mesh, so triangle order is reversed once [inferred]. Hajiwo case [code]: index order reversed per triangle; read-back checks consistent winding |
| tangents | Hajiwo case [code]: bitangent sign negated with the axis swap |
| UV | Blender's UV origin is bottom-left. Hajiwo case [code]: v -> 1 - v, exactly once in the whole chain (atlas notes: materials_faces.md) |
| weights | <= 4 influences, drop tiny ones (base skill: < 1.5 %), renormalise; zero-weight vertices collapse to the origin in game; export only bone vertex groups (others become bones). Hajiwo case: native UByte4 indices, <= 2 positive weights on the body, 3 on the veil |
| culling | vanilla cloth face sets are double-sided; FLVER Editor imports default to culling; face materials keep culling |

Re-check weight sums, index ranges and finite values after quantising. Do not weld every UV seam, recompute all normals or enable global culling without evidence. The FLVER Editor FBX route and a SoulsFormats builder (Hajiwo) need the same items; re-derive them for yours.

## 6. FLVER Nodes, BaseSkeleton, AllSkeletons, HKA

| Index space | Meaning |
|---|---|
| FLVER Nodes | every node in the file, including a tail of Disabled helper nodes; links and dummies refer to it by index |
| active render prefix | the leading nodes the engine gives render matrices; vertex bone indices must stay below it |
| BaseSkeleton / AllSkeletons | hierarchy tables with their own order and parent differences; keep each one's semantics |
| HKA (skeleton in the anibnd) | what animations drive; linked to the FLVER by bone name, not index |
| runtime matrix array | what a plug-in can write; its length is the render prefix, not the node count |

A bone in the file is not necessarily a rendered, writable slot. Hajiwo case, "new bones in the Disabled tail are not rendered": the vanilla body file had 257 nodes, a 204-node active prefix plus a 53-node Disabled tail, and the HKA 197 bones [data]. v005 appended four expression nodes at 257..260, behind the tail; in game there was local stretching and flicker while standing at full HP, and faces never switched [game]. v006 moved them to 204..207 (render prefix 208, 261 nodes), shifted the tail, updated Nodes, BaseSkeleton and dummy references together, kept AllSkeletons' own hierarchy and‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ every vertex index below 208; an inverse permutation reproduced v005 byte for byte [data]. The owner confirmed the flicker gone [game].

Rules: new nodes go at the end of the active prefix, before the Disabled tail; update every link, weight, dummy and control-table reference; append HKA bones keeping original names, parents and reference pose; prove the original bones unchanged (inverse mapping, per-name matrix and weight comparison). Never copy Hajiwo's node counts or another plug-in's write range.

## 7. Read back after packing

Unpack the installed high and low parts and check connectivity, seam weights, index ranges against the render prefix, the HKA and bone tables, material and texture references and sampler names (the low part needs `_l` aliases). Render from the read-back data and confirm it matches the reviewed `.blend`; record expected high/low differences. Hajiwo case: the v008 read-back verifier failed the package unless the body was closed, manifold, consistently wound, one component, free of degenerate triangles and seam-consistent [code]. Such gates catch export regressions; they do not replace the in-game matrix (acceptance.md).
