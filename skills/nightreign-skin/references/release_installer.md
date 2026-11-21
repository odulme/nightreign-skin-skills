# Release: a standalone installer that merges at install time

Ship a costume people can add to any me3 setup without breaking it. Scope: free, non-commercial, offline only (me3, EAC off, its own
save file). Co-op only through Seamless Co-op or a pack's own co-op, never official matchmaking. Say so in the README.

## Why merge at install time

A costume with a menu touches shared files: regulation, text binders, the material library, menu atlases, and the Roundtable talk and
map. Whole copies either overwrite the player's pack, losing its content, or fit one pack only. So the installer adds the costume to
the copy of each file the profile really serves, proves every addition reversible, and puts the merged copies into a new package that
loads last. Nothing of the pack is edited.

## Install flow

1. **The player picks their `.me3`** in a file dialog. Start it in the folders where me3 and profile managers usually keep profiles.
2. **Strict TOML read.** A real TOML 1.0 reader with three outcomes: valid, invalid, or unsupported (dates, integers wider than 64
   bits), which is refused, never guessed. Duplicate keys and redefined tables fail. Then read the profile as me3 deserialises it: BOM
   and CRLF allowed, singular or plural table names (one spelling per kind), the `path` / `source` alias, and an optional package id
   (me3 names an id-less package by its joined path). Hajiwo case: cross-checked against Python's `tomllib` and me3's own loader on a
   corpus [sim].
3. **Load order as me3 resolves it.** Port me3's own sort, pinned to a tagged release:
   - listed order plus `load_after` / `load_before` constraints;
   - missing sources dropped;
   - disabled entries sorted with the rest, then dropped.
   The later package wins per path. Constrained packages can move: `[P1, P2, P3 after P1]` loads as P1, P3, P2, so the effective‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ base
   is P2's copy [sim]. Re-diff the sort source on every me3 release.
4. **Load last without moving anyone.** Simulate the sort to find the smallest `load_after` list that puts your package last and keeps
   every other package where it was. Mark entries `optional = true`. An earlier draft added `load_after` on every package, which can
   reorder the others [sim]. The native loads after the Seamless Co-op DLL where that moves nobody; it is optional, so it also works
   without co-op.
5. **Compatibility checks.** Show every check with a plain-language result. Enable Install only when all pass:
   - **Kit:** every kit file present and hash-correct.
   - **Game:** the build matches the kit (PE stamp and SizeOfImage); the game's Oodle DLL and `regulation.bin` are present; the game
     is not running (ignore zero-thread leftover processes).
   - **Profile:** it parses; it is not a launcher-generated profile that gets rewritten at every start; it does not already carry the
     costume (its DLL, its `parts/bd_m_<model>` files, its package id).
   - **Merge targets:** your ids are free in every effective file; row size and param type match; the talk binder lacks your member;
     the map has the model and collision your NPC uses, and no part with your part's name.
   - **Disk:** the folder is writable; there is enough free space.
6. **Merge.** Work on each effective copy and only add. Prove each step: removing the additions gives the input back byte for byte.
   - `regulation.bin`: raw row insertion in id order, for stripped and named tables; untouched PARAM members stay byte-identical
     (costume_params.md).
   - `msg/<lang>/*.msgbnd.dcx`: FMG entry additions in every language folder. With no translation, use English. Keep the input's own
     layout so the inverse is exact.
   - Material library: add the MATBIN members your FLVERs reference.
   - Menu atlases: add one texture and one layout member to both resolutions; create the layout binder if no copy exists.
   - Talk binder: add your new talk member as fixed bytes. Never touch the wardrobe script.
   - Map MSB: insert the NPC inside the Enemy group, after the last Enemy, and shift every later part index (runtime_module.md). Which
     fields hold part indices is data. Hajiwo case: derived structurally from Smithbox's MSB writer and checked byte for byte against
     it on every vanilla map [sim]. On a structure you have not validated, skip only the NPC pair (talk member and map part, all or
     nothing). The costume still installs, and the report says so.
   The report lists every pack file your package now shadows.
7. **Edit the profile.**
   - Back up the `.me3` before each install.
   - Append one marked block at the end.
   - me3's own serialiser writes empty `natives = []` / `packages = []` lines, and appending `[[natives]]` after them gives invalid
     TOML. An audit caught the installer reporting success on exactly that [sim]. Turn such lines into comments, and restore them on
     uninstall.
   - Read the result back: strict TOML, loadable by me3, ours last, nobody moved, exactly invertible.
   - Replace files safely: write a temp file, verify it, swap it in. If the `.me3` is a symlink in the same folder, edit its target.
8. **Receipt and basecheck.**
   - The receipt records version, game build, the profile's hashes before and after, and for each merged file its base (package, game
     folder or shipped vanilla copy) with hashes. Prefer the player's own game files as the base: a shipped vanilla copy means
     redistributing game files.
   - The basecheck file next to the DLL has one line per item. `<sha256> TAB <file>` means a pack file you merged on, or the `.me3`
     itself, must stay unchanged. `absent TAB <file>` means another enabled package must not gain that path. Such an update would carry
     content your stale merge lacks.
   - At start the plug-in compares these lines and warns once per change, keeping a marker so it does not repeat. On a game build
     mismatch it advises uninstalling.

## Repair, uninstall, failure

- **Repair** re-resolves the bases and rebuilds what changed. It re-adds the block if a pack update or a profile manager rewrote the
  `.me3`, then rewrites the receipt and basecheck. Replaced files are kept until the commit. Repair is also the upgrade path:
  1.0.0 to 1.0.1 needed no uninstall [sim].
