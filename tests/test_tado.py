"""Test the Tado object."""

import os
import json
from unittest.mock import patch

from PyTado.interface import Tado


def load_fixture(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path) as fptr:
        return fptr.read()


def mock_tado():
    """Mock out a Tado object."""
    with patch("PyTado.interface.Tado._loginV2"), patch(
        "PyTado.interface.Tado.getMe"
    ):
        tado = Tado("my@username.com", "mypassword")
        return tado


def test_home_can_be_set_to_auto_when_home_supports_geofencing_and_home_set_to_manual_mode():
    """Test that the Tado home can be set to auto geofencing mode when it is supported and currently in manual mode."""
    tado = mock_tado()
    with patch("PyTado.interface.Tado._apiCall",
        return_value=json.loads(load_fixture("tadov2.home_state.auto_supported.manual_mode.json")),
    ):
        tado.getHomeState()

    with patch("PyTado.interface.Tado._apiCall"):
        raised = False
        try:
            tado.setAuto()
        except:
            raised = True
        
        # An exception should NOT have been raised because geofencing is supported
        assert raised is False


def test_home_remains_set_to_auto_when_home_supports_geofencing_and_home_already_set_to_auto_mode():
    """Test that the Tado home remains set to auto geofencing mode when it is supported, and already in auto mode."""
    tado = mock_tado()
    with patch("PyTado.interface.Tado._apiCall",
        return_value=json.loads(load_fixture("tadov2.home_state.auto_supported.auto_mode.json")),
    ):
        tado.getHomeState()

    with patch("PyTado.interface.Tado._apiCall"):
        raised = False
        try:
            tado.setAuto()
        except:
            raised = True
        
        # An exception should NOT have been raised because geofencing is supported
        assert raised is False


def test_home_cant_be_set_to_auto_when_home_does_not_support_geofencing():
    """Test that the Tado home can't be set to auto geofencing mode when it is not supported."""
    tado = mock_tado()
    with patch("PyTado.interface.Tado._apiCall",
        return_value=json.loads(load_fixture("tadov2.home_state.auto_not_supported.json")),
    ):
        tado.getHomeState()

    with patch("PyTado.interface.Tado._apiCall"):
        raised = False
        try:
            tado.setAuto()
        except:
            raised = True
        
        # An exception should have been raised because geofencing is NOT supported
        assert raised is True
