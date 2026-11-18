"""
Unit tests for the balloon celebration feature.

Run with: pytest tests/test_balloons.py -v
"""

import pytest
from app.game.balloons import (
    BalloonConfig,
    BalloonManager,
    BalloonState,
    PopSpeed,
    PopTrigger,
)


class TestBalloonConfig:
    """Tests for BalloonConfig dataclass."""

    def test_default_config_creation(self):
        """Test creating config with defaults."""
        config = BalloonConfig()
        assert config.count == 15
        assert config.pop_trigger == PopTrigger.CLICK
        assert config.pop_speed == PopSpeed.MEDIUM
        assert config.float_animation is True
        assert len(config.colors) == 7

    def test_custom_config_creation(self):
        """Test creating config with custom values."""
        custom_colors = ["#FF0000", "#00FF00", "#0000FF"]
        config = BalloonConfig(
            count=20,
            colors=custom_colors,
            pop_trigger=PopTrigger.AUTO,
            pop_speed=PopSpeed.FAST,
            float_animation=False,
        )
        assert config.count == 20
        assert config.colors == custom_colors
        assert config.pop_trigger == PopTrigger.AUTO
        assert config.pop_speed == PopSpeed.FAST
        assert config.float_animation is False

    def test_default_colors_set_on_none(self):
        """Test that colors are set even if None is passed."""
        config = BalloonConfig(colors=None)
        assert config.colors is not None
        assert len(config.colors) == 7
        # Check that colors are valid hex values
        for color in config.colors:
            assert color.startswith("#")
            assert len(color) == 7

    def test_pop_duration_fast(self):
        """Test pop duration for fast speed."""
        config = BalloonConfig(pop_speed=PopSpeed.FAST)
        duration = config.get_pop_duration_ms()
        assert 300 <= duration <= 500

    def test_pop_duration_medium(self):
        """Test pop duration for medium speed."""
        config = BalloonConfig(pop_speed=PopSpeed.MEDIUM)
        duration = config.get_pop_duration_ms()
        assert 600 <= duration <= 900

    def test_pop_duration_slow(self):
        """Test pop duration for slow speed."""
        config = BalloonConfig(pop_speed=PopSpeed.SLOW)
        duration = config.get_pop_duration_ms()
        assert 1000 <= duration <= 1500


class TestBalloonState:
    """Tests for BalloonState dataclass."""

    def test_balloon_state_creation(self):
        """Test creating a balloon state."""
        balloon = BalloonState(
            x=100.0,
            y=200.0,
            radius=20.0,
            color="#FF0000",
            velocity_y=-1.5,
            velocity_x=0.5,
            float_duration=2000.0,
            start_time=0.0,
        )
        assert balloon.x == 100.0
        assert balloon.y == 200.0
        assert balloon.radius == 20.0
        assert balloon.color == "#FF0000"
        assert balloon.is_popped is False

    def test_balloon_state_popped_flag(self):
        """Test popped flag on balloon state."""
        balloon = BalloonState(
            x=100.0,
            y=200.0,
            radius=20.0,
            color="#FF0000",
            velocity_y=-1.5,
            velocity_x=0.5,
            float_duration=2000.0,
            start_time=0.0,
            is_popped=True,
        )
        assert balloon.is_popped is True


