"""
Balloon celebration animation system for Tetris game win screen.
"""

from dataclasses import dataclass
from typing import List
from enum import Enum


class PopSpeed(str, Enum):
    """Pop animation speed options."""
    FAST = "fast"      # 300-500ms
    MEDIUM = "medium"  # 600-900ms
    SLOW = "slow"      # 1000-1500ms


class PopTrigger(str, Enum):
    """Balloon pop trigger options."""
    CLICK = "click"    # User must click to pop
    AUTO = "auto"      # Auto-pop with animation
    BOTH = "both"      # Click or auto-pop


@dataclass
class BalloonConfig:
    """Configuration for balloon celebration animation."""
    count: int = 15
    colors: List[str] = None
    pop_trigger: PopTrigger = PopTrigger.CLICK
    pop_speed: PopSpeed = PopSpeed.MEDIUM
    float_animation: bool = True

    def __post_init__(self):
        """Set default colors from game palette if not provided."""
        if self.colors is None:
            # Using Tetris standard piece colors
            self.colors = [
                "#FF6B6B",  # Red (I-piece)
                "#4ECDC4",  # Cyan (T-piece)
                "#45B7D1",  # Blue (J-piece)
                "#FFA07A",  # Orange (L-piece)
                "#FFD93D",  # Yellow (O-piece)
                "#6BCB77",  # Green (S-piece)
                "#FF7FB3",  # Purple (Z-piece)
            ]

    def get_pop_duration_ms(self) -> int:
        """Get pop animation duration in milliseconds."""
        if self.pop_speed == PopSpeed.FAST:
            return 400  # middle of 300-500ms
        elif self.pop_speed == PopSpeed.SLOW:
            return 1250  # middle of 1000-1500ms
        else:  # MEDIUM
            return 750  # middle of 600-900ms


@dataclass
class BalloonState:
    """State of a single balloon."""
    x: float
    y: float
    radius: float
    color: str
    velocity_y: float
    velocity_x: float
    float_duration: float  # milliseconds
    start_time: float  # milliseconds from start
    is_popped: bool = False
    string_length: float = 50


class BalloonManager:
    """Manages balloon creation and state for win animations."""

    def __init__(self, config: BalloonConfig = None):
        """
        Initialize balloon manager.

        Args:
            config: BalloonConfig instance with animation settings.
                   Defaults to standard configuration if None.
        """
        self.config = config or BalloonConfig()
        self.balloons: List[BalloonState] = []

    def create_balloons(self, canvas_width: int, canvas_height: int) -> List[BalloonState]:
        """
        Create initial balloon states for animation.

        Args:
            canvas_width: Width of the game canvas in pixels.
            canvas_height: Height of the game canvas in pixels.

        Returns:
            List of BalloonState instances ready for animation.
        """
        import random
        import time

        self.balloons = []
        current_time = time.time() * 1000

        for i in range(self.config.count):
            balloon = BalloonState(
                x=random.uniform(0, canvas_width),
                y=canvas_height + 50,
                radius=15 + random.random() * 10,
                color=random.choice(self.config.colors),
                velocity_y=-1 - random.random() * 1.5,
                velocity_x=(random.random() - 0.5) * 2,
                float_duration=(2000 + random.random() * 1500) if self.config.float_animation else 0,
                start_time=current_time + i * 100,
                string_length=50 + random.random() * 50,
            )
            self.balloons.append(balloon)

        return self.balloons

    def to_dict(self) -> dict:
        """
        Convert balloon state to dictionary for JSON serialization.

        Returns:
            Dictionary representation of balloon manager state.
        """
        return {
            "config": {
                "count": self.config.count,
                "colors": self.config.colors,
                "popTrigger": self.config.pop_trigger.value,
                "popSpeed": self.config.pop_speed.value,
                "floatAnimation": self.config.float_animation,
                "popDurationMs": self.config.get_pop_duration_ms(),
            },
            "balloons": [
                {
                    "x": b.x,
                    "y": b.y,
                    "radius": b.radius,
                    "color": b.color,
                    "velocityY": b.velocity_y,
                    "velocityX": b.velocity_x,
                    "floatDuration": b.float_duration,
                    "startTime": b.start_time,
                    "isPopped": b.is_popped,
                    "stringLength": b.string_length,
                }
                for b in self.balloons
            ],
        }
