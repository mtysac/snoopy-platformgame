import sys
import os
import json
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pygame
pygame.init()

from scripts.tilemap import Tilemap


class MockGame:
    """Minimal game stub — Tilemap only needs game for rendering, not save/load."""
    pass


def make_tilemap(tile_size: int = 32) -> Tilemap:
    return Tilemap(MockGame(), tile_size=tile_size)


def make_tile(x: int, y: int, tile_type: str = 'grass', variant: int = 0) -> dict:
    return {'type': tile_type, 'variant': variant, 'pos': [x, y]}


# --- Save / Load ---

def test_save_and_load_roundtrip():
    tm = make_tilemap()
    tm.tilemap['2;3'] = make_tile(2, 3, 'grass')
    tm.offgrid_tiles.append({'type': 'back', 'variant': 0, 'pos': [10.0, 20.0]})

    with tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w') as f:
        path = f.name

    try:
        tm.save(path)

        tm2 = make_tilemap()
        tm2.load(path)

        assert '2;3' in tm2.tilemap
        assert tm2.tilemap['2;3']['type'] == 'grass'
        assert tm2.tile_size == 32
        assert len(tm2.offgrid_tiles) == 1
        assert tm2.offgrid_tiles[0]['type'] == 'back'
    finally:
        os.unlink(path)


def test_save_preserves_tile_size():
    tm = make_tilemap(tile_size=16)

    with tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w') as f:
        path = f.name

    try:
        tm.save(path)
        tm2 = make_tilemap(tile_size=32)
        tm2.load(path)
        assert tm2.tile_size == 16
    finally:
        os.unlink(path)


def test_load_empty_map():
    data = {'tilemap': {}, 'tile_size': 32, 'offgrid': []}

    with tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w') as f:
        json.dump(data, f)
        path = f.name

    try:
        tm = make_tilemap()
        tm.load(path)
        assert tm.tilemap == {}
        assert tm.offgrid_tiles == []
    finally:
        os.unlink(path)


# --- tiles_around ---

def test_tiles_around_returns_neighbors():
    tm = make_tilemap(tile_size=32)
    tm.tilemap['2;3'] = make_tile(2, 3)
    tm.tilemap['3;3'] = make_tile(3, 3)

    # pos inside tile (2,3) — should find both (2,3) and (3,3) as neighbors
    tiles = tm.tiles_around([2 * 32 + 1, 3 * 32 + 1])
    types = [t['type'] for t in tiles]
    assert 'grass' in types


def test_tiles_around_empty_map():
    tm = make_tilemap()
    tiles = tm.tiles_around([100.0, 100.0])
    assert tiles == []


# --- physics_rects_around ---

def test_physics_rects_around_grass():
    tm = make_tilemap(tile_size=32)
    tm.tilemap['2;3'] = make_tile(2, 3, 'grass')

    rects = tm.physics_rects_around([2 * 32 + 1, 3 * 32 + 1])
    assert len(rects) >= 1
    assert all(isinstance(r, pygame.Rect) for r in rects)


def test_physics_rects_around_non_physics_tile():
    tm = make_tilemap(tile_size=32)
    tm.tilemap['2;3'] = make_tile(2, 3, 'back')  # 'back' is not a physics tile

    rects = tm.physics_rects_around([2 * 32 + 1, 3 * 32 + 1])
    assert rects == []


def test_physics_rects_around_cement():
    tm = make_tilemap(tile_size=32)
    tm.tilemap['5;5'] = make_tile(5, 5, 'cement')

    rects = tm.physics_rects_around([5 * 32 + 1, 5 * 32 + 1])
    assert len(rects) >= 1
