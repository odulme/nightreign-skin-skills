# Costume params: a standalone new costume

How a costume reaches the wardrobe, which rows and files it needs, how to pick ids, and how to add them without breaking anyone
else's content. Geometry and textures are in geometry_rigging.md and materials_faces.md; shipping the result is in
release_installer.md.

## Standalone costume or replace a vanilla one

| | Replace a vanilla costume | Standalone new costume |
|---|---|---|
| Files | override `parts/bd_m_<vanilla>.partsbnd.dcx` (+ `_l`) | new `bd_m_<new>` pair |
| Params | none, or edit the vanilla rows | add rows to four tables (five with a menu NPC) |
| Text | overwrite the vanilla garb name | new GoodsName / GoodsInfo entries |
| Vanilla look | gone while the mod is on | stays selectable |
| Other costume mods | collide on the same file and text id | coexist if ids are free |
| A/B in the same spot | needs two profiles | swap garb at the wardrobe |
| Plug-in identity | "body is model X" is shared with vanilla | own costume id and own model |

Hajiwo case: v001 overrode the vanilla Revenant body (`bd_m_5050` / `_l`) and renamed the Chinese GoodsName 40500 [data]. v006 made it
standalone, so the package no longer overrides the vanilla white garb [data]. Standalone is better for four reasons:
- **Comparison.** Switching to the vanilla garb in the same spot was the key clue in the frame-time hunt (runtime_module.md). With an
  override, that comparison means relaunching the game.
- **Identity.** A plug-in can bind on "costume row 50591 + body 5085100 + private bone names". With an override it would have to tell
  your model apart from the vanilla one by mesh‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ contents alone.
- **Co-op.** Presets keyed by costume id could follow each player without messages, if the costume id replicates. That replication
  is not proven, so the plug-in uses it only to pick presets [inferred].
- **Uninstall and merging.** These come down to "remove the added rows". No vanilla row has to be restored, and nobody else's edit of
  that row is lost.

Replace a vanilla costume only for a throwaway test.

## The chain

```
EquipParamGoods (the garb item) -> CharaInitParam (the loadout) -> EquipParamProtector (one armour piece) -> parts/bd_m_<model>
     ^                                                                                                        + parts/bd_m_<model>_l
ShopLineupParam (wardrobe entry) ; msg FMG (name, info) ; menu icon atlas (iconId)
```

| Table / file | Key fields | Notes |
|---|---|---|
| EquipParamGoods | `goodsType` = hero, `characterInitId`, `sortId`, `iconId` | `goodsType` selects which hero sees the garb. Read it from that hero's vanilla garb row; Revenant = 21 [data]. `sortId` = own id is the usual choice. |
| CharaInitParam | `heroId`, `equip_Helm` / `equip_Armer` / `equip_Gaunt` / `equip_Leg`, `CharacterScale`, start weapon | Clone the hero's default row and change only the slot you replace. Revenant: `heroId` 6, `CharacterScale` 0.85, both copied unchanged [data]. Do the big-head look in the mesh, not with this scale. |
| EquipParamProtector | `equipModelId`, `bodyEquip` / `headEquip` / ... bits | Clone the vanilla piece. `equipModelId` N maps to `parts/bd_m_N.partsbnd.dcx` [data]. |
| parts | `bd_m_N.partsbnd.dcx` and `bd_m_N_l.partsbnd.dcx` | Ship both. The low file needs its own `_l` texture names (aliases) [data]. Players far away, and possibly other players' copies, use `_l`. Cloth files that no longer fit your mesh must be dropped (geometry_rigging.md). |
| ShopLineupParam | `equipId` = goods id, `value`, `costType`, `equipType`, `eventFlag_forRelease` | The row must sit in the id block that the wardrobe's shop call opens. Hajiwo case: the 11000-11999 Change Garb block, `equipType` 3 (goods), `costType` 4 (Murk), `value` 0, release flag 0 [data]. Other recipes gate the row on a release flag instead. |
| msg FMG | GoodsName / GoodsInfo = goods id, in `item_dlc01.msgbnd.dcx` | Do this for every language folder you ship. A missing entry shows a placeholder like `?GoodsName?`: the English UI did this when only Chinese text was added [game]. With no translation, ship English text rather than nothing. |
| icon | `iconId` -> sprite `MENU_ItemIcon_<id>` in `menu/05_dummy_h` and `05_dummy_l` (`.sblytbnd.dcx` + `.tpf.dcx`) | Add one atlas texture plus one layout member to both resolutions. Hajiwo case: iconId 17970 (160x160 item icon) and 17971 (420x220 list picture), one 512 px BC7 atlas; both ids checked free [data]. |

