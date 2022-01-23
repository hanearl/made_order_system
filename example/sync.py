import hashlib
import os
import shutil
from pathlib import Path


# def sync(source, dest):
#     source_hashes = {}
#     for folder, _, files in os.walk(source):
#         for fn in files:
#             source_hashes[hash_file(Path(folder) / fn)] = fn
#
#     seen = set()
#
#     for folder, _, files in os.walk(dest):
#         for fn in files:
#             dest_path = Path(folder) / fn
#             dest_hash = hash_file(dest_path)
#             seen.add(dest_hash)
#
#             if dest_hash not in source_hashes:
#                 dest_path.remove()
#             elif dest_hash in source_hashes and fn != source_hashes[dest_hash]:
#                 shutil.move(dest_path, Path(folder) / source_hashes[dest_hash])
#
#     for src_hash, fn in source_hashes.items():
#         if src_hash not in seen:
#             shutil.copy(Path(source) / fn, Path(dest) / fn)
#


# refactoring

def sync(source, dest):
    source_hashes = read_paths_and_hashes(source)
    dest_hashes = read_paths_and_hashes(dest)

    actions = determine_actions(source_hashes, dest_hashes, source, dest)

    for action, *paths in actions:
        if action == 'copy':
            shutil.copyfile(*paths)

        if action == 'move':
            shutil.move(*paths)

        if action == 'delete':
            os.remove(paths[0])


def read_paths_and_hashes(root):
    hashes = {}
    for folder, _, files in os.walk(root):
        for fn in files:
            hashes[hash_file(Path(folder) / fn)] = fn
    return hashes


def determine_actions(src_hashes, dst_hashes, src_folder, dst_folder):
    for sha, filename in src_hashes.items():
        if sha not in dst_hashes:
            sourcepath = Path(src_folder) / filename
            destpath = Path(dst_folder) / filename
            yield 'copy', sourcepath, destpath

        elif dst_hashes[sha] != filename:
            olddestpath = Path(dst_folder) / dst_hashes[sha]
            newdestpath = Path(dst_folder) / filename
            yield 'move', olddestpath, newdestpath

    for sha, filename in dst_hashes.items():
        if sha not in src_hashes:
            yield 'delete', dst_folder / filename