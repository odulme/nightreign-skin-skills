# Runtime module (native plug-in)

Write a native plug-in only when assets cannot do the job: swapping faces by game state, motion where the native cloth no longer fits
the mesh, reading an in-game menu choice, or per-player co-op sync. It costs a lot:
- It is bound to one game build and needs re-proving after every patch.
- It runs only offline (me3, EAC off) or in Seamless Co-op.
- Any bug in it can cost frame time or crash the game.

Assets, params and talk scripts come first (costume_params.md).

## 1. Identity binding

The plug-in must act only on your costume, on a game build it was proven against.

- **Game build.** Check the PE fingerprint at load: timestamp and SizeOfImage, plus a set of RTTI names and short code signatures at
  the sites you read. Verify every proof with a script against the exe on disk, never from memory. On any mismatch, hook nothing, log
  why, and leave the game vanilla. Raw addresses are build-specific: find them again by RTTI name and signature after each patch.
- **Asset identity.** Bind only when the costume row, the body piece, the loaded FLVER's node and render-slot counts, and private bone
  names that only your model has all match. The marker file next to the DLL holds a compiled-in string, not a runtime hash. Bone order,
  model, generated headers, DLL and marker are one set: rebuild and ship them together.
- **Gates that failed.** v005 required a cloth instance the new model does not have: READY and WAIT, never BOUND [game]. v006 gated
  on a per-player field that looked like a hero id; it went from 6 to 29 in the Roundtable and switched the faces off, so v007 logs it
  only [game]. Never make an unproven field a hard gate.
- **Remote players.** Hard condition: a network-driven character whose loaded FLVER has all private bone names. The costume field only
  picks presets [code].
- **NPCs.** Pin the exact CharaInit row. In v022 the wardrobe preview mannequin‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ also wore the costume and took one of the two NPC slots,
  so only one test NPC followed the menu [game].
- **Lifecycle.** Clone the instance's vtable and replace only its matrix-fill slot; call the native fill first, then write your
  private matrices. Never patch the global vtable. Track generations, and unbind on costume change, reload or a player leaving. A
  retired instance passes straight through.

| Log line | Proves | Does not prove |
|---|---|---|
| READY | build fingerprint passed | your costume was found |
| WAIT / *_SKIP stage=... | which identity check failed (stage, actual, expected) | |
| BOUND | this character matched every asset check | anything is drawn |
| RENDER_CONFIRMED | the fill callback wrote your matrices | the right surface is visible |
| FACE | the state machine chose a face | the face looks right (look at the game) |

## 2. State machine and profile

Two layers: the state machine answers what happened (the trigger), and the profile answers which face to show. Presets are keyed by
costume id, so a future costume variant is one more table row. The local ini `[Profile]` overrides the presets, and the menu overrides
both. All three apply to your own character only.

Hajiwo case triggers, highest priority first (tuning choices, not defaults):

| Trigger | Detection | Timing |
|---|---|---|
| Downed | HP <= 1 (a proxy, not full downed-state detection) | while true |
| Ultimate | animation a905_650000 starts, or SpEffect 705010 present | see below |
| Hurt | HP drops | hold 900 ms, 250 ms retrigger cooldown |
| Heavy attack | the wearer's own heavy-attack animations (one-hand, charged, two-hand variants) | while playing + 300 ms |
| Low health | HP <= 25 % | leave at >= 32 % (hysteresis) |
| Rest | calm, and the body still for IdleSeconds (10 s) | until movement |
| Calm | none of the above | |

**Ultimate.** The ultimate is an animation (TimeAct 905650000, 5.33 s in game [game]) plus a lasting state: SpEffect 705010, self
immortality for 15 s [data]. Start on either. While the effect is visible, follow it, relic extensions included. For a teammate whose
effects cannot be read, hold 16.5 s. If the effect does not appear within 2.5 s, the cast was interrupted. v019 had guessed two effect
ids from the animation's events: one was a relic effect, the other does not exist [data]. Ending the face with the animation was also
wrong; the owner wanted it for the whole state.

**Rest** belongs on the worker thread. Hajiwo computed it on the render thread until v021.

**Calibrate, never guess.** Ship a read-only recorder that logs first-seen action and effect ids per player, with a second level that
logs every action change. Have the owner do each action with a 2 s pause, then map ids from that log. Motion clips too: Hajiwo
previews first used walk clips (a000_020000 / 020200) as "sprint"; the sprint loop is a000_020300, with about 55 degrees of pelvis
lean [data].

