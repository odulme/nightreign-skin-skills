# Nightreign Skin Skills

**English** | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md)

A Claude Code skill for making costumes (skins) in ELDEN RING NIGHTREIGN as offline mods: from reference images or an
existing model to a costume that holds up in real play, with optional swappable faces, an in-game menu and an installer that
works on any me3 pack. It is built on methods that worked in game, marks what was only tested offline, and says plainly where results stayed rough. Every
lesson in it was paid for by a costume that looked right in Blender and wrong in game.

> Unofficial fan project. Not affiliated with or endorsed by FromSoftware, Bandai Namco or Anthropic.

## What the skill does

| skill | covers |
|---|---|
| `nightreign-skin` | The whole costume pipeline in ten stages (S0-S9) with an exit gate per stage: visual contract from reference images, AI base mesh with Tripo, Blender cleanup into one continuous body, rigging to a hero's vanilla skeleton and checks with real motion clips, the FLVER export contract and index spaces, materials and channel packing, flat faces on face cards (and how to remove old-face halos), the standalone costume param chain, an optional native plug-in (face switching, secondary motion, NPC menu, co-op sync, frame-time lessons), in-game acceptance, and release as an install-time merge installer. A second route covers porting an existing PMX / FBX / VRM model. |

It builds on **`nightreign-modding`** (me3 profiles and load order, dev overlays, Smithbox and regulation cell edits,
WitchyBND, param recipes, privacy scan, evidence labels), which is published in the companion repository
[Nightreign Boss Skills](https://github.com/odulme/nightreign-boss-skills). Install both.

Claims carry evidence tags (`[game-MP]`, `[game]`, `[code]`, `[data]`, `[sim]`, `[inferred]`) so you can tell what was seen in
game from what was only tested offline or reasoned out. Engine facts were found on Nightreign 1.3.3.0; re-check them after a game
patch. The skill body is in English; its description is Chinese + English, so it triggers in either language.

## The worked example: Hajiwo

Hajiwo (哈基蜗) is a standalone meme costume for the Revenant: a big head, a tiny body and a printed face that changes with
the situation. The skill follows it from four‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ meme images to release:

1. reference board and a turnaround the owner approved;
2. one Tripo multiview generation;
3. a Blender cleanup - the first rig used rigid "doll parts" and was rejected in game for cut faces and double sleeves, the
   accepted version is one continuous body;
4. game files and a standalone costume entry, so the vanilla look stays selectable;
5. flat faces drawn on a fixed template and projected onto face cards (15 faces in the end);
6. a native plug-in that picks faces by situation (calm, hurt, low health, downed, ultimate, idle, heavy attack), sways the
   veil, and is built to share each player's choices in co-op (a full two-machine test is still pending);
7. a face menu hosted by an NPC at the Roundtable fireplace;
8. an installer that merges the costume into whatever me3 pack the player uses.

The case file records the rejected routes and the bugs too (a 20 ms-per-frame plug-in, bones the engine never drove, a
false "pack updated" warning caused by me3 file redirection), because those are where the time went.

A second, shorter case - an anime-game character model ported onto the Recluse - shows the existing-model route. It reached
play, but weapon grip, physics and some materials stayed rough, and the skill says so.

## Where to start if you are new

1. Get the vanilla files out of the game archives (the unpack tools in `nightreign-modding`).
2. Set up me3 with its own save file and a dev profile.
3. Params only: in Smithbox, copy a vanilla costume's chain (Goods -> CharaInit -> Protector -> shop entry + texts) and copy
   the hero's parts files under a new model number, until a new wardrobe entry appears in game.
4. Textures only, on that copy (never on a vanilla file): unpack with WitchyBND, recolour, repack.
5. A mesh: learn rigging and weights in Blender, bind to the hero's vanilla skeleton, export to FLVER.
6. Faces, physics and plug-ins last; they are the expensive parts.

With an agent that can run scripts (Claude Code with these skills), each step is a request; the skill tells the agent what
evidence to show you before anything is installed.

## The hard rule: released games only

The skill begins with a mandatory **Step 0**. Before porting any model, texture, animation, effect or sound from another
game, Claude must:

1. use web search to verify that the source game, or the DLC or update that contains the content, has been officially and
   publicly released and is commercially available, and write down the evidence;
2. **refuse** the port if the game, DLC or character is unreleased, if the material comes from leaks, datamines of
   unreleased builds or betas, or if the release status cannot be confirmed;
3. read the model's own terms - many character‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ models forbid use in other games' mods and redistribution, and a public
   download is not permission.

Costumes from your own designs, AI base meshes from your own reference images (unless they show another game's character), and edits of Nightreign's own costumes are
allowed without this check. Community art used as reference belongs to its creators: credit them and do not ship their
images. Please keep this rule if you fork or adapt the skill.

## Requirements

- **Claude Code** with skills support, and web search enabled (Step 0 needs it).
- **ELDEN RING NIGHTREIGN** on PC (a copy you own).
- **me3** (0.10.1 or later), **Smithbox**, **WitchyBND**, **Blender** 4.x, **texconv** (DirectXTex).
- Depending on the route: **Tripo** (account and credits; MCP server or CLI) and an image-generation model for faces;
  **BlenderMCP** if an agent should drive a live Blender scene; **SoulsFormats** with the .NET Framework C# compiler for small
  builders; **FLVER Editor** (a Nightreign-capable fork); **mmd_tools** for PMX models; **Python** 3 with Pillow and NumPy for
  the helper script; **Seamless Co-op** only for co-op testing.

## Install

Copy the skill folder into your Claude Code skills folder, together with `nightreign-modding` from Nightreign Boss Skills:

```
git clone https://github.com/odulme/nightreign-skin-skills
git clone https://github.com/odulme/nightreign-boss-skills
mkdir -p ~/.claude/skills
cp -r nightreign-skin-skills/skills/nightreign-skin ~/.claude/skills/
cp -r nightreign-boss-skills/skills/nightreign-modding ~/.claude/skills/
```

- Personal skills (every project): `~/.claude/skills/` (on Windows `%USERPROFILE%\.claude\skills\`).
- Project skills (one project only): `<your project>/.claude/skills/`.

Start a new Claude Code session afterwards. The skill loads from its description when you ask about Nightreign costumes or
skins, or you can name it ("use nightreign-skin"). The files are plain Markdown, so you can also read them as a guide.

## Responsible use

- Free, non-commercial mods only. Do not sell, paywall or bundle for sale anything that contains another game's or another
  creator's assets.
- Respect the EULAs and terms of service of the source games and of Nightreign, and the terms of any model you use; extract
  only from copies you own; credit sources when you share.
- Offline only. Run modded Nightreign through me3 with Easy Anti-Cheat off and its own save file. Never take modified files
  onto the official online service or matchmaking: Nightreign uses Easy Anti-Cheat and bans are possible. Co-op in this skill
  means the Seamless Co-op mod or a mod pack's own co-op, which play outside official matchmaking.

## License

Everything in this repository - the documentation and the Python helper script alike - is licensed under the
**Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International** license (CC BY-NC-SA 4.0). Copyright (c) 2026
odulnme. The full legal code is in [LICENSE](LICENSE), and [NOTICE](NOTICE) has the short version:

- **Attribution** is required ("Nightreign Skin Skills by odulnme", a link to the original repository, the license, and
  what you changed).
- **No commercial use**: selling, reselling, paywalling or bundling this material, original or modified, into paid products
  or services is not permitted.
- **ShareAlike**: adaptations must use the same license.

Because of the non-commercial term this is a source-available license, not an OSI-approved open-source license. No game files
and no costume files are included, and the license does‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ not cover any game content or the meme art the Hajiwo costume follows.

## Credits

- Skill written and maintained by **odulnme**.
- The Hajiwo look follows community meme art by the YouTube creator **茹でられた海老**. No image of it is included here.
- ELDEN RING NIGHTREIGN is developed by **FromSoftware**; the game, its content and trademarks belong to FromSoftware and
  **Bandai Namco Entertainment**.
- Tools and services the skill relies on, with thanks to their authors and contributors: **me3** (garyttierney),
  **Smithbox** (vawser), **WitchyBND** (ividyon), **SoulsFormats** (TKGP), **FLVER Editor** and its Nightreign fork
  (asasasasasbc), **Blender** (Blender Foundation), **BlenderMCP**, **Tripo**, **mmd_tools**, **DirectXTex / texconv**
  (Microsoft), **Seamless Co-op** (LukeYui).
- The FromSoftware modding community, whose shared research and documentation made this work possible.

## Disclaimer

This is an unofficial fan project with no affiliation with FromSoftware, Bandai Namco, Anthropic or any of the tool or
service authors. All trademarks belong to their owners. The skill and script are provided as is, without any warranty.
Modding can break saves and, if modified files are taken online, lead to bans: back up your saves and use the skill at your
own risk.
