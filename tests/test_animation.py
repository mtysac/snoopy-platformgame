import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from unittest.mock import MagicMock
from scripts.utils import Animation


def make_animation(frames: int = 4, dur: int = 2, loop: bool = True) -> Animation:
    images = [MagicMock() for _ in range(frames)]
    return Animation(images, img_dur=dur, loop=loop)


def test_looping_animation_wraps():
    anim = make_animation(frames=2, dur=2, loop=True)
    for _ in range(4):  # full cycle
        anim.update()
    assert anim.frame == 0


def test_non_looping_animation_stops():
    anim = make_animation(frames=2, dur=2, loop=False)
    for _ in range(10):
        anim.update()
    assert anim.done is True


def test_non_looping_frame_does_not_exceed_max():
    anim = make_animation(frames=2, dur=2, loop=False)
    for _ in range(20):
        anim.update()
    max_frame = anim.img_duration * len(anim.images) - 1
    assert anim.frame <= max_frame


def test_copy_is_independent():
    anim = make_animation()
    copy = anim.copy()
    anim.update()
    assert copy.frame == 0


def test_img_returns_correct_frame():
    anim = make_animation(frames=4, dur=2, loop=True)
    first_img = anim.img()
    anim.update()
    anim.update()  # advance one full frame
    assert anim.img() is not first_img