## 3. Performance: measure, do not blame poly count

Hajiwo case:
- v007 ran at about 30 FPS [game]. v008 cut polygons and micro-optimised the callback from 14.49 to 2.00 us offline [sim].
- In game it still stuttered. The custom callback averaged 19-21 ms, peaking at 42 ms, while the native fill took 15-20 us (in-game log) [game].
  Switching back to the vanilla garb in the same spot restored FPS [game].
- **Root cause:** a per-frame `VirtualQuery` that checked whether the matrix buffer was writable. Its cost grows with the size of the
  committed region past the queried page, and the buffer sat in a heap region of about 1.1 GB; the offline fixture used a 12 KB block.
  Bench [sim]: 0.36 us on a small block, 13.9 ms at the start of a 1 GB region.
- **v010 fix.** The worker checks the region once and caches its range; the render path only compares addresses. An unverified
  buffer keeps the native pose for that frame.
- **Result.** The callback took 25-30 us at 55-59 calls/s; the one-off worker query was 22.1 ms on a 1138.8 MB region (log) [game]. The
  owner confirmed FPS recovered [game].

Rules:
- Time each phase in the real game with aggregated, rate-limited stats; never write a file every frame. A callback count is not an FPS
  counter. Offline fakes say nothing about the game's heap, threads or scheduling.
- Keep the render path free of region scans, blocking locks, file or network IO, and repeated string identity checks.
- A forced-face preview is not a "no plug-in" control, and disabling the whole plug-in also stops the motion. Change one factor per
  test entry.
- Look at GPU causes (overdraw, duplicate face shells, draw calls, textures) only once the CPU is ruled out.

## 4. Secondary motion (v011-v014)

Hajiwo dropped the vanilla cloth files with the new mesh, so motion beyond skinning comes from the plug-in (geometry_rigging.md).

- **v011, limbs around a slowly following neutral pose.** v008 multiplied each limb's whole rotation from the bind pose by a gain (arm
  0.45, leg 0.70). The static arm droop used up the gain: in a sprint the hands moved about 5 cm [sim], and the owner saw "one block"
  [game]. v011 instead keeps a neutral pose per limb (time constant 0.5 s) and amplifies only the swing around it: arm 0.9, leg 1.0,
  caps 50 / 55 degrees. Two more pieces: a foot lift (0.25x, at most 8 cm) and a 5 degree waddle over the stance foot.
- **v012, sprint forward-lean correction.** Arm gain went to 1.35 with a 60 degree cap. With the pelvis as pivot, 65 % of its tilt from
  vertical is taken back: in full up to 65 degrees of tilt, fading to nothing at 95. Rolls and lying poses stay native. The owner
  approved this version [game].
- **v014, veil halves on damped springs.** Two new veil bones take the back cloth, with weights split by height and front/back. Each
  half is a damped spring (1.4 / 1.9 / 2.2 Hz lateral / fore-aft / vertical, damping 0.6, at most 12 cm). It lags the body, is pushed by
  the same-side hand, and bulges out when that‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ hand is behind it. The body twists with the arms (up to 6 degrees), and the waddle went
  to 7. A teleport resets the springs. Checked against a Blender reference [sim]; it has run in game since v015, but no owner verdict on
  the veil is recorded.

**One parameter source.** One file generates the C++ header and the Blender reference data, and tests compare the two. The ini
`[Motion]` section scales each part (0-200 %, 0 = off) and is re-read about every 2 s, so the owner tunes it live.

## 5. In-game settings menu

A talk-script menu gives the native look, pad and keyboard input and FMG text with no input hooks. An overlay was rejected: pads come
through Steam Input, and another Present hook adds GPU-crash risk [inferred].

- **v017: the wardrobe talk script.** The wardrobe button first offered Change garb / expressions / leave; the map-menu Change Garb
  path stayed direct [code]. The owner used the menu in v018 [game]. Weak point: the Roundtable talk binder ships whole. In a large pack
  a map-and-weapons mod owned it, so the menu was rebuilt on that copy with its hash pinned; any other mod shipping it collides.
- **v022: an NPC in front of the fireplace.**
  - The wardrobe went back to vanilla.
  - A new talk member (new id, own Talk button) runs on an NPC part cloned from a vanilla Revenant NPC: talk set, no story placement,
    no entity group. Her loadout is a CharaInit clone wearing the costume.
  - She shows your face for the row you are editing, through a display row stored in spare flag bits. She runs no triggers of her own,
    so she never falls into the idle face [code].
