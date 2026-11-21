# Reference images and AI base-mesh generation (route A)

Stages S1 and S2 of SKILL.md: turn a pile of reference images into one agreed design, then into an AI-generated base mesh that is worth cleaning up. A successful Tripo task, a nice Blender render and an in-game look are three different kinds of evidence; keep them apart.

Rights first (SKILL.md Step 0). Memes and fan art used as reference belong to their creators: credit them and do not ship their images. A design that borrows from another game's character falls under Step 0 like any port. The hashes and name maps below are for reproducing the work; they are not a rights review.

## 1. Lock the visual contract

Write down, from the references, before any generation:

- silhouette and head-to-body ratio;
- garment layers (what sits over what), patterns, accessories;
- number of hands and feet, cuff and hem structure;
- how the face is drawn (printed lines, 3D features, or both).

Several meme images rarely agree. Choose **one consistent body** and let each other image contribute only what it alone shows (an expression, a back detail). Front, side and back‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ views must show the same character in the same outfit version; never mix two costume variants into one turnaround.

**Ambiguous strokes.** Label each unclear stroke as one of: flat printed feature or outline, real seam, garment edge, or a separate 3D part. If the references do not settle it, offer two or three annotated options or ask the owner one concrete question. This is far cheaper than cutting and patching downstream.

Hajiwo case:
- A chin outline stroke was read as a strap and ended up in the model, and low-resolution eye sockets were read as closed-eye black bars.
- A later attempt to remove the chin band from the fused mesh was cancelled by the owner after review renders: "the more it is patched, the weirder it gets". It was never installed [sim].

**Stylisation is a requirement, not a defect.**
- Keep the big head, the puffiness and the deliberate exaggeration.
- Still complete what the references never show: sleeve roots, wrists, armpits, soles, the back.
- When only a front view exists, mark which back details are your inferred design.

Hajiwo case: the memes had no back view. The back veil, the crown wrapping round the head and the garment thickness were completed from the vanilla Revenant costume's structure, and were labelled as design inference on the board.

**Decide the face strategy now** (materials_faces.md). Hajiwo case: a round 3D head volume with flat printed features: no eyeballs, nose, cavities or mouth interior. One smooth head shell with one face UV layout carries every expression, so Tripo was never asked to generate four heads.

The owner approves the board (turnaround plus expression sheet) before any paid generation. Hajiwo case: the board was drawn with an image-generation model from the four memes and research renders of the vanilla costume. Its prompts were saved next to it.

## 2. Prepare the generation inputs

- **The review board is for people.** It can carry labels, arrows, several views and close-ups.
- **A single-image endpoint** needs one complete subject on a plain background, with no frames, titles, watermarks or cropping.
- **A real multiview endpoint** takes separate, aligned views. Feeding a collage into a single-image endpoint is not multiview input.
- **Keep records:**
  - the original references and their SHA256;
  - what each image contributes (view, body part, expression);
  - every generation parameter.
- **When renaming references,** keep an old-name / new-name / hash map. Never overwrite the originals, and never let review labels or red boxes leak into the generation input.

Hajiwo case: the one‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ multiview task took two clean single-subject inputs, a front and a back view [data].

## 3. Tripo: discover the tools, do not remember them

- Use an existing Tripo MCP server if the session has one. Otherwise read the installed CLI's `--help` and `doctor` output.
- Do not guess API paths, versions or flags from memory. CLI and MCP field names need not match.
- Capabilities seen in one setup (rediscover in yours):
  - balance;
  - history;
  - make (input, output folder, optional model version, scenario and follow-up step);
  - task get and task wait (resume or download by task id).
- The official CLI offered `doctor`, `balance`, `history`, `make`, `task get/list/watch` and `mcp`. Check the current official CLI and API docs for your version. A plan or dry-run mode exists only if your version has it.
- Never spend credits to "test the tool" or run a health check.
- A game-oriented scenario is a candidate setting, not a claim that it matches Nightreign.
- Cinematic polygon counts, auto-rigging and repeated retexturing are not needed. A Tripo auto-rig never replaces fitting the hero's skeleton (geometry_rigging.md).

## 4. Balance, cost and task ids

1. **Account and region.** Confirm the API region, the account and the output root, and reuse an already authorised session.
   - If login needs the user, give them the official authorisation link or code.
   - Never ask for a plaintext key, and never copy a token into notes, checkpoints or packs.
2. **Budget.** Check the real API balance and the task's cost before submitting. Web studio membership credits can be a separate pool from API credits.
3. **Record every task:** input hashes, model version, parameters, task id, status, actual credits, output file, and whether the owner accepted it. The fields below are a project record, not an API schema:

   ```json
   {"input_sha256": ["..."], "model_version": "as-queried", "params": {}, "task_id": "returned-id",
    "status": "success", "credits_consumed": null, "model_file": "work/gen_001/model.glb", "accepted": false}
   ```

4. **A timeout is not a failure.** Once you hold a task id, keep querying that id.
   - Never submit the same paid task again while its state is unknown.
   - An expired download link is fixed by re-querying the original task.
5. **Repeated failure with no new evidence:** record the cause, then change one testable factor or report that you are blocked. Do not keep burning credits.
6. **Disk.** Put outputs on the disk the user chose. CLI caches, downloads and Blender temp files count toward the space plan.

Hajiwo case [data]:
- **Settings.** One multiview task from front and back views: face limit 60,000, textures with PBR on, the "detailed" texture tier (the plan flagged it as a higher price tier), standard geometry, fixed seed.
- **Plan.** The CLI printed the plan before submitting.
- **Run.** Progress sat at 99 % for several polls before success.
- **Cost.** It billed 40 API credits. That is one historical bill, not a price list.

## 5. Import checks in Blender

- Keep the raw GLB/FBX and its textures untouched, and‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ work on a copy. Record the import scale normalisation, units and transforms.
- Before any rigging, check:
  - bounding box and facing;
  - UVs and material count;
  - triangle count and connected components;
  - internal overlaps;
  - texture resolution.
- A live Blender scene driven over BlenderMCP is the user's scene. Read it first, and never clear an unsaved session.
- For audits and renders prefer a background Blender run with an explicit `.blend`, script, output and log; it does not need the foreground.
- Do not upgrade the user's pinned Blender or add-ons to make an import easier. Fix compatibility locally in the project.

Hajiwo case [data]:
- **Shape.** The GLB arrived normalised to a unit box (height -0.5..0.5) with an identity transform: one object, about 35.6k vertices and 59.1k triangles.
- **Maps.** One material with three 4096 maps: base colour, a metallic-roughness (ORM) map and an OpenGL-convention normal map. None of these is in the game's channel layout (materials_faces.md).

## 6. Regenerate, retopologise, or only redraw faces

| Finding after import | Route |
|---|---|
| a few local holes or duplicate shells | repair in Blender; check the back side and real motion (geometry_rigging.md) |
| arms fused into the body, wrong garment layering, topology that cannot deform | retopologise, or regenerate from a revised reference |
| the shape is accepted, only a new expression is wanted | image model on the fixed face template (materials_faces.md); no Tripo |
| you did regenerate | topology, UVs and proportions changed: redo weights, bone order and the face atlas; never carry vertex indices over |

Change one factor per attempt so that each result tests a hypothesis.

Hajiwo case: one generation was enough for the whole project [data]. Every later change was either Blender work on that surface (geometry_rigging.md) or a 2D face edit (materials_faces.md). The full timeline is in hajiwo_case.md.