- **Uninstall** removes exactly the block and restores the commented lines. It deletes the costume folder, receipt last, so a partial
  removal is still detected. An edited ini is saved next to the profile. It works on a mismatched‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ game build. If nothing else changed,
  the profile comes back byte-identical.
- **Failure.** Undo everything you can, then state what is true, read back from disk, not what was intended. An antivirus holding the
  fresh DLL open leaves a folder behind: say "not fully undone"; Uninstall finishes it [sim]. The README gives manual recovery too.

## Install-time rehearsal matrix

Run the release exe headless on scratch profile copies, never the live one. Read every merged file back with independent readers
(Smithbox; SoulsFormats with paramdefs).

| Case | Expect |
|---|---|
| vanilla + Seamless Co-op; vanilla offline; me3's stock default profile (empty arrays, a package without id) | install, then uninstall restores the bytes |
| big map-and-weapons pack; a pack whose tables were written by an editor (named rows) | merge on that pack's copies |
| a profile that already carries the costume; an id or part name already taken | refused, naming the item |
| game build mismatch; read-only folder; exe moved out of its kit | refused with a clear reason |
| hand-written TOML (comments, BOM, CRLF, aliases, disabled or missing packages) | parses like me3 |
| constrained load order | base = me3's real winner, nobody moved |
| map with an unvalidated part structure; map without the NPC model | NPC skipped, costume installed |
| pack folder moved; pack updated after install (file changed or added) | Repair / basecheck catch it |
| fault injection at every write; previous version installed, then Repair | profile intact; upgrade works |
| every UI language | full cycle, profile byte-identical |

Hajiwo case: 173/173 for 1.0.0, 183/183 for 1.0.1 [sim]. A passing matrix is not an in-game check.

## The 1.0.1 false alarm

me3 hooks file access. When the plug-in DLL called `CreateFileW` on the game folder's `regulation.bin`, me3 redirected the read to
the package override, which is the installer's merged copy. So with no package shipping a regulation (me3's default profile, for
example), the plug-in hashed the merged file. It never matched the base hash and warned "pack updated" at every start. Repair could
not clear it. This was found in an in-game log [game].

The 1.0.1 fix: write no hash line for a base that is the game folder's own file. The trade-off: a regulation-only game patch with an
unchanged exe is no longer noticed; the build check still catches every exe change [code]. The 1.0.1 rehearsal passes [sim], but the
in-game confirmation of 1.0.1 was still pending when work paused.

Rule: in the game, a plug-in sees files as me3 serves them, so an in-process read never proves what is on disk.

## Distribution

- **README in four languages** (zh-CN, zh-TW, en, ja, matching the installer UI): what it does, install, backup, uninstall, when to
  Repair, after a game update, manual recovery, what the unsigned exe does and does not do (SmartScreen warns), limits, the co-op rule,
  license, credits. The owner reviews machine-written translations.
- **GPL-3.0 when the installer uses SoulsFormats.** SoulsFormats is GPL-3.0, so Hajiwo shipped the installer as GPL-3.0-or-later:
  complete source, a build script, the license text and third-party notices. The costume files and the plug-in DLL are separate works
  aggregated in the same archive. GPL-3.0 requires the Corresponding Source of the exact build you ship, so build SoulsFormats from a
  pinned commit and ship or link that source. (Hajiwo 1.0.0 shipped an existing binary whose revision could not be determined, and
  its notices say so.) Not legal advice.
- **Privacy scan of every shipped file,** inside DCX and binder layers too, and of DLL strings in UTF-8 and UTF-16. Look for absolute
  paths, user and account names, private hosts and links, and wording about the author's own computer. One release DLL was rebuilt only to change log
  wording. Record known chance matches in compressed texture bytes so later scans can be compared.
- **Frozen release folder.** After the final checks, write a READY marker into the version folder. From then on nothing in it
  changes; any fix goes into a new version folder. Hajiwo case: 1.0.0 is frozen. 1.0.1 is built and rehearsed, but without READY,
  pending its in-game check.

## Packaging for a community launcher

Some launchers import a zip with a manifest instead of a `.me3`. Generic shape:
- id, version, and components: a content component rooted at `mod/` and a native component pointing at the DLL, both required, ordered;
- an `incompatibleWith` list;
- a readme.

Build the content with the same merge engine on a temporary profile whose only package is the launcher pack's payload. Ship no
basecheck, receipt or profile: they carry absolute paths, and the launcher owns the order.

This zip contains the pack's own regulation, msg, map and talk files with your additions merged in, and those‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ files are other
authors' work. Share it only where the pack's terms or its authors allow it, credit them, and otherwise keep it for personal use.

The launcher resolves each path with last writer wins, so tell players to place the costume after the base pack. Any other add-on that
ships its own `regulation.bin`, `msg` or Roundtable (`m10`) files is exclusive with yours: one of them silently loses its content. List
the known ones in `incompatibleWith` and in the readme. When the launcher updates the base pack, disable the costume until a matching
build exists.

Hajiwo case: the owner's solo test of the launcher zip was fully OK (player and NPC bound; calm, rest, heavy-attack and ultimate faces
seen) [game]. Co-op on it is untested.

## Co-op rule

The whole team installs the same version. Regulation and the Roundtable map must match, or players see missing costumes, wrong faces
or a param-mismatch warning [inferred]. Put this in every README.

## me3 version notes

- me3 0.13 did not change native load timing for this plug-in. A source diff of 0.10.1 to 0.13.0 shows the native-loading and order
  code unchanged [code]. A game run on 0.13 logged READY, both bindings and applied faces [game].
- Open: one player reported "NPC there, faces never change". If the antivirus quarantines the unsigned DLL, me3 drops the natives while
  the packages still load [inferred]. Ask for the plug-in's log first.
