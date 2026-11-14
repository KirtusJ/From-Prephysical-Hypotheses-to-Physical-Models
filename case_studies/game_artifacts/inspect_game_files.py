"""Inventory the 15 supplied files and inspect archives in memory without running contents."""

import argparse
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import stat
import struct
import tarfile
from zipfile import ZipFile


FILES = (
    "Night_Post.html", "Night_Post(1).html", "Night_Post_Flight.gif",
    "Night_Post_Flight(1).gif", "Night_Post_Rust.zip", "Bellweather_Harbor.html",
    "Bellweather_Harbor_Timelapse.gif", "Bellweather_Harbor_Rust.zip",
    "Doom_Game_Memory.zip", "Doom_Hangar.gif", "Barrel_Bowl.zip",
    "Barrel_Bowl_At_Phobos.mp4", "Ultra_Omega_Barrel.zip",
    "Ultra_Omega_Barrel_Fight.mp4", "PCP_OS_Boot.png",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def identity(data):
    return {"bytes": len(data), "sha256": sha256(data).hexdigest()}


def validate_path(name, seen):
    clean = name.removesuffix("/")
    parts = clean.split("/")
    require(all(parts) and not any(p in (".", "..") for p in parts), name)
    require("\\" not in name and ":" not in name, name)
    folded = clean.casefold()
    require(folded not in seen, f"duplicate path: {name}")
    seen.add(folded)


def tar_inventory(data):
    records = []
    seen = set()
    with tarfile.open(fileobj=BytesIO(data), mode="r:gz") as archive:
        for member in archive:
            validate_path(member.name, seen)
            require(member.isdir() or member.isfile(), f"nonregular tar entry: {member.name}")
            if member.isfile():
                records.append({"path": member.name, **identity(archive.extractfile(member).read())})
            else:
                records.append({"path": member.name, "directory": True})
    return records


def wad_directory(data):
    marker, count, offset = struct.unpack_from("<4sii", data)
    require(marker == b"PWAD" and 0 <= count and 12 <= offset <= len(data)-16*count,
            "invalid PWAD directory")
    names = []
    for i in range(count):
        start, length, raw = struct.unpack_from("<ii8s", data, offset+16*i)
        require(0 <= start <= len(data) and 0 <= length <= len(data)-start, "invalid PWAD extent")
        names.append(raw.rstrip(b"\0").decode("ascii"))
    return names


def inspect(folder):
    originals = {name: (folder/name).read_bytes() for name in FILES}
    manifest = {n: identity(data) for n, data in originals.items()}
    listing, unpacked = {}, {}
    for name, data in originals.items():
        if not name.endswith(".zip"):
            continue
        members = {}
        seen = set()
        with ZipFile(BytesIO(data)) as archive:
            require(archive.testzip() is None, f"CRC failure: {name}")
            for item in archive.infolist():
                validate_path(item.filename, seen)
                require(not item.is_dir() and not stat.S_ISLNK(item.external_attr >> 16),
                        f"unexpected ZIP entry: {item.filename}")
                entry = archive.read(item)
                require(len(entry) == item.file_size, item.filename)
                members[item.filename] = entry
        unpacked[name] = members
        listing[name] = {}
        for n, entry in members.items():
            record = identity(entry)
            if n.endswith(".tar.gz"):
                record["members"] = tar_inventory(entry)
            if n.endswith(".wad"):
                record["lumps"] = wad_directory(entry)
            listing[name][n] = record
        manifest[name]["zip_entries"] = len(members)
        manifest[name]["unpacked_bytes"] = sum(len(v) for v in members.values())

    ultra = {k.split("/",1)[1]:v for k,v in unpacked["Ultra_Omega_Barrel.zip"].items()}
    bowl = {k.split("/",1)[1]:v for k,v in unpacked["Barrel_Bowl.zip"].items()}
    common = sorted(set(ultra) & set(bowl))
    extra = unpacked["Doom_Game_Memory.zip"]
    save = extra["doomsav0.dsg"]
    info = json.loads(extra["session-memory.json"])
    require(sha256(save).hexdigest() == info["save"]["sha256"], "doom save pin")
    require(save[-1] == 0x1d and save[43:47] == bytes([1,0,0,0]), "save header or EOF")
    fields = {"description": save[:24].rstrip(b"\0").decode("ascii"),
              "episode": save[41], "map": save[42]}
    # v1.9 little-endian, one active, aligned player record beginning at offset 52.
    for field, offset in (("health", 84), ("armor", 88), ("bullets", 208)):
        fields[field] = struct.unpack_from("<i", save, offset)[0]
    require(all(info["save"][k] == v for k,v in fields.items()), "save field disagreement")
    coords = struct.pack("<ii", info["save"]["x_fixed"], info["save"]["y_fixed"])
    records = {"files": manifest, "zip_members": listing,
               "overlap_of_barrel_packages": {
                   "same_bytes": [n for n in common if ultra[n] == bowl[n]],
                   "different_bytes": [n for n in common if ultra[n] != bowl[n]],
                   "only_in_bowl": sorted(set(bowl)-set(ultra)),
                   "only_in_ultra": sorted(set(ultra)-set(bowl))},
               "doom_save": {"verified_fields": fields, "version": save[24:40].rstrip(b"\0").decode(),
                             "claimed_coordinate_pair_byte_matches": save.count(coords)},
               "byte_equalities": {
                   "standalone_night_posts_match": originals["Night_Post.html"] == originals["Night_Post(1).html"],
                   "night_post_archive_matches_standalone": unpacked["Night_Post_Rust.zip"]["night-post/dist/Night_Post.html"] == originals["Night_Post.html"],
                   "bellweather_archive_matches_standalone": unpacked["Bellweather_Harbor_Rust.zip"]["Bellweather_Harbor/dist/Bellweather_Harbor.html"] == originals["Bellweather_Harbor.html"],
                   "ultra_fight_matches_extra": ultra["extras/The-Last-Press.mp4"] == originals["Ultra_Omega_Barrel_Fight.mp4"],
                   "doom_hangar_matches_extra": ultra["extras/Hangar.gif"] == originals["Doom_Hangar.gif"]}}
    return records


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path, help="directory containing the 15 original inputs")
    parser.add_argument("--inventory", type=Path, help="write full nested inventory to a new local file")
    args = parser.parse_args()
    result = inspect(args.folder)
    reference = json.loads(Path(__file__).with_name("files.json").read_text("utf-8"))
    require(result["files"] == reference, "file differs from supplied intake")
    if args.inventory:
        with args.inventory.open("x", encoding="utf-8", newline="\n") as f:
            json.dump(result, f, indent=2)
            f.write("\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("files","zip_members")}, indent=2))
