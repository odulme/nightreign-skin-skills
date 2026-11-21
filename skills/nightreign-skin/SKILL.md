---
name: nightreign-skin
description: "MUST verify the source game is publicly released before porting a model from another game (web search; refuse unreleased, leaked or unconfirmed sources; own designs OK). 移植其他游戏的模型前必须先联网核实源游戏已正式发售，否则拒绝。为《艾尔登法环：黑夜君临》(ELDEN RING NIGHTREIGN) 制作离线 me3 服装/皮肤 MOD：参考图 → AI 生成三维模型（Tripo）→ Blender 修整、绑骨、权重 → FLVER / TPF / MATBIN 打进 partsbnd → 独立新服装参数链（Goods / CharaInit / Protector / 商店 / 文本 / 图标）→ 平面表情脸卡 → 可选运行插件（表情切换、次级摆动、局内菜单、联机同步）→ 安装时合并的独立安装包。以哈基蜗（复仇者梗图服装）为完整案例；另附现成模型（PMX / FBX / VRM）移植路线。触发词：做皮肤、做服装、换模型、二游角色、MMD 移植、Tripo、绑骨、权重、袖子断开、拉伸闪烁、表情、脸卡、黑眼白、过暗过曝、握持悬空、独立安装包。English: Nightreign costume / skin mod - reference board, Tripo, Blender cleanup, rigging to a hero skeleton, FLVER export contract, MATBIN, flat face cards, expression plug-in, standalone costume params, install-time merge installer, PMX port."
---

# Nightreign costumes (skins), from reference image to release

## Step 0 - MANDATORY before porting anything from another game: released games only

This step comes first and is never skipped, shortened or assumed done. It applies whenever a costume would use a model,
texture, animation, effect or sound taken from another game (including models of game characters redistributed for MMD or
other tools):

1. **Verify with a web search** that the source game - for DLC or update content, that exact DLC or update - has been
   officially and publicly released and is commercially available. Do not rely on memory or on the user's word alone. Write the
   title, the release date and the source you checked into your reply or plan.
2. **Refuse and explain why** when the game, DLC or character is announced but not on sale, when the material comes from a
   leak, a datamine of an unreleased build or update, a press build or a beta / network test, or when the release status cannot
   be confirmed (then ask the user to enable web search or name an official source; do not continue on a guess).
3. **Read the model's own terms.** A downloadable character model is not permission. Many distributions forbid use in other
   games' mods, modification or redistribution; tell the user what the terms say before any work, and never help strip
   credits or licence files.
4. **Allowed without a source-game check:** costumes from the‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ user's own designs and assets (or assets they hold the rights
   to), AI-generated base meshes from the user's own reference images (when those images show another game's character or
   costume, that game must pass items 1-3 first), and recolours or edits of Nightreign's own costumes.
   Community art used as reference (memes, fan art) belongs to its creators: credit them and do not ship their images. Credit is not permission: when the costume itself copies a creator's
   character design, ask the creator before sharing it.
5. Repeat the check for every new source.

Example: a request to port the Saltglass Courier of Brackenmoor from a game that has only been announced is refused until the
game is on sale, however complete the leaked model looks.

## Responsible use

- Free, non-commercial mods only. Never sell, paywall or bundle for sale anything that contains another game's or another
  creator's assets, and do not help anyone do so.
- Offline only. Modded Nightreign runs through me3 with Easy Anti-Cheat off and its own save file; never take modified files
  onto the official online service or matchmaking (EAC; bans are possible). Co-op here means the Seamless Co-op mod or a
  mod pack's own co-op, which play outside official matchmaking.

## About this skill

This skill covers the costume itself: design, mesh, rig, materials, faces, game files, optional runtime plug-in and release.
It builds on `nightreign-modding` (me3 profiles and load order, dev overlays, Smithbox / regulation cell edits, WitchyBND,
the param recipes, privacy scan, evidence labels), published in the companion repository Nightreign Boss Skills. Install both.
One correction to that base skill: its line "a custom mesh cannot get physics" is outdated - a later port rebuilt Havok cloth
for a custom mesh from a vanilla-compatible template [game]; it is expert work (see
[references/model_port.md](references/model_port.md)).

The worked example is **Hajiwo** (哈基蜗), a standalone meme-style costume for the Revenant: four meme images, one Tripo
multiview generation, a Blender cleanup into one continuous chibi body rigged to the Revenant skeleton, flat printed faces
(15 in all: the default on the body texture, 14 on face cards), a native plug-in that swaps faces by situation, sways the veil
and is built to sync each player's choices in co-op (never tested on two machines), a face
menu on an NPC at the Roundtable fireplace, and an installer that merges the costume into any me3 pack at install time. Its
numbers are examples, never defaults: [references/hajiwo_case.md](references/hajiwo_case.md).