class TestBalloonManager:
    """Tests for BalloonManager class."""

    def test_manager_creation_with_default_config(self):
        """Test creating manager with default config."""
        manager = BalloonManager()
        assert manager.config is not None
        assert manager.config.count == 15
        assert len(manager.balloons) == 0

    def test_manager_creation_with_custom_config(self):
        """Test creating manager with custom config."""
        config = BalloonConfig(count=10)
        manager = BalloonManager(config)
        assert manager.config.count == 10

    def test_create_balloons(self):
        """Test creating balloons."""
        manager = BalloonManager(BalloonConfig(count=10))
        balloons = manager.create_balloons(600, 800)

        assert len(balloons) == 10
        assert len(manager.balloons) == 10

        # Check that all balloons have required attributes
        for balloon in balloons:
            assert isinstance(balloon, BalloonState)
            assert 0 <= balloon.x <= 600
            assert balloon.y > 800
            assert balloon.radius > 0
            assert balloon.color in manager.config.colors
            assert balloon.is_popped is False

    def test_create_balloons_different_canvas_size(self):
        """Test creating balloons with different canvas sizes."""
        manager = BalloonManager(BalloonConfig(count=5))
        balloons = manager.create_balloons(1000, 1500)

        for balloon in balloons:
            assert 0 <= balloon.x <= 1000
            assert balloon.y > 1500

    def test_to_dict_serialization(self):
        """Test converting balloon state to dictionary."""
        config = BalloonConfig(count=2)
        manager = BalloonManager(config)
        manager.create_balloons(600, 800)

        result = manager.to_dict()

        assert "config" in result
        assert "balloons" in result
        assert result["config"]["count"] == 2
        assert len(result["balloons"]) == 2

    def test_to_dict_config_values(self):
        """Test that config values are correctly serialized."""
        config = BalloonConfig(
            count=10,
            pop_trigger=PopTrigger.AUTO,
            pop_speed=PopSpeed.FAST,
        )
        manager = BalloonManager(config)
        manager.create_balloons(600, 800)

        result = manager.to_dict()
        assert result["config"]["count"] == 10
        assert result["config"]["popTrigger"] == "auto"
        assert result["config"]["popSpeed"] == "fast"
        assert result["config"]["floatAnimation"] is True

    def test_to_dict_balloon_values(self):
        """Test that balloon values are correctly serialized."""
        manager = BalloonManager(BalloonConfig(count=1))
        manager.create_balloons(600, 800)

        result = manager.to_dict()
        balloon = result["balloons"][0]

        assert "x" in balloon
        assert "y" in balloon
        assert "radius" in balloon
        assert "color" in balloon
        assert "velocityY" in balloon
        assert "velocityX" in balloon
        assert "isPopped" in balloon


class TestPopSpeedEnum:
    """Tests for PopSpeed enum."""

    def test_pop_speed_values(self):
        """Test PopSpeed enum values."""
        assert PopSpeed.FAST.value == "fast"
        assert PopSpeed.MEDIUM.value == "medium"
        assert PopSpeed.SLOW.value == "slow"


class TestPopTriggerEnum:
    """Tests for PopTrigger enum."""

    def test_pop_trigger_values(self):
        """Test PopTrigger enum values."""
        assert PopTrigger.CLICK.value == "click"
        assert PopTrigger.AUTO.value == "auto"
        assert PopTrigger.BOTH.value == "both"


class TestBalloonIntegration:
    """Integration tests for balloon system."""

    def test_full_balloon_creation_workflow(self):
        """Test the complete workflow of creating balloons."""
        config = BalloonConfig(
            count=5,
            pop_trigger=PopTrigger.CLICK,
            pop_speed=PopSpeed.MEDIUM,
        )
        manager = BalloonManager(config)
        balloons = manager.create_balloons(800, 600)
        state_dict = manager.to_dict()

        assert len(balloons) == 5
        assert state_dict["config"]["count"] == 5
        assert state_dict["config"]["popTrigger"] == "click"
        assert len(state_dict["balloons"]) == 5

    def test_multiple_managers_independent(self):
        """Test that multiple managers don't interfere."""
        manager1 = BalloonManager(BalloonConfig(count=5))
        manager2 = BalloonManager(BalloonConfig(count=10))

        manager1.create_balloons(600, 800)
        manager2.create_balloons(800, 1000)

        assert len(manager1.balloons) == 5
        assert len(manager2.balloons) == 10

    def test_color_distribution(self):
        """Test that colors are distributed from palette."""
        config = BalloonConfig(count=100)
        manager = BalloonManager(config)
        manager.create_balloons(600, 800)

        colors_used = set(b.color for b in manager.balloons)
        # With 100 balloons and 7 colors, we should use multiple colors
        assert len(colors_used) > 1
        # All colors used should be in the palette
        assert colors_used.issubset(set(config.colors))

    def test_velocities_vary(self):
        """Test that velocities vary across balloons."""
        manager = BalloonManager(BalloonConfig(count=20))
        manager.create_balloons(600, 800)

        velocities_y = set(b.velocity_y for b in manager.balloons)
        velocities_x = set(b.velocity_x for b in manager.balloons)

        # With 20 balloons, we should have varied velocities
        assert len(velocities_y) > 1
        assert len(velocities_x) > 1
