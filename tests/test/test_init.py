"""Test module.

make test T=test_init.py
"""
import pytest
from . import TestBase


class TestsInit(TestBase):
    """Module tests."""

    @staticmethod
    def test_is_in_limits():
        """Check is_in_limits function."""
        from pipeline_anomaly_detection_gazprom import is_in_limits, MagnetType

        real = (100, 100, 5)
        calcked = (90, 90, 6)

        assert is_in_limits(calcked, real, 10, magnet_type=MagnetType.MFL) == (True, True, True)
        assert is_in_limits(calcked, real, 10, magnet_type=MagnetType.TFI) == (True, True, True)
        assert is_in_limits((90, 90, 1), real, 30, magnet_type=MagnetType.TFI) == (True, True, False)
        assert is_in_limits((90, 5, 1), real, 30, magnet_type=MagnetType.TFI) == (True, False, False)

        real = (10, 10, 10)
        calcked = (9, 9, 6)

        assert is_in_limits(calcked, real, 10, magnet_type=MagnetType.MFL) == (True, True, False)
        assert is_in_limits(calcked, real, 10, magnet_type=MagnetType.TFI) == (True, True, False)
        assert is_in_limits((90, 90, 1), real, 30, magnet_type=MagnetType.TFI) == (False, False, False)

        real = (5, 5, 5)
        calcked = (9, 9, 6)

        assert is_in_limits(calcked, real, 10, magnet_type=MagnetType.MFL) == (True, True, True)
        assert is_in_limits(calcked, real, 10, magnet_type=MagnetType.TFI) == (True, True, True)
        assert is_in_limits((90, 90, 1), real, 30, magnet_type=MagnetType.TFI) == (False, False, True)

        real = (5, 100, 10)
        calcked = (5, 100, 6)

        assert is_in_limits(calcked, real, 10, magnet_type=MagnetType.MFL) == (True, True, False)

        with pytest.raises(Error) as exc:
            is_in_limits(calcked, real, 10, magnet_type=MagnetType.TFI)
        assert "class 'CISL'. Not applicable for method 'TFI'" in str(exc)

        real = (100, 5, 10)
        calcked = (100, 5, 6)

        assert is_in_limits(calcked, real, 10, magnet_type=MagnetType.TFI) == (True, True, False)
        assert is_in_limits((90, 90, 1), real, 30, magnet_type=MagnetType.TFI) == (True, False, False)

        with pytest.raises(Error) as exc:
            is_in_limits(calcked, real, 10, magnet_type=MagnetType.MFL)
        assert "class 'AXSL'. Not applicable for method 'MFL'" in str(exc)

        real = (50, 10, 10)
        calcked = (50, 10, 6)

        assert is_in_limits(calcked, real, 10, magnet_type=MagnetType.MFL) == (True, True, False)
        assert is_in_limits(calcked, real, 10, magnet_type=MagnetType.TFI) == (True, True, False)
        assert is_in_limits((90, 90, 1), real, 30, magnet_type=MagnetType.TFI) == (False, False, False)

        real = (10, 50, 10)
        calcked = (10, 50, 6)

        assert is_in_limits(calcked, real, thick, magnet_type=MagnetType.MFL) == (True, True, False)
        assert is_in_limits(calcked, real, thick, magnet_type=MagnetType.TFI) == (True, True, False)

    def test_is_detectable(self):
        """Check is_detectable function."""
        from pipeline_anomaly_detection_gazprom import is_detectable, MagnetType

        thick = 10
        assert is_detectable((10, 10, 5), thick, magnet_type=MagnetType.MFL)
        assert is_detectable((10, 10, -1), thick, magnet_type=MagnetType.MFL)
        assert not is_detectable((20, 1, -1), thick, magnet_type=MagnetType.MFL)