Engine facts (node tables, animation, effect and flag ids, plug-in checks) were found on Nightreign 1.3.3.0; re-verify them after
a game patch.

Evidence tags on claims: `[game-MP]` seen in a real co-op session > `[game]` seen in game by the owner > `[code]` > `[data]`
read from files > `[sim]` offline render / simulation > `[inferred]`. Offline checks find causes; they never prove a fix.

## 1. Pick the route

| route | when | cost and risk |
|---|---|---|
| **A. Reference images -> AI base mesh -> Blender** (Hajiwo) | an original look, a meme, a stylised or chibi body, no usable model exists | paid generation; the mesh needs real cleanup; proportions are yours to choose, so grip and motion can be designed in |
| **B. Port an existing model** (PMX / FBX / VRM) | a finished character model exists and its terms allow it (Step 0) | proportions rarely match the hero: floating weapons, long cloth, materials; the one worked case reached play but stayed rough ([model_port.md](references/model_port.md)) |
| **C. Edit a vanilla costume** (recolour, texture, small mesh edits) | learning, or a variant | cheapest; the best first project |

Choose the target hero by body proportions first: a body close to the hero's arm length and height avoids the hardest
problem (weapon grip). A standalone new costume is better than overriding a vanilla one: the vanilla costume and‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ any
third-party costumes stay selectable, and uninstalling is clean ([costume_params.md](references/costume_params.md)).

## 2. Pipeline with exit gates

Each stage ends with evidence. The owner is the final visual QA: show renders before installing, install only after an
explicit OK, and keep every rejected route recorded so it is not retried.

| stage | do | exit gate | reference |
|---|---|---|---|
| S0 scope | route, hero, standalone vs replace, Step 0, approval points, budget for paid generation | written scope; rights checked | this file |
| S1 visual contract | one consistent body from all references; mark every ambiguous stroke (flat drawing, seam, separate part) | owner approves the reference board / turnaround | [reference_generation.md](references/reference_generation.md) |
| S2 base mesh | Tripo multiview (route A) or import (route B); record task id, inputs, cost | import audit: scale, axes, parts, UVs, holes, duplicates | [reference_generation.md](references/reference_generation.md), [model_port.md](references/model_port.md) |
| S3 geometry | complete, continuous body: sleeve roots, wrists, armpits, soles, back; no cut faces or second sleeves | multi-angle and posed renders approved | [geometry_rigging.md](references/geometry_rigging.md) |
| S4 rig | bind to the hero's vanilla skeleton; <= 4 weights, no zero-weight vertices, smooth joints | real motion clips (walk, real sprint, roll, attacks, skills, getting up) without stretching or exposed sections | [geometry_rigging.md](references/geometry_rigging.md) |
| S5 materials | read the real shader / MATBIN interface; pack channels; BC formats with mips | decoded read-back matches; light / dark preview sane | [materials_faces.md](references/materials_faces.md) |
| S6 game files | FLVER + TPF into high and low parts; standalone param chain, texts, icon; dev me3 overlay | owner sees it in game in the dev profile; vanilla costume still there | [costume_params.md](references/costume_params.md), [acceptance.md](references/acceptance.md) |
| S7 faces (optional) | flat faces drawn on a fixed template, projected onto face cards in an atlas | pixel checks + full-size review; no old-face halo | [materials_faces.md](references/materials_faces.md) |
| S8 plug-in (optional) | only what assets cannot do: face switching, secondary motion, menu, co-op sync | identity binding proven; frame time measured in game; per-player isolation | [runtime_module.md](references/runtime_module.md) |
| S9 release | installer or pack import zip; four-language readme; privacy scan; one audit + one re-check | rehearsal matrix passes; release folder frozen | [release_installer.md](references/release_installer.md) |

Get a minimal correct costume into the game early (end of S6) instead of polishing dozens of offline renders: the game
shows problems no preview shows (lighting, LOD, real motion, frame time).

## 3. Hard rules (traps already hit)

- **One continuous body.** Rigid "doll parts" that are each closed and watertight still showed cut faces and double sleeves in
  motion; the owner rejected them [game]. Closed is not connected, and a watertight check is not a completeness check.
- **Real clips, correctly named.** Check the real sprint clip, not a walk or jog labelled as sprint; save the worst frame of
  every clip type. Static T-pose renders prove little.
- **Weights:** at most 4 influences per vertex, renormalised after quantising; no zero-weight vertices (they collapse to the
  origin); only bone vertex groups are exported (other groups become bones).
