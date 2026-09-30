"""Model constants shared across the physics modules (from ``sim.js``)."""

from __future__ import annotations

import math

from .rig import STROKE, WELLBORE

TAU = math.pi * 2
G = 9.81
LBF_N = 4.44822
S_M = STROKE.length                 # polished-rod stroke (m)
S_IN = S_M / 0.0254                 # stroke in inches
CYCLE_DAYS, INJ_END, SOAK_END = 120, 14, 18
T_RES = 47.0                        # reservoir temperature (C)
Z_SAND = 1120.0                     # mid-perforation depth (m)
PUMP_DEPTH = float(WELLBORE["pumpTop"])      # 1068 m
PUMP_INTAKE = float(WELLBORE["pumpBottom"])  # 1088 m
PLUNGER_IN = 1.25                   # plunger diameter (in)
ETA_S = 0.88                        # stroke loss (rod stretch, slippage)
OIL_SG, WATER_SG = 0.945, 1.02
SPM_MIN, SPM_MAX = 0.5, 15.0
PRICE = {"oil": 6000.0, "steamT": 2800.0, "kwh": 8.0}
GRID_CO2_KG_KWH, STEAM_CO2_T_PER_T = 0.71, 0.062
BBL_PER_T_CWE = 6.2898
STEAM_RATE_T_PER_D = 800.0 / INJ_END      # steam generator output: the 800 t practice volume is injected in INJ_END days
TORQUE_RATING_INLB = 320000.0
MU_CAP_CP = 30000.0                 # wetted-rod / emulsified cap on annulus viscosity
KVIS = 0.26                         # effective viscosity fraction seen by the rods
FRIC_FRAC = 0.15                    # rod/tubing friction as a fraction of W_rf
MARGIN_REQ = 0.15

CYCLE = {"days": CYCLE_DAYS, "injEnd": INJ_END, "soakEnd": SOAK_END}