- **MSB group rule.** A part appended at the end of the parts list is not spawned. Insert it inside the Enemy group, after the last
  Enemy; every later part index moves by one and every part reference must be fixed up [game]. Round one seemed to show the appended
  NPC spawning, but only the three grouped ones had. Make each candidate identifiable in the log before concluding.
- **No gravity.** The NPC is not affected by gravity and hung at her MSB height; give the floor height [game].
- **Moving origin.** The game moves the world origin: the same NPC logged at MSB minus (0, 0, 64), later at MSB minus (32, 0, 56), and
  other objects logged in other frames. Convert through a reference with a known MSB position, sampled in the same period. To place her,
  the owner stood on the target spot for 3 s and the logged pelvis was read; the spot took four rounds [game].

**Flags.** Choices are event flags in the save: one flag per (row, face), plus symbol and idle toggles. The plug-in reads them with the
game's own flag reader every 0.5 s and keeps the last choice while they cannot be read (loading). Before taking a range, check that no
event script, talk script or param cell references it. Hajiwo case: 6536 + 8*t + f (6536-6599, 64 flags) for row t and face f.

**The 8 to 15 faces trap.** With eight columns per row, face f >= 8 lands in the next row (8*t + 8 = 8*(t+1)), so a bigger face count
is not enough. Keep old saves meaning the same thing: faces 0-7 stay in the first range, and faces 8-14 go to a second, separately
scanned range (Hajiwo case: 6480 + 8*t + (f-8)). Also check any 64-bit mask, parsers, ini names, text ids and the sync
encoding. Unknown values become the preset. Still open: can a co-op host overwrite a client's menu flags? Thought unlikely [inferred].

## 6. Co-op

None of this has been seen in a real two-machine session: that test was prepared several times and never reported. Read it as design
plus offline tests.

- **Every machine drives every Hajiwo wearer.** Each one finds all players in the game's player set and runs one binding, one state
  machine and one motion state per player [code]. Triggers come from replicated state (HP, animations), so the faces animate without any
  messages. Solo logs show the player set and local binding working [game].
- **Per-player profile.** Your menu, ini and preview apply only to you. A teammate's character uses only the table that teammate sent.
  A shared global face would put A's choice on B and C; an offline three-player test covers this [sim].
- **Private channel.** A small table (faces, symbols, costume, checksum) goes to each session member over `ISteamNetworkingMessages`
  from the game's own Steam API, on a private channel number. It is sent on change, at once to a new‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ teammate, else every 5 s, and
  dropped after 20 s without a refresh. Steam calls are exception-guarded (a fault turns sync off), and `[Sync] Enabled=0` makes none
  [code]. A solo run brought the sync interface up [game]. Logs keep only the last 3 hex digits of a Steam id.
- **Sender to character.** Map each sender to a character through the game's own session table (Steam id to the remote player-data
  block) [code]. Never use array order.
- **Elimination fallback.** Use it only when exactly one remote Hajiwo is unmatched and exactly one unmatched sender says it is wearing
  the costume [code].
- **Unknown means default.** An unmatched character shows its costume preset, never someone else's profile [code].
- **Six-player mods.** A six-player hook DLL that was read leaves the lookup alone [data]. In one pack a hero-fix plug-in changes
  it, as a solo log showed [game], so pairing falls back to elimination [code]. With three or more players and two or more other Hajiwo wearers, their
  picks then fall back to presets, though triggers still animate [inferred]. A pack's LAN / relay mode probably does not carry the
  messages [inferred].
- **Same version for everyone.** Regulation and the Roundtable map differ between versions, so the whole team must install the same
  build. Fields a receiver does not know (from a newer sender) keep its preset [code].

## 7. Hygiene

- **Do not ship debug probes.** The placement logs ran in every map, so they ship switched off in the ini. Keep only read-only,
  rate-limited diagnostics; DLL strings go through the privacy scan too (release_installer.md).
- **Do not reuse another mod's addresses.** A proven reader from earlier work is a starting point only: re-prove every RTTI name and
  signature on the current exe (the NPC finder re-checked 57) [code].
- **Expect other mods in your code sites.** Co-op mods patch code near the lookups you read, so re-check signatures in the real stack.
  In one pack, fix plug-ins touched a site the build check reads, which can trigger a silent refusal [inferred]. Log the failing site.