- **New bones must be in the rendered range.** Bones added at the disabled tail of the FLVER node table are not driven by the
  engine: Hajiwo's face stretched and flickered while standing until they moved [game]. Nodes, BaseSkeleton, AllSkeletons and
  the HKA skeleton are separate index spaces.
- **Clothing is double-sided** in vanilla (no backface culling on cloth face sets); imported meshes default to culling and
  show the background through every gap. Face materials keep culling.
- **Read the material interface** before making textures: `_a` sRGB albedo, `_n` RG normal + B gloss, `_m` metallic (cloth 0),
  as the vanilla template actually packs them (an emissive cartoon material may set metallic on purpose; see
  [materials_faces.md](references/materials_faces.md)). Do not fix "too dark" or "glowing blob" with more emission; compare against
  vanilla under the same light and settings.
- **Flat faces are images, not geometry.** Draw new faces on one fixed template; never regenerate a whole head for a new face.
  Rebuild clean skin from what all faces share, or old eye-white halos survive and glow in game [game].
- **Never trust the biggest version number.** The live combination is what the me3 profile actually loads; a rejected
  experiment (Hajiwo v009, a chin-line edit) must not become the baseline.
- **Plug-ins:** never scan memory regions on the render path (Hajiwo v008 spent 19-21 ms per frame in one system call; fixed
  in v010 [game]); bind to a proven identity; each remote player gets only their own settings; unknown means default.
- **Co-op:** every player must install the same version of the costume; mixed installs break params and maps.
- **Dev first, then pack.** A change is confirmed in the dev profile before it goes into anything others install; a release
  folder marked ready is frozen, and fixes go into a new version.
- **Never launch or drive the game** for the owner; prepare candidates while it runs and‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ install only after it closed.

## 4. Tools

me3 (mod loader, own save file), Smithbox (params, texts), WitchyBND (unpack / repack), SoulsFormats (small C# builders and
checks), FLVER Editor (Nightreign-capable fork) or a SoulsFormats-based exporter, Blender 4.x (headless scripts; BlenderMCP
when an agent drives a live scene), Tripo (route A base mesh, via its MCP server or CLI), an image-generation model for flat
faces, texconv (DirectXTex), mmd_tools (route B, PMX). Paths and versions depend on the user's setup; discover them, do not
assume them.

## 5. A learning order for people starting out

1. Get the vanilla files out of the game archives with the unpack tools of `nightreign-modding` (its section 0), so you can
   read the hero's parts files and params.
2. me3 with its own save file: run a dev profile that loads one empty package (`nightreign-modding` section 1).
3. Params only: copy a vanilla costume's chain in Smithbox (Goods -> CharaInit -> Protector -> shop entry + texts) and give it
   its own model number by copying the hero's parts files (high and `_l`) to a new `bd_m_<id>` name, until the new costume shows
   in the wardrobe ([costume_params.md](references/costume_params.md); the base skill's `references/params.md`).
4. Textures only, on that copy (never on a vanilla parts file): unpack it with WitchyBND, recolour the albedo, encode with mips,
   keep the low-model texture aliases, repack ([materials_faces.md](references/materials_faces.md) section 1).
5. A mesh: learn Blender rigging and weights, bind to the hero's vanilla skeleton, export to FLVER, read it back
   ([geometry_rigging.md](references/geometry_rigging.md); the base skill's `references/model-pipeline.md`).
6. Only then faces, physics and plug-ins - the expensive parts.

## References (read on demand)

| file | covers |
|---|---|
| [reference_generation.md](references/reference_generation.md) | visual contract, reference board, Tripo generation and records, import audit |
| [geometry_rigging.md](references/geometry_rigging.md) | completeness diagnostics, continuous body, rigging routes, real-clip checks, export contract, FLVER index spaces |
| [materials_faces.md](references/materials_faces.md) | material interface, lighting problems, flat faces, halo removal, colour space, face cards and atlas |
| [costume_params.md](references/costume_params.md) | standalone costume param chain, id scanning, texts, icon |
| [runtime_module.md](references/runtime_module.md) | optional plug-in: identity, state machine, performance, secondary motion, NPC menu, co-op sync |
| [release_installer.md](references/release_installer.md) | install-time merge installer, me3 redirection, launcher zips, licences, privacy |
| [acceptance.md](references/acceptance.md) | layered acceptance, in-game test matrix, checkpoint contents |
| [hajiwo_case.md](references/hajiwo_case.md) | the Hajiwo timeline: what was tried, kept and rejected |
| [model_port.md](references/model_port.md) | route B: porting a PMX / FBX / VRM model, and why the worked case stayed rough |
| [scripts/README.md](scripts/README.md) | `validate_face_png.py`, a read-only check for drawn faces |
