# Materials and flat faces

Stages S5 and S7 of SKILL.md. Hajiwo numbers are examples.

## 1. Read the real material interface first

Before planning a single texture, read the shader, the MATBIN parameter types, the samplers and the FLVER vertex semantics from the target game and a vanilla template material. AI PBR output does not map onto the game's packing. Hajiwo case: Tripo delivered base colour, a metallic-roughness (ORM) map and an OpenGL-named normal map [data]; none was usable as packed.

Channel conventions read from vanilla costumes and a reference skin [data]:

| Texture | Content | Encoding |
|---|---|---|
| `_a` | albedo | sRGB; BC1 in vanilla (BC7 sRGB also used); full mip chain |
| `_n` | R/G normal, **B = gloss** (metal 64-128, skin ~37, cloth 0-30, black cloth 6-12), A = 255 or a mask | linear, BC7 |
| `_m` | metallic; cloth must be 0 (most vanilla cloth pixels are 0) | linear, BC4 |

- The community reports DirectX-style normal green [inferred]; Tripo's map is OpenGL-named. Test the green channel with a known bump in game or against a vanilla map instead of assuming.
- Keep sRGB colour and linear data apart; check normal direction, alpha mode and threshold, mips, TPF format and the low part's `_l` sampler aliases. Decode after compressing and compare.
- Hajiwo case [data]: v001 used 4K albedo with 2K normal/gloss and metallic, BC7 with full mips; albedo read back within 0.43/255 mean error, alpha 251-255 (above the alpha-test threshold), opaque material.
- A fault seen only on NPCs or at a distance is the low part (its textures or aliases), not ambient occlusion.
- Material libraries are merged by member; never overwrite a whole binder, because other mods' members live in it. Ship only the MATBINs your FLVERs reference, checked by reference, not name. Hajiwo case (the v021 build): of 13 extra MATBINs, 7 were in use although their names said "Test" or an old version, and 6 were dead [data].

## 2. Too dark, or a blob of light

**Too dark** under maximum shadows and SSAO: compare with the vanilla costume in the same spot‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ and light, checking base colour, normals, duplicate surfaces, AO, material inputs and shader output in that order. **For a near-unlit or toon look**, check the shader's exposure-compensated colour path and its separate bloom path. Piling on emission is not a diagnosis.

| Hajiwo case | Material | Result |
|---|---|---|
| v002 | an unlit ("NoLight"-type) material | a white glowing blob [game] |
| v003 | back to a normal lit material | still too dark at max shadows / SSAO [game] |
| v004 | glow variant of the vanilla character shader, read from the current game | accepted by the owner, confirmed on the v005 build [game] |

The accepted v004 settings [data]: lit base colour and `g_DiffuseMapColor` RGB at 0, metallic 1, flat normal and low specular, so the lit path adds almost nothing; the albedo reused as emissive map; the shader's intensity float at 0.45 / 15 = 0.03 after reading the shader's own scaling; `g_GlowScale` = [1, 1, 1, 0], where W = 0 zeroes the separate bloom weight while RGB still feeds the exposure-compensated colour. These are one shader's analysed parameters, not a recipe.

Edit only your own material members, never global lighting or shader files. Write down the lighting the owner accepted and do not retune it while fixing rigging or performance.

## 3. The flat-face route

New faces are 2D edits; Tripo is not involved.

1. **Template.** A fixed orthographic camera on the final, stable head renders a base face. Add an editable mask, the existing faces as references, and the saved camera parameters.
2. **One face per edit** with an image-generation model (Hajiwo used GPT image generation). Keep camera, head silhouette, skin, hair and jewellery; change only the printed features.
3. **Interpret low-resolution memes with the owner**, eye rims, pupils, brows and mouth separately. "Blank eyes, no pupils" and "pupils pushed against the rim (eye roll)" are different faces; a printed white dot is not a 3D highlight. Hajiwo case: the owner corrected how one eye-roll face had been read.
4. **Size and records.** Generators do not guarantee the requested size; resize or composite only as the tool's rules and the owner allow. Keep the raw output and the prompt.
5. **Check before projection**: the pixel check, then every face at full size. A pass does not mean the skin matches or nothing was clipped.

```text
Edit the exact base template. Change only the flat printed face graphics inside the visible editable face.
Keep framing, head and chin silhouette, fringe, jewellery and background identical.
Use the supplied meme for the expression only, not for its body pose.
Eye rims: ... Pupils: ... Eyebrows: ... Mouth: ...
No 3D eyeballs, holes, nose or lips, no extra props, text or watermark.
```

**Mask rules.** The mask may be projection coverage that includes pixels behind hair or chains, so the composite must still protect that foreground. Leave margins so a fixed mask never clips eye corners, drool or tears. For a local fix, composite only the eye region and verify the rest is pixel-identical to the previous version. Scripts post-process; they do not draw features the image model was asked to draw.

**`../scripts/validate_face_png.py`**, a read-only contract check (needs Pillow and NumPy):
- Inputs: `--template` (a PNG; its size is the required size, and `--width` / `--height`, given together, must equal it); `--mask` (same size; editable where luminance > `--mask-threshold`, default 127, and alpha > 0); one or more `--image`.
- An image fails if it is not a PNG, if its size differs, if any pixel outside the editable area differs by more than `--outside-tolerance` (default 0, any channel), or if its alpha differs from the template anywhere, inside the mask included.
- Reports changed pixels inside the mask, the largest outside delta and SHA256s. Exit 0 pass, 1 contract failure, 2 bad inputs (also an empty mask). A `--report` path equal to an input is refused; the JSON holds absolute paths, so scrub it before sharing.
- It proves nothing about face meaning, colour projection, skin halos, UVs or the in-game look.

