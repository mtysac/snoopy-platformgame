import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pygame
pygame.init()

from unittest.mock import MagicMock
from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap


TILE_SIZE = 32


def make_animation() -> MagicMock:
    anim = MagicMock()
    anim.copy.return_value = MagicMock()
    anim.copy.return_value.img.return_value = pygame.Surface((32, 32))
    anim.copy.return_value.update = MagicMock()
    return anim


def make_game() -> MagicMock:
    """Stub game with enough assets for PhysicsEntity to initialise."""
    game = MagicMock()
    game.assets.__getitem__ = lambda self, key: make_animation()
    return game


def make_entity(pos=(0.0, 0.0), size=(32, 32)) -> PhysicsEntity:
    return PhysicsEntity(make_game(), 'p1', pos, size)


def make_tilemap_with_floor(floor_y: int = 5) -> Tilemap:
    """Creates a tilemap with a row of grass tiles at floor_y."""
    class MockGame:
        pass

    tm = Tilemap(MockGame(), tile_size=TILE_SIZE)
    for x in range(10):
        tm.tilemap[f'{x};{floor_y}'] = {'type': 'grass', 'variant': 0, 'pos': [x, floor_y]}
    return tm


def make_empty_tilemap() -> Tilemap:
    class MockGame:
        pass
    return Tilemap(MockGame(), tile_size=TILE_SIZE)


# --- rect ---

def test_rect_matches_position_and_size():
    entity = make_entity(pos=(10.0, 20.0), size=(32, 32))
    r = entity.rect()
    assert r.x == 10
    assert r.y == 20
    assert r.width == 32
    assert r.height == 32


# --- gravity ---

def test_gravity_increases_y_velocity():
    entity = make_entity()
    tm = make_empty_tilemap()
    initial_vy = entity.velocity[1]
    entity.update(tm)
    assert entity.velocity[1] > initial_vy


def test_gravity_capped_at_max():
    entity = make_entity()
    entity.velocity[1] = 10.0  # above max
    tm = make_empty_tilemap()
    entity.update(tm)
    assert entity.velocity[1] <= 5


# --- collision ---

def test_downward_collision_detected():
    """Entity falling onto a floor tile should register a 'down' collision."""
    floor_y = 5
    tm = make_tilemap_with_floor(floor_y)

    # Place entity just above the floor
    entity_y = (floor_y * TILE_SIZE) - 32
    entity = make_entity(pos=(2 * TILE_SIZE, float(entity_y)))
    entity.velocity[1] = 5.0  # falling

    entity.update(tm)
    assert entity.collisions['down'] is True


def test_downward_collision_stops_y_velocity():
    floor_y = 5
    tm = make_tilemap_with_floor(floor_y)

    entity_y = (floor_y * TILE_SIZE) - 32
    entity = make_entity(pos=(2 * TILE_SIZE, float(entity_y)))
    entity.velocity[1] = 5.0

    entity.update(tm)
    assert entity.velocity[1] == 0


def test_no_collision_in_open_space():
    tm = make_empty_tilemap()
    entity = make_entity(pos=(100.0, 100.0))
    entity.update(tm)
    assert entity.collisions['down'] is False
    assert entity.collisions['up'] is False
    assert entity.collisions['left'] is False
    assert entity.collisions['right'] is False


# --- flip ---

def test_flip_false_when_moving_right():
    entity = make_entity()
    tm = make_empty_tilemap()
    entity.update(tm, movement=(1, 0))
    assert entity.flip is False


def test_flip_true_when_moving_left():
    entity = make_entity()
    tm = make_empty_tilemap()
    entity.update(tm, movement=(-1, 0))
    assert entity.flip is True
