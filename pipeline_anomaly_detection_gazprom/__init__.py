# coding: utf-8
"""Gazprom requirements for the detection threshold and accuracy of determining the size of pipeline defects."""
from pipeline_anomaly_dimension_class import FeatureClass, size_class


class Error(Exception):
    """Module exception."""


class MagnetType:
    """Magnet system types."""

    MFL = 'MFL'  # lengthwise
    TFI = 'TFI'  # diametral
    CAL = 'CAL'  # caliper


MIN_PERCENT = {  # пороги обнаружения в % от толщины стенки трубы

  MagnetType.MFL: {
    FeatureClass.GENE: 5,
    FeatureClass.PITT: 10,
    FeatureClass.PINH: 20,
    FeatureClass.AXGR: 20,
    FeatureClass.CIGR: 8,
    FeatureClass.CISL: 8,
  },

  MagnetType.TFI: {
    FeatureClass.GENE: 5,
    FeatureClass.PITT: 10,
    FeatureClass.PINH: 20,
    FeatureClass.CIGR: 20,
    FeatureClass.AXGR: 8,
    FeatureClass.AXSL: 8,
  },
}

LIMITS = {

  MagnetType.MFL: {

    FeatureClass.GENE: lambda thick, length, width, depth: (
      lim(length, 0, 30),  # точность по длине, мм -/+
      lim(width, 0, 30),  # точность по ширине, мм -/+
      lim_z(depth, thick, 0.1),  # точность по глубине, мм -/+
    ),

    FeatureClass.PITT: lambda thick, length, width, depth: (
      lim(length, 0, 20), lim(width, 0, 30), lim_z(depth, thick, 0.1),
    ),

    FeatureClass.PINH: lambda thick, length, width, depth: (
      lim(length, 0, 15), lim(width, thick, 30), lim_z(depth, thick, 0.2),
    ),

    FeatureClass.AXGR: lambda thick, length, width, depth: (
      lim(length, 0, 20), lim(width, 0, 30), lim_z(depth, thick, 0.2),
    ),

    FeatureClass.CIGR: lambda thick, length, width, depth: (
      lim(length, 0, 20), lim(width, thick, 30), lim_z(depth, thick, 0.15),
    ),

    FeatureClass.CISL: lambda thick, length, width, depth: (
      lim(length, 0, 20), lim(width, thick, 30), lim_z(depth, thick, 0.15),
    ),

  },

  MagnetType.TFI: {

    FeatureClass.GENE: lambda thick, length, width, depth: (
      lim(length, 0, 30), lim(width, 0, 30), lim_z(depth, thick, 0.1),
    ),

    FeatureClass.PITT: lambda thick, length, width, depth: (
      lim(length, 0, 30), lim(width, 0, 20), lim_z(depth, thick, 0.1),
    ),

    FeatureClass.PINH: lambda thick, length, width, depth: (
      lim(length, thick, 30), lim(width, 0, 15), lim_z(depth, thick, 0.2),
    ),

    FeatureClass.CIGR: lambda thick, length, width, depth: (
      lim(length, 0, 30), lim(width, 0, 20), lim_z(depth, thick, 0.2),
    ),

    FeatureClass.AXGR: lambda thick, length, width, depth: (
      lim(length, 0, 30), lim(width, 0, 20), lim_z(depth, thick, 0.15),
    ),

    FeatureClass.AXSL: lambda thick, length, width, depth: (
      lim(length, 0, 30), lim(width, 0, 20), lim_z(depth, thick, 0.15),
    ),

  },
}


def lim_z(depth, thick, val):
    """Return limits for depth."""
    return (depth - val * thick, depth + val * thick)


def lim(size, thick, val):
    """Return limits for width/length."""
    return (size - (thick + val), size + (thick + val))


def is_detectable(sizes, thick, magnet_type=MagnetType.MFL):
    """Return True if defekt with given sizes on wallthick more than minimal percent."""
    length, width, depth = sizes
    cls = size_class(length, width, thick)
    min_percent = MIN_PERCENT[magnet_type]
    if cls not in min_percent:
        return False

    if depth < 0:  # through hole
        depth = thick

    return int(round(depth * 100.0 / thick, 0)) >= min_percent[cls]


def is_in_limits(calcked, real, thick, magnet_type=MagnetType.MFL):
    """Return tuple from 3 boolean items, that represent limits by length, width, depth."""
    limits = LIMITS[magnet_type]
    cls = size_class(real[0], real[1], thick)
    if cls not in limits:
        raise Error("Defect with params {} has class '{}'. Not applicable for method '{}'".format(
          real, cls, magnet_type
        ))

    length, width, depth = calcked
    limits_length, limits_width, limits_depth = limits[cls](thick, *real)

    return (
      limits_length[0] <= length <= limits_length[1],
      limits_width[0] <= width <= limits_width[1],
      limits_depth[0] <= depth <= limits_depth[1],
    )