The FLVER's materials also need their MATBIN members in the material library. Add only the names your FLVERs reference: Hajiwo once
shipped 7 when 5 were used (an early build) [data]. See materials_faces.md.

## Picking ids

- **Scan the actual target, not vanilla.** For each file, find the copy the player's profile really serves (the last package in me3's
  order that has it, else the game's). Check every id there: param rows, `parts/` names, FMG ids, icon sprite names, MATBIN names. If
  you add an NPC or menu, also check talk members, MSB part names, text ids and event flags. Also read the pack's own reservation notes
  or CSVs if it ships any.
- **A free id in vanilla says little.** Costume packs fill the ranges right after the vanilla garbs. For Wylder, vanilla uses goods
  40000-40060, and packs commonly start at 40061 / 50061 / 11131 [data]. A protector id that looks free next to your hero's can belong
  to another hero: an earlier recipe found 5009100 taken that way [data].
- **Check again at install time.** A release cannot rely on the scan you did on your own pack. Hajiwo's installer refuses, naming the
  table and id, when any id is taken in the files it merges into [sim].
- **Parallel numbers help humans.** Goods 40xyz, chara 50xyz, shop 11xyz is a readable convention, not a rule.
- **Event flags are ids too.** Before using a flag range, check that no event script, talk script or param cell references it
  (runtime_module.md).

## Row order when serialising PARAM

- Rows stay sorted by id, ascending; the game looks rows up by binary search [data]. Insert a new row before the first row with a
  larger id. Never append at the end.
- Two table shapes exist. Vanilla‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ tables are name-stripped: every row's name offset points to one spot. Editor-written tables carry row
  names. Handle both; a named table needs room for the new row's (empty) name.
- Rebuild only the PARAM members you change. Untouched members stay byte-identical. Do not round-trip untouched (possibly stripped)
  tables through a paramdef writer.
- Prove each edit: the rebuilt table parses, the new row reads back as built, and removing the row gives the original table byte for
  byte. Hajiwo case: the installer runs these checks per row and per table, then decrypts its own output and compares every member
  [sim].
- Compare decrypted content: each write gets a new container IV.

## Edit cells only

Describe a new row as "clone of row X, plus these cells". Do not ship a full table, and do not rewrite cells you did not mean to change.
A clone inherits everything, so diff it field by field against its source before trusting it.

Hajiwo case, from the shipped row data [data]:
- NpcParam 521069800 = clone of 521060200 with `nameId` set to 905980.
- CharaInitParam 50592 = clone of 50570 with `equip_Armer` set to 5085100.
- The four costume rows ship as whole rows of the right row size. The installer checks row size and param type against the target
  table before inserting.

## Keep vanilla and third-party costumes selectable

- Never override a vanilla `bd_m_` file or a vanilla garb row or text.
- Merge into shared files; do not replace them. The menu atlas files, the material library, the text binders and regulation all hold
  other mods' content. One costume pack's menu atlas was missing other costumes' icon atlases [data], so overwriting it would have dropped
  their icons.
- Add your shop‌​⁠‍‌‌​⁠‌‌​⁠​‍⁠‌​⁠​‍​⁠​​​⁠​‍​⁠‌‍​⁠​‌​⁠​‌​⁠​‍​⁠​‌​‍⁠‌‌‍​⁠​⁠​​​⁠‌‌​⁠‍‌‌‍​‌​⁠​⁠‌‍‌‍‌‍​‍ row inside the wardrobe block without moving anyone else's row.
- After install, check in game: vanilla garb, at least one third-party garb, and yours, all selectable and all with their own icons.

## Hajiwo case: ids

| Kind | Id | Role |
|---|---|---|
| EquipParamGoods | 40591 | the garb item; goodsType 21, characterInitId 50591, iconId 17970 |
| CharaInitParam | 50591 | Revenant loadout with the Hajiwo body |
| EquipParamProtector | 5085100 | body piece, equipModelId 7980 |
| parts | `bd_m_7980`, `bd_m_7980_l` | high / low model |
| ShopLineupParam | 11691 | free wardrobe entry |
| FMG | GoodsName / GoodsInfo 40591 | 15 language folders; English where no translation |
| icons | 17970 / 17971 | atlas `Hajiwo_Costume_17970` in `05_dummy_h` and `05_dummy_l` |
| NpcParam / CharaInitParam | 521069800 / 50592 | the menu NPC (v022), NpcName 905980 |

These are examples; re-scan and pick your own.

## Checklist

1. List every row, file, text and icon id. Scan the effective copies in the target profile.
2. Build clones as "source row + changed cells". Diff each clone against its source.
3. Insert in id order. Prove the inverse and untouched members.
4. Add texts for every shipped language and icons for both menu resolutions.
5. In game: vanilla, third-party and new garb selectable, with right names and icons in two UI languages.