## 4. The old-eye-white halo (the key lesson)

"The new PNG barely differs from the template here" does not prove the area is clean skin.

Hajiwo case:
- New faces showed light patches round the eyes in game [game]. First cause: repainted skin taken straight from the generator, 17-21/255 brighter than the body skin after colour conversion.
- With the skin taken from the body texture, all four new faces still had‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ white ellipses round the eyes [game].
- Root cause: the default happy face's large eye whites had a faint warm-white halo at their edges. The generator's image matched the template there almost exactly (under 0.02 in display space), so those pixels never counted as "changed" and the halo survived; game lighting magnified it. A chroma test had also classified warm eye white as skin.

Method:
1. Best: save a true featureless skin texture at the start.
2. Otherwise estimate a **shared clean skin base K**: pixels on which all original faces agree and which look like skin (they cannot be anyone's features). Dilate the old features, then fill the holes with a smooth fill suited to large holes. Hajiwo case: agreement within 4/255 across four faces, dilation 3, a multigrid harmonic fill (a single-level fill left blocks in big holes), then happy-face skin within 3/255 of K merged and refilled.
3. **Recomposite the union** of the region the new image changed and the region of the old base face's unique patterns, halos included (Hajiwo case: pixels present only on the happy face, 1.5/255 threshold), clipped to the valid template mask so hair and chains stay untouched.
4. Inside that region, features take the generator's colour and skin takes K. Hajiwo split features from skin with a 3x3 median against speckle.
5. Never take a new eye white, or the light ring of an old eye white, as K.

The fix passed an amplified high-pass check and boosted difference sheets with the ellipses gone [sim]; in-game confirmation of this specific fix is not recorded. Thresholds, fill and median are a readable implementation, not constants.

## 5. Colour space of the template

Hajiwo case: the template was rendered with Blender's default AgX view transform, which is display-referred; writing its PNG colours straight back into the albedo produced colour blocks [sim]. Preferred: export the template with the Standard view transform from the start, so template and texture share one space. Otherwise build and validate a mapping from known template-to-texture pixel pairs (Hajiwo case: a cubic polynomial fitted on the four original faces, median error 1.5/255 [data]). Eye white and skin differ very little in AgX template space, so make feature-versus-skin decisions in texture space, by chroma.

## 6. Face cards and the atlas

Keep only the surfaces an expression needs, reuse stable geometry and one material, never duplicate the whole body per face.

| Hajiwo case [data] | Alternate faces built as | Size |
|---|---|---|
| early | full-body duplicates | 157k vertices, 244k triangles, 12 draw meshes |
| v008 | face-only surfaces | 49.7k vertices, 81.4k triangles, 4 draw meshes in all |
| v016 | cards over only the triangles where any face differs, grown by 4 rings | 2,736 triangles each; borders identical in every face, so no seam; each LOD's parts file 38 MB -> 12 MB |

- **UV.** Planar and cylindrical projections flipped triangles because the face contour folds; an angle-based unwrap gave zero flips [data]. Check flips, overlaps, concave areas and borders.
- **Tile size.** Measure real detail first. Hajiwo case: the 4K body bake carried only about 780 px across the face [data], so 1024 px tiles lost nothing (render comparison mean difference 0.23/255 [sim]).
- **Orientation.** Check the projection array's row order and the DDS orientation separately. Hajiwo case [code]: Blender image buffers are stored bottom-up and the rasterised card rows were already in that order, so one more flip would double-flip. Exactly one v flip exists in the whole chain (geometry_rigging.md).
- **Per face, record** a stable semantic name, display name, tile, UV range, node or control id, and whether it replaced an old face.

Expansion from 8 to 15 faces (Hajiwo case; the body texture carries the default face, so 15 faces = 14 cards):

| Version | Atlas | Old content |
|---|---|---|
| v016 | 2048x2048: three alternate faces + a swatch tile for comic symbols | - |
| v018 | 4096x2048 | old half unchanged; old card and symbol UVs scaled u x 0.5 |
| v021 | 4096x4096, seven new faces, one tile empty | old half unchanged; old UVs scaled v x 0.5 |

When an atlas grows, transform every old face and symbol UV, verify the old‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ tiles decode identically, check padding, mips (13 levels at 4096 wide, BC7 sRGB) and every LOD. Each new face is a new node in the render prefix (geometry_rigging.md); menu, sync and packing limits can hit old ceilings (runtime_module.md).

**Inactive faces.** Hajiwo stores each alternate card shrunk to 1/64 around its control bone inside the head, so without the plug-in nothing shows and the default face never depends on it. The plug-in expands the selected card through that bone's matrix; the card sits about 0.5 mm above the base face along the normal, which avoids z-fighting. Validate any hiding method against indices, bounds, materials and the low LOD. No state may leave a fragment of the previous face, and in co-op only the matching player's model switches.

## 7. QA of faces

- Zoom in on the old eye outline, skin differences and edges; also judge at normal size.
- High-pass detail check: luminance minus a Gaussian blur, amplified (Hajiwo case: x12); patch borders show up.
- Keep real graphics (white eyes, teeth, printed dots, grey tears, drool); do not over-denoise. Hajiwo case: light isolated noise dots in generated skin were restored to clean skin; faint spots already in the original texture are not new defects.
- Projection: the pattern lands on the card; check front and three-quarter views for occlusion and seams.
- After mips and BC7, thin overlapping lines and small pupils must stay legible. Hajiwo case: BC7 decode mean error 0.2/255 [data]; legibility is still judged by eye, at a distance in game.
