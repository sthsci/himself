#!/usr/bin/env python3
"""Flow cytometry explainer, "zerokun style".

White blood cells (red cells already removed) flow in single file through a laser.
Each cell scatters some light a little forward (FSC: grows with size) and some sideways
(SSC: grows with the granules inside). Each detector gives a pulse; its peak is recorded.
One stream of particles drives every panel:
  (a) the flow cell: a particle crosses the beam, both detectors light up,
      the meters show the signal now (grey bar) and its peak (black tick)
  (b) every recorded cell is one dot at (FSC peak, SSC peak)
  (c) the FSC peaks alone, as a histogram
(b), (c) and the FSC meter share one x-axis; (b) and the SSC meter share one y-axis.
Particles below the FSC threshold (debris) are drawn but not recorded.
Stage 1: five particles one at a time (lymphocyte, granulocyte, debris, monocyte,
         granulocyte).  Stage 2: the flow speeds up, then stops.

Usage
  python3 flow_zerokun.py info
  python3 flow_zerokun.py scan SEED0 SEED1          # seed search (no drawing)
  python3 flow_zerokun.py render START STOP out.mp4 # frames [START, STOP)
  python3 flow_zerokun.py still FRAME out.png
  python3 flow_zerokun.py stills F1,F2,... DIR       # several stills, one process
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.patches import Rectangle, Ellipse, Polygon, Circle, PathPatch
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection
from matplotlib.ticker import MaxNLocator
from matplotlib.transforms import blended_transform_factory
from matplotlib.path import Path

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
    "text.latex.preamble": r"\usepackage{amsmath}\usepackage{amssymb}",
    "font.size": 11.5,
    "axes.linewidth": 0.9,
    "lines.linewidth": 1.0,
    "xtick.labelsize": 10, "ytick.labelsize": 10,
    "xtick.major.size": 3.5, "ytick.major.size": 3.5,
    "xtick.major.width": 0.8, "ytick.major.width": 0.8,
    "xtick.major.pad": 2, "ytick.major.pad": 2,
    "axes.spines.top": False, "axes.spines.right": False,
})

FPS = 30

# ================================================================== the blood sample
NAMES = ("lymphocyte", "monocyte", "granulocyte", "debris")
P_CELL = np.array([0.30, 0.08, 0.62])          # shares of the white cells
P_DEBRIS = 0.10                                # share of all particles
FSC_MU = np.array([300.0, 640.0, 600.0, 40.0])   # median pulse heights (0-1023 scale)
FSC_CV = np.array([0.10, 0.10, 0.09, 0.35])
SSC_MU = np.array([70.0, 230.0, 600.0, 25.0])
SSC_CV = np.array([0.20, 0.15, 0.13, 0.40])
FMAX = 1024.0
THRESH = 100.0                                 # FSC threshold: below it nothing is recorded
DEBRIS_FSC_MAX = 85.0
K_F = 300.0 / 49.0                             # FSC per um^2 (a 7 um lymphocyte -> 300)
SEED = int(os.environ.get("FLOW_SEED", "13"))


def sample(n, rng):
    """Types and pulse heights (FSC, SSC) of n random particles."""
    p = np.append(P_CELL * (1 - P_DEBRIS), P_DEBRIS)
    t = rng.choice(4, size=n, p=p)
    fsc = FSC_MU[t] * np.exp(FSC_CV[t] * rng.standard_normal(n))
    ssc = SSC_MU[t] * np.exp(SSC_CV[t] * rng.standard_normal(n))
    bad = (t == 3) & (fsc > DEBRIS_FSC_MAX)
    while bad.any():
        fsc[bad] = FSC_MU[3] * np.exp(FSC_CV[3] * rng.standard_normal(int(bad.sum())))
        bad = (t == 3) & (fsc > DEBRIS_FSC_MAX)
    return t, np.clip(fsc, 1, FMAX - 1), np.clip(ssc, 1, FMAX - 1)


# gates (centre FSC, centre SSC, half-width, half-height), one per cell type
GATES = np.array([[314.0, 84.0, 98.0, 48.0],
                  [669.0, 254.0, 200.0, 106.0],
                  [624.0, 646.0, 168.0, 238.0]])


def gate_of(fsc, ssc):
    g = np.full(len(fsc), -1)
    for i, (cx, cy, a, b) in enumerate(GATES):
        g[((fsc - cx) / a) ** 2 + ((ssc - cy) / b) ** 2 <= 1] = i
    return g


NB = 64
BW = FMAX / NB
_big_t, _big_f, _big_s = sample(2_000_000, np.random.default_rng(12345))
_rec = _big_f >= THRESH
_g = gate_of(_big_f[_rec], _big_s[_rec])
GATE_COVER = np.array([np.mean(_g[_big_t[_rec] == i] == i) for i in range(3)])
SHARE_EXP = np.array([np.sum(_g == i) for i in range(3)], float)
SHARE_EXP /= SHARE_EXP.sum()
PBIN = np.bincount(np.minimum((_big_f[_rec] // BW).astype(int), NB - 1), minlength=NB)
PBIN = PBIN / PBIN.sum()
del _big_t, _big_f, _big_s, _rec, _g

# ================================================================== flow cell geometry
# (a) is drawn in display units with equal aspect
XL = (-2.0, 5.0)
YL = (-1.58, 2.66)
_PXU = 0.96 * 720 / (XL[1] - XL[0])            # pixels per display unit
_AXH = (YL[1] - YL[0]) * _PXU / 1280
AX_A = (0.02, 0.925 - _AXH, 0.96, _AXH)
Y_TOP, Y_BOT = YL[1], YL[0]
TUBE_IN, TUBE_OUT, Y_TIP = 0.20, 0.235, 1.70   # sample tube
FUN_W, Y_FUN0, Y_FUN1, CUV_W = 0.56, 1.98, 1.22, 0.175
Y_FOC = 1.30                                   # cells are in single file below this
CORE_END = 0.05
Y_LASER, W0 = 0.30, 0.12                       # beam centre and 1/e^2 half-height
V_TUBE = 0.55                                  # flow speed in the tube / in the channel
X_LASER0, X_STOP = -1.45, 0.95
X_FLENS, X_FDET = 1.35, 1.55
R_PER_UM = 0.011                               # drawn radius per um of diameter
SSC_DIR = np.array([np.cos(np.radians(-45)), np.sin(np.radians(-45))])
SSC_N = np.array([-SSC_DIR[1], SSC_DIR[0]])
P_LASER = np.array([0.0, Y_LASER])
C_SLENS = P_LASER + 0.80 * SSC_DIR
C_SDET = P_LASER + 1.25 * SSC_DIR


def smooth(u):
    u = np.clip(u, 0.0, 1.0)
    return u * u * (3 - 2 * u)


def wall(y):
    return CUV_W + (FUN_W - CUV_W) * (1 - smooth((Y_FUN0 - y) / (Y_FUN0 - Y_FUN1)))


def vel(y):
    return V_TUBE + (1 - V_TUBE) * smooth((Y_TIP - y) / (Y_TIP - Y_FUN1))


def qlat(y):
    return 1 - smooth((Y_TIP - y) / (Y_TIP - Y_FOC))


# stream coordinate s: distance travelled, in channel lengths (speed 1 in the channel)
_YG = np.linspace(Y_TOP + 0.6, Y_BOT - 0.6, 6001)
_SG = np.concatenate([[0.0], np.cumsum(0.5 * (1 / vel(_YG[1:]) + 1 / vel(_YG[:-1]))
                                        * -np.diff(_YG))])
S_LASER = float(np.interp(-Y_LASER, -_YG, _SG))


def y_of_s(s):
    return np.interp(s, _SG, _YG, left=np.nan, right=np.nan)


# ================================================================== timeline
E1 = np.array([40, 96, 152, 208, 264])          # crossing frames of the five singles
S2, RAMP, F_DEC, F_STOP = 290, 130, 732, 752
N_ANIM, N_HOLD = 760, 60
N_FRAMES = N_ANIM + N_HOLD
U1 = 0.014                                     # channel lengths per frame in stage 1
F2_FIRST = 306.0
N_TARGET = 2000
S1_T = np.array([0, 2, 3, 1, 2])
S1_F = np.array([303.0, 586.0, 44.0, 655.0, 622.0])
S1_S = np.array([71.0, 620.0, 24.0, 233.0, 576.0])
S1_TXT = ("lymphocyte", "granulocyte", "", "monocyte", "granulocyte")


def speeds(umax):
    f = np.arange(N_ANIM)
    u = np.full(N_ANIM, U1)
    m = (f >= S2) & (f < S2 + RAMP)
    u[m] = U1 * (umax / U1) ** smooth((f[m] - S2) / RAMP)
    u[(f >= S2 + RAMP) & (f < F_DEC)] = umax
    m = (f >= F_DEC) & (f < F_STOP)
    u[m] = umax * 0.5 * (1 + np.cos(np.pi * (f[m] - F_DEC) / (F_STOP - F_DEC)))
    u[f >= F_STOP] = 0.0
    return u


def cum_of(u):
    return np.concatenate([[0.0], np.cumsum(u)])  # cum[f] = distance moved by frame f


def build_stream(seed):
    rng = np.random.default_rng(seed)
    nq = 3600
    qt, qf, qs = sample(nq, rng)
    typ = np.concatenate([S1_T, qt])
    fsc = np.concatenate([S1_F, qf])
    ssc = np.concatenate([S1_S, qs])
    n = len(typ)
    diam = np.sqrt(fsc / K_F)                  # FSC grows as d^2
    r = diam * R_PER_UM
    ngr = np.where(typ == 3, 0, np.clip(np.rint(ssc / 50), 1, 15)).astype(int)
    xi = np.where(np.arange(n) % 2 == 0, 1.0, -1.0) * rng.uniform(0.3, 1.0, n)
    xi[:5] = [0.5, -0.6, 0.4, -0.5, 0.6]
    rot = rng.uniform(0, 2 * np.pi, n)
    gaps = r[5:-1] + r[6:] + 0.06 + rng.exponential(0.22, n - 6)
    # widen gaps where two neighbours would touch on the way down
    probe = np.linspace(0.0, S_LASER, 90)
    lat = np.maximum(0.0, TUBE_IN - r - 0.015)
    for _ in range(40):
        s_off = np.concatenate([[0.0], np.cumsum(gaps)])
        bad = np.zeros(n - 6, bool)
        for k in (1, 2):
            if k == 2:
                dd = s_off[2:] - s_off[:-2]
                a, b = np.arange(5, n - 2), np.arange(7, n)
            else:
                dd = gaps
                a, b = np.arange(5, n - 1), np.arange(6, n)
            ya = y_of_s(probe[None, :])
            yb = y_of_s(probe[None, :] - dd[:, None])
            xa = xi[a, None] * lat[a, None] * qlat(ya)
            xb = xi[b, None] * lat[b, None] * qlat(yb)
            dist = np.hypot(xa - xb, ya - yb)
            hit = np.nanmin(np.where(np.isnan(dist), 9, dist), axis=1) < r[a] + r[b] + 0.012
            if k == 1:
                bad |= hit
            else:
                bad[:len(hit)] |= hit
        if not bad.any():
            break
        gaps = gaps + 0.04 * bad
    return dict(typ=typ, fsc=fsc, ssc=ssc, r=r, ngr=ngr, xi=xi, rot=rot, gaps=gaps,
                lat=lat, weff=np.sqrt(W0 ** 2 + r ** 2), rec=fsc >= THRESH)


def place(st, umax):
    """Stream positions s0 (at frame 0) and crossing frames for a given top speed."""
    u = speeds(umax)
    cum = cum_of(u)
    s0 = np.empty(len(st["typ"]))
    s0[:5] = S_LASER - U1 * E1 + 1e-9
    c2 = np.interp(F2_FIRST, np.arange(N_ANIM + 1), cum)
    s0[5] = S_LASER - c2
    s0[6:] = s0[5] - np.cumsum(st["gaps"])
    L = np.searchsorted(cum, S_LASER - s0, side="left")   # first frame at/after the laser
    return u, cum, s0, L


def solve_umax(st):
    """Top speed for which the flow stops with ~N_TARGET cells recorded and no particle
    in the beam: the stop falls in the widest nearby gap, equally far (in beam widths)
    from the particle that just crossed and the next one."""
    off = np.concatenate([[0.0], np.cumsum(st["gaps"])])
    w = st["weff"][5:]
    n_rec = 4 + np.cumsum(st["rec"][5:])
    slack = (off[1:] - off[:-1]) / (w[:-1] + w[1:])
    cand = np.nonzero(np.abs(n_rec[:-1] - N_TARGET) <= 25)[0]
    j = int(cand[np.argmax(slack[cand])])
    D = off[j] + (off[j + 1] - off[j]) * w[j] / (w[j] + w[j + 1])
    fr = np.arange(N_ANIM + 1)
    lo, hi = 0.2, 10.0
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        cum = cum_of(speeds(mid))
        if cum[N_ANIM] - np.interp(F2_FIRST, fr, cum) > D:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi), float(slack[j])


def summary(seed):
    st = build_stream(seed)
    umax, _ = solve_umax(st)
    u, cum, s0, L = place(st, umax)
    rec = (L < N_ANIM) & st["rec"]
    f, s = st["fsc"][rec], st["ssc"][rec]
    g = gate_of(f, s)
    cnt = np.array([np.sum(g == i) for i in range(3)], float)
    share = cnt / cnt.sum()
    h = np.bincount(np.minimum((f // BW).astype(int), NB - 1), minlength=NB)
    e = PBIN * rec.sum()
    m = e > 5
    chi = float(np.sum((h[m] - e[m]) ** 2 / e[m]) / m.sum())
    d_end = np.abs(s0 + cum[N_ANIM - 1] - S_LASER)
    near = float(np.min(d_end / st["weff"]))
    return st, umax, share, chi, near, int(rec.sum()), int(((L < N_ANIM) & ~st["rec"]).sum())


def seed_scan(a, b):
    for sd in range(a, b):
        st, umax, share, chi, near, nrec, ndeb = summary(sd)
        dev = np.abs(share - SHARE_EXP) * 100
        print(f"seed {sd:4d} umax {umax:5.3f} N {nrec} deb {ndeb} share "
              f"{np.round(share * 100, 2)} dev {np.round(dev, 2)} chi2/dof {chi:4.2f} "
              f"end-gap {near:4.1f}w")


# ================================================================== the run
ST = build_stream(SEED)
U_MAX, END_SLACK = solve_umax(ST)
U, CUM, S0, LAND = place(ST, U_MAX)
TYP, FSC, SSC, RAD = ST["typ"], ST["fsc"], ST["ssc"], ST["r"]
WEFF, REC = ST["weff"], ST["rec"]
NPART = len(TYP)
_sunflower = []
for _n in range(16):
    _i = np.arange(_n)
    _sunflower.append(np.column_stack([np.sqrt((_i + 0.5) / max(_n, 1)) *
                                       np.cos(_i * 2.39996), np.sqrt((_i + 0.5) / max(_n, 1))
                                       * np.sin(_i * 2.39996)]))


def granules(k):
    p = _sunflower[ST["ngr"][k]]
    c, s = np.cos(ST["rot"][k]), np.sin(ST["rot"][k])
    return 0.62 * RAD[k] * (p @ np.array([[c, s], [-s, c]]))


# per-frame signals at the detectors (the largest pulse seen during each frame)
BAR_F = np.zeros(N_ANIM)
BAR_S = np.zeros(N_ANIM)
RAY_Y = np.full(N_ANIM, Y_LASER)
for _f in range(N_ANIM):
    c0, c1 = CUM[max(_f - 1, 0)], CUM[_f]
    idx = np.nonzero((S0 >= S_LASER - c1 - 0.8) & (S0 <= S_LASER - c0 + 0.8))[0]
    if len(idx) == 0:
        continue
    dp, dn = S0[idx] + c0 - S_LASER, S0[idx] + c1 - S_LASER
    dmin = np.where((dp <= 0) & (dn >= 0), 0.0, np.minimum(np.abs(dp), np.abs(dn)))
    gain = np.exp(-2 * dmin ** 2 / WEFF[idx] ** 2)
    j = int(np.argmax(FSC[idx] * gain))
    BAR_F[_f] = FSC[idx][j] * gain[j]
    BAR_S[_f] = float(np.max(SSC[idx] * gain))
    if U[max(_f - 1, 0)] < 0.08:
        RAY_Y[_f] = Y_LASER - np.clip(dn[j], -0.25, 0.25)

REC_IDX = np.nonzero(REC & (LAND < N_ANIM))[0]                # in crossing order
DEB_IDX = np.nonzero(~REC & (LAND < N_ANIM))[0]
N_REC = np.searchsorted(LAND[REC_IDX], np.arange(N_ANIM), side="right")
N_DEB = np.searchsorted(LAND[DEB_IDX], np.arange(N_ANIM), side="right")
XY_R = np.column_stack([FSC[REC_IDX], SSC[REC_IDX]])
BIN_R = np.minimum((FSC[REC_IDX] // BW).astype(int), NB - 1)
G_R = gate_of(FSC[REC_IDX], SSC[REC_IDX])
GCUM = np.vstack([np.zeros((1, 3), int),
                  np.cumsum(np.stack([G_R == i for i in range(3)], axis=1), axis=0)])
# pulse start (signal above 1 % of its peak) of every particle, for stage-1 timing
_ds = WEFF * np.sqrt(np.log(100) / 2)
PSTART = np.searchsorted(CUM, S_LASER - S0 - _ds, side="left")
S1_ON = PSTART[:6].copy()                      # windows: [S1_ON[i], S1_ON[i+1])
S1_ON[5] = min(S1_ON[5], S2 + 10)
_ev_start = np.searchsorted(LAND, np.arange(N_ANIM + 1), side="left")
# peak ticks (peak-hold, reset when the next recorded pulse starts):
#   events that land in this frame -> their peaks; otherwise, if the next recorded pulse
#   has started -> its running maximum; otherwise hold the peaks of the latest landing
_lr = LAND[REC_IDX]
TICKS = []
for _f in range(N_ANIM):
    _n = N_REC[_f]
    if _f >= F_STOP or _n == 0 and PSTART[REC_IDX[0]] > _f:
        TICKS.append(np.zeros((0, 2)))
        continue
    _lo = np.searchsorted(_lr, _f, side="left")
    if _lo < _n:                                         # landed this frame
        TICKS.append(np.column_stack([FSC[REC_IDX[_lo:_n]], SSC[REC_IDX[_lo:_n]]]))
        continue
    _k = REC_IDX[_n] if _n < len(REC_IDX) else None
    if _k is not None and PSTART[_k] <= _f:              # next pulse rising
        _d = S0[_k] + CUM[_f] - S_LASER
        _gn = np.exp(-2 * _d ** 2 / WEFF[_k] ** 2)
        TICKS.append(np.array([[FSC[_k] * _gn, SSC[_k] * _gn]]))
        continue
    _a = np.searchsorted(_lr, _lr[_n - 1], side="left")   # hold the latest
    TICKS.append(np.column_stack([FSC[REC_IDX[_a:_n]], SSC[REC_IDX[_a:_n]]]))
N_EXP_SHOW, N_GATE_SHOW = 30, 150



def _ytop():
    out = np.empty(N_ANIM)
    prev = 4.0
    for f in range(N_ANIM):
        n = N_REC[f]
        h = np.bincount(BIN_R[:n], minlength=NB).max() if n else 0
        e = (PBIN * n).max() if n >= N_EXP_SHOW else 0
        prev = max(prev, 1.32 * h, 1.32 * e)
        out[f] = prev
    return out


YTOP = _ytop()


def fmt_int(n):
    return f"{n:,}".replace(",", r"\,")


# ================================================================== figure helpers
def fx(d):
    return AX_A[0] + (d - XL[0]) / (XL[1] - XL[0]) * AX_A[2]


def fy(d):
    return AX_A[1] + (d - YL[0]) / (YL[1] - YL[0]) * AX_A[3]


AX_B = (0.10, 0.330, 0.40, 0.225)               # square: 288 x 288 px
AX_FM = (AX_B[0], AX_B[1] + AX_B[3] + 0.007, AX_B[2], 0.0115)
AX_SM = (AX_B[0] + AX_B[2] + 0.007, AX_B[1], 0.0205, AX_B[3])
AX_C = (AX_B[0], 0.165, AX_B[2], 0.110)
XR = 0.575


def bx(v):
    return AX_B[0] + v / FMAX * AX_B[2]


def by(v):
    return AX_B[1] + v / FMAX * AX_B[3]


def draw_cell(ax, x, y, k_or_type, r=None, gr=None, z=6):
    """Static cell icon (legend)."""
    t = k_or_type
    if t == 3:
        ax.add_patch(Circle((x, y), r, fc="0.35", ec="k", lw=0.5, zorder=z))
        return
    ax.add_patch(Circle((x, y), r, fc="white", ec="k", lw=0.8, zorder=z))
    if gr is not None and len(gr):
        ax.plot(x + gr[:, 0], y + gr[:, 1], "o", ms=1.9, color="k", mew=0, zorder=z + 1)


# ================================================================== figure
def build():
    fig = plt.figure(figsize=(7.2, 12.8), dpi=100)
    fig.patch.set_facecolor("white")
    T = {}
    fig.text(0.035, 0.965, r"\textbf{(a) how a flow cytometer sees cells}", fontsize=13.5,
             va="center")
    T["counter"] = fig.text(0.64, 0.965, "", fontsize=20, va="center")
    T["caption"] = fig.text(0.64, 0.943, "", fontsize=10.5, va="center", color="0.3")
    T["phase"] = fig.text(0.64, 0.929, "", fontsize=10.5, va="center", color="0.3")

    # ---------------- (a) flow cell, laser, detectors
    ax = fig.add_axes(AX_A)
    ax.axis("off")
    ax.set_xlim(*XL)
    ax.set_ylim(*YL)
    yy = np.linspace(Y_BOT - 0.05, Y_TOP + 0.05, 500)
    ww = wall(yy)
    inner = np.concatenate([np.column_stack([-ww, yy]), np.column_stack([ww[::-1], yy[::-1]])])
    fluid = Polygon(inner, closed=True, fc="0.965", ec="none", zorder=0)
    ax.add_patch(fluid)
    ax.plot(-ww, yy, color="k", lw=1.0, zorder=3)
    ax.plot(ww, yy, color="k", lw=1.0, zorder=3)
    yc = np.linspace(Y_BOT - 0.05, Y_TIP, 300)
    hc = CORE_END + (TUBE_IN - CORE_END) * qlat(yc)
    ax.fill_betweenx(yc, -hc, hc, color="0.89", lw=0, zorder=1)
    ax.add_patch(Rectangle((-TUBE_IN, Y_TIP), 2 * TUBE_IN, Y_TOP + 0.1 - Y_TIP, fc="0.89",
                           ec="none", zorder=1))
    for x0 in (-TUBE_OUT, TUBE_IN):
        ax.add_patch(Rectangle((x0, Y_TIP), TUBE_OUT - TUBE_IN, Y_TOP + 0.1 - Y_TIP,
                               fc="0.6", ec="k", lw=0.6, zorder=3))
    for xs in (-0.40, 0.40):
        ax.annotate("", xy=(xs, 2.02), xytext=(xs, 2.50), zorder=2,
                    arrowprops=dict(arrowstyle="-|>,head_length=0.45,head_width=0.22",
                                    color="0.5", lw=0.9))
    clip = PathPatch(Path(inner), fc="none", ec="none", transform=ax.transData)
    ax.add_patch(clip)

    # laser and beam (soft band = the beam profile; the pulse is the cell crossing it)
    ax.add_patch(Rectangle((-1.95, Y_LASER - 0.10), X_LASER0 + 1.95, 0.20, fc="0.3",
                           ec="k", lw=0.7, zorder=3))
    yb = np.linspace(-0.3, 0.3, 61)
    rgba = np.zeros((len(yb), 2, 4))
    rgba[..., 3] = 0.20 * np.exp(-2 * yb ** 2 / W0 ** 2)[:, None]
    ax.imshow(rgba, extent=(X_LASER0, X_STOP, Y_LASER - 0.3, Y_LASER + 0.3), origin="lower",
              aspect="auto", zorder=1.5, interpolation="bilinear")
    ax.plot([X_LASER0, X_STOP], [Y_LASER, Y_LASER], color="k", lw=0.8, zorder=1.6)
    ax.add_patch(Rectangle((X_STOP, Y_LASER - 0.12), 0.06, 0.24, fc="k", ec="k", lw=0.5,
                           zorder=3))
    ax.add_patch(Ellipse((X_FLENS, Y_LASER), 0.09, 0.54, fc="0.85", ec="k", lw=0.8, zorder=3))
    T["det_f"] = Rectangle((X_FDET, Y_LASER - 0.16), 0.13, 0.32, fc="0.8", ec="k", lw=0.7,
                           zorder=3)
    ax.add_patch(T["det_f"])
    ax.add_patch(Ellipse(tuple(C_SLENS), 0.09, 0.56, angle=-45, fc="0.85", ec="k", lw=0.8,
                         zorder=3))
    corners = [C_SDET + a * 0.065 * SSC_DIR + b * 0.16 * SSC_N
               for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    T["det_s"] = Polygon(corners, closed=True, fc="0.8", ec="k", lw=0.7, zorder=3)
    ax.add_patch(T["det_s"])
    T["ray_f"] = LineCollection([], colors="0.5", linewidths=0.9, zorder=2.5)
    T["ray_s"] = LineCollection([], colors="0.5", linewidths=0.9, zorder=2.5)
    ax.add_collection(T["ray_f"])
    ax.add_collection(T["ray_s"])

    def lab(x_from, y_from, name, what, y_text, x_text=2.2):
        ax.plot([x_from, x_text - 0.07], [y_from, y_text], color="k", lw=0.5, zorder=1)
        ax.text(x_text, y_text + 0.095, name, va="center", fontsize=11.5)
        ax.text(x_text, y_text - 0.095, what, va="center", fontsize=10.5, color="0.3")
    lab(TUBE_OUT, 2.48, "sample", "white blood cells in liquid", 2.45)
    lab(FUN_W, 2.12, "sheath fluid", "squeezes cells into single file", 1.85)
    lab(X_STOP + 0.06, Y_LASER + 0.10, "beam stop", "blocks the direct beam", 1.22)
    lab(X_FDET + 0.13, Y_LASER, "forward scatter (FSC)", "light bent a little: size", 0.52)
    p = C_SDET + 0.065 * SSC_DIR + 0.10 * SSC_N
    lab(p[0], p[1], "side scatter (SSC)", "light bounced sideways: granules", -0.42)
    ax.text(-1.95, Y_LASER - 0.25, "laser", va="center", fontsize=11.5)
    ax.text(-1.95, Y_LASER - 0.43, "488 nm", va="center", fontsize=10.5, color="0.3")

    # legend: the four kinds of particle, drawn like the moving ones
    T["leg_arrow"] = []
    leg_y = (2.45, 2.17, 1.89, 1.61)
    demo = {0: (7.0, 2), 1: (10.2, 5), 2: (9.9, 12), 3: (2.6, 0)}
    for t, yv in zip((0, 1, 2, 3), leg_y):
        d, ng = demo[t]
        r = d * R_PER_UM
        g = 0.62 * r * _sunflower[ng] if ng else None
        draw_cell(ax, -1.75, yv, t, r=r, gr=g)
        ax.text(-1.58, yv, NAMES[t], va="center", fontsize=10.5)
        T["leg_arrow"].append(ax.text(-1.99, yv, r"$\blacktriangleright$", fontsize=9,
                                      va="center", visible=False))
    ax.text(-1.95, 1.30, "(not to scale;", va="center", fontsize=10.5, color="0.4")
    ax.text(-1.95, 1.12, r"SSC is really at $90^\circ$)", va="center", fontsize=10.5,
            color="0.4")

    # moving particles
    T["cells"] = []
    for _ in range(40):
        c = Circle((0, 0), 0.1, fc="white", ec="k", lw=0.8, zorder=4, visible=False)
        ax.add_patch(c)
        c.set_clip_path(clip)
        T["cells"].append(c)
    T["gran"] = ax.scatter(np.zeros(0), np.zeros(0), s=3.6, c="k", lw=0, zorder=5)
    T["gran"].set_clip_path(clip)

    # ---------------- meters (share axes with (b))
    axf = fig.add_axes(AX_FM)
    axf.axis("off")
    axf.set_xlim(0, FMAX)
    axf.set_ylim(0, 1)
    axf.add_patch(Rectangle((0, 0), FMAX, 1, fc="white", ec="k", lw=0.7, zorder=1,
                           clip_on=False))
    T["fbar"] = Rectangle((0, 0), 0, 1, fc="0.5", ec="none", zorder=2)
    axf.add_patch(T["fbar"])
    axf.plot([THRESH, THRESH], [-0.5, 1.5], ls=(0, (2, 1.5)), color="k", lw=0.9,
             clip_on=False, zorder=3)
    T["fticks"] = LineCollection([], colors="k", linewidths=1.6, zorder=4)
    T["fticks"].set_clip_on(False)
    axf.add_collection(T["fticks"])
    T["fx"] = axf.plot([], [], "x", ms=7, mew=1.5, color="k", clip_on=False, zorder=5)[0]
    T["fpeak"] = axf.text(0, 1.9, "peak", ha="center", va="bottom", fontsize=10,
                          visible=False)
    fig.text(AX_FM[0] - 0.008, AX_FM[1] + AX_FM[3] / 2, "FSC", ha="right", va="center",
             fontsize=11)
    fig.text(bx(THRESH), AX_FM[1] + AX_FM[3] + 0.010, "threshold", ha="center",
             va="center", fontsize=10, color="0.35")
    T["axf"] = axf

    axs = fig.add_axes(AX_SM)
    axs.axis("off")
    axs.set_ylim(0, FMAX)
    axs.set_xlim(0, 1)
    axs.add_patch(Rectangle((0, 0), 1, FMAX, fc="white", ec="k", lw=0.7, zorder=1,
                           clip_on=False))
    T["sbar"] = Rectangle((0, 0), 1, 0, fc="0.5", ec="none", zorder=2)
    axs.add_patch(T["sbar"])
    T["sticks"] = LineCollection([], colors="k", linewidths=1.6, zorder=4)
    T["sticks"].set_clip_on(False)
    axs.add_collection(T["sticks"])
    T["speak"] = axs.text(1.9, 0, "peak", ha="left", va="center", fontsize=10,
                          visible=False)
    fig.text(AX_SM[0] + AX_SM[2] / 2, AX_SM[1] - 0.012, "SSC", ha="center", va="center",
             fontsize=11)
    fig.text(0.030, AX_B[1] + AX_B[3] / 2, "SSC peak", rotation=90, ha="center", va="center",
             fontsize=11)

    # ---------------- (b) FSC vs SSC
    axb = fig.add_axes(AX_B)
    axb.set_xlim(0, FMAX)
    axb.set_ylim(0, FMAX)
    axb.set_xticks([0, 400, 800])
    axb.set_yticks([0, 400, 800])
    axb.tick_params(labelbottom=False)
    axb.axvline(THRESH, ls=(0, (2, 2)), color="0.7", lw=0.8, zorder=1)
    T["dots"] = axb.scatter(np.zeros(0), np.zeros(0), s=5.0, c="k", lw=0, alpha=0.6,
                            zorder=3)
    T["gates"], T["glabels"] = [], []
    gl_pos = ((300, 190), (705, 98), (624, 975))
    for (cx, cy, a, b), (lx, ly), name in zip(GATES, gl_pos,
                                              ("lymphocytes", "monocytes", "granulocytes")):
        e = Ellipse((cx, cy), 2 * a, 2 * b, fill=False, ec="k", lw=0.9, ls=(0, (3, 2)),
                    zorder=4, visible=False)
        axb.add_patch(e)
        T["gates"].append(e)
        T["glabels"].append(axb.text(lx, ly, name, ha="center", va="center", fontsize=10.5,
                                     zorder=5, visible=False))
    T["newdot"] = axb.plot([], [], "o", ms=3.6, color="k", mew=0, zorder=7)[0]
    T["halo"] = axb.plot([], [], "o", ms=15, mfc="none", mec="white", mew=3.4, zorder=6)[0]
    T["ring"] = axb.plot([], [], "o", ms=15, mfc="none", mec="k", mew=1.4, zorder=7)[0]
    T["rtxt"] = axb.text(0, 0, "", fontsize=10.5, va="center", zorder=8,
                         bbox=dict(fc="white", ec="none", pad=1.0))
    T["dtxt"] = axb.text(140, 820, "", fontsize=10.5, va="center", zorder=8, linespacing=1.4)
    T["axb"] = axb

    fig.text(XR, 0.548, r"\textbf{(b) one cell, one dot}", fontsize=13.5, va="center")
    fig.text(XR, 0.530, "dot at (FSC peak, SSC peak)", fontsize=10.5, va="center",
             color="0.3")
    fig.add_artist(Rectangle((XR, 0.496), 0.035, 0.009, fc="0.5", ec="none",
                             transform=fig.transFigure))
    fig.text(XR + 0.045, 0.500, "detector signal now", fontsize=10.5, va="center")
    fig.add_artist(Line2D([XR + 0.0175, XR + 0.0175], [0.474, 0.488], color="k", lw=1.6))
    fig.text(XR + 0.045, 0.481, "its peak", fontsize=10.5, va="center")
    fig.add_artist(Ellipse((XR + 0.0175, 0.462), 0.035, 0.011, fill=False, ec="k", lw=0.9,
                           ls=(0, (3, 2)), transform=fig.transFigure))
    fig.text(XR + 0.045, 0.462, "gate: one cell type", fontsize=10.5, va="center")
    T["rhead"] = fig.text(XR, 0.425, "share of cells", fontsize=10.5, va="center",
                          color="0.3")
    fig.text(0.845, 0.425, "measured", fontsize=10.5, va="center", ha="right", color="0.3")
    fig.text(0.965, 0.425, "expected", fontsize=10.5, va="center", ha="right", color="0.3")
    T["rows"] = []
    for i, name in enumerate(("lymphocytes", "monocytes", "granulocytes")):
        yv = 0.402 - 0.021 * i
        fig.text(XR, yv, name, fontsize=11, va="center")
        T["rows"].append(fig.text(0.845, yv, "", fontsize=11, va="center", ha="right"))
        fig.text(0.965, yv, rf"{SHARE_EXP[i] * 100:.0f}\%", fontsize=11, va="center",
                 ha="right", color="0.3")

    # ---------------- (c) FSC histogram
    axc = fig.add_axes(AX_C)
    edges = np.arange(NB + 1) * BW
    T["meas"] = axc.stairs(np.zeros(NB), edges, fill=True, color="0.62", lw=0, zorder=1)
    T["exp"] = axc.stairs(np.zeros(NB), edges, fill=False, color="k", lw=1.0, zorder=3,
                          visible=False)
    T["unit"] = Rectangle((0, 0), BW, 1, fc="k", ec="none", zorder=2, visible=False)
    axc.add_patch(T["unit"])
    axc.axvline(THRESH, ls=(0, (2, 2)), color="0.45", lw=0.8, zorder=2)
    tr = blended_transform_factory(axc.transData, axc.transAxes)
    T["clab"] = [axc.text(300, 0.84, "lymphocytes", transform=tr, ha="center", va="center",
                          fontsize=10.5, zorder=4, visible=False),
                 axc.text(870, 0.62, "monocytes +\ngranulocytes", transform=tr,
                          ha="center", va="center", fontsize=10.5, zorder=4,
                          linespacing=1.3, visible=False)]
    axc.set_xlim(0, FMAX)
    axc.set_xticks([0, 400, 800])
    axc.yaxis.set_major_locator(MaxNLocator(nbins=3, integer=True, min_n_ticks=2))
    axc.text(0.0, 1.04, "cells", transform=axc.transAxes, ha="left", va="bottom",
             fontsize=11)
    axc.text(1.0, -0.21, "FSC peak", transform=axc.transAxes, ha="right", va="top",
             fontsize=11)
    T["axc"] = axc
    fig.text(XR, 0.262, r"\textbf{(c) size alone (FSC)}", fontsize=13.5, va="center")
    fig.text(XR, 0.244, "cells per FSC bin", fontsize=10.5, va="center", color="0.3")
    fig.add_artist(Rectangle((XR, 0.210), 0.035, 0.010, fc="0.62", ec="none",
                             transform=fig.transFigure))
    fig.text(XR + 0.045, 0.215, "measured", fontsize=10.5, va="center")
    fig.add_artist(Line2D([XR, XR + 0.035], [0.197, 0.197], color="k", lw=1.0))
    fig.text(XR + 0.045, 0.197, "expected", fontsize=10.5, va="center")
    fig.add_artist(Line2D([XR, XR + 0.035], [0.179, 0.179], color="0.45", lw=0.8,
                          ls=(0, (2, 2))))
    fig.text(XR + 0.045, 0.179, "threshold", fontsize=10.5, va="center")
    fig.text(XR, 0.150, "monocytes and granulocytes", fontsize=10.5, va="center",
             color="0.3")
    fig.text(XR, 0.134, "overlap here; SSC splits them", fontsize=10.5, va="center",
             color="0.3")

    # ---------------- guides shared by the meters, (b) and (c)
    T["gv"] = fig.add_artist(Line2D([0, 0], [AX_C[1], AX_FM[1] + AX_FM[3]], ls=(0, (3, 2)),
                                    color="0.35", lw=0.9, visible=False))
    T["gh"] = fig.add_artist(Line2D([0, 0], [0, 0], ls=(0, (3, 2)), color="0.35", lw=0.9,
                                    visible=False))

    # ---------------- equation + takeaway
    fig.text(0.5, 0.094, r"$\mathrm{FSC} \propto d^{\,2}, \qquad \mathrm{SSC} \propto g$",
             ha="center", va="center", fontsize=16)
    fig.text(0.5, 0.058, r"$d$: cell diameter,\ \ $g$: granularity (granules inside);"
             r"\ \ both are rough rules", ha="center", va="center", fontsize=11,
             color="0.25")
    fig.text(0.5, 0.027, r"size alone gives 2 groups; size $+$ granularity gives 3",
             ha="center", va="center", fontsize=13.5)
    return fig, T


def single_now(f):
    """Index of the stage-1 particle whose window contains f, else None."""
    if f >= S1_ON[5] or f < S1_ON[0]:
        return None
    return int(np.searchsorted(S1_ON, f, side="right") - 1)


def update(f, T):
    f = min(f, N_ANIM - 1)
    n, nd = int(N_REC[f]), int(N_DEB[f])
    T["counter"].set_text(rf"$N = {fmt_int(n)}$")
    T["caption"].set_text(rf"cells recorded ({nd} debris skipped)" if nd else
                          "cells recorded")
    T["phase"].set_text("(one cell at a time)" if f < S2 else
                        ("(sped up)" if f < F_STOP else "(done)"))

    # ------- (a) particles in the flow cell
    s = S0 + CUM[f]
    vis = np.nonzero((s > 0.15) & (s < _SG[-1] - 0.15))[0]
    ys = y_of_s(s[vis])
    keep = (ys < Y_TOP + 0.15) & (ys > Y_BOT - 0.15)
    vis, ys = vis[keep], ys[keep]
    xs = ST["xi"][vis] * ST["lat"][vis] * qlat(ys)
    gx, gy = [], []
    for c, k, x, y in zip(T["cells"], vis, xs, ys):
        c.set_center((x, y))
        c.set_radius(RAD[k])
        if TYP[k] == 3:
            c.set_facecolor("0.35")
            c.set_linewidth(0.5)
        else:
            c.set_facecolor("white")
            c.set_linewidth(0.8)
            g = granules(k)
            gx.append(x + g[:, 0])
            gy.append(y + g[:, 1])
        c.set_visible(True)
    for c in T["cells"][len(vis):]:
        c.set_visible(False)
    T["gran"].set_offsets(np.column_stack([np.concatenate(gx), np.concatenate(gy)])
                          if gx else np.zeros((0, 2)))

    # ------- detectors, rays, meters
    bf, bs = float(BAR_F[f]), float(BAR_S[f])
    T["det_f"].set_facecolor(str(0.8 - 0.65 * min(1.0, bf / 600)))
    T["det_s"].set_facecolor(str(0.8 - 0.65 * min(1.0, bs / 600)))
    oy = float(RAY_Y[f])
    if bf > 4:
        T["ray_f"].set_segments([[(0, oy), (X_FLENS, Y_LASER + sg * 0.23), (X_FDET, Y_LASER)]
                                 for sg in (1, -1)])
        T["ray_f"].set_color(str(1 - 0.85 * min(1.0, bf / 600)))
    else:
        T["ray_f"].set_segments([])
    if bs > 4:
        face = C_SDET - 0.065 * SSC_DIR
        T["ray_s"].set_segments([[(0, oy), tuple(C_SLENS + sg * 0.24 * SSC_N), tuple(face)]
                                 for sg in (1, -1)])
        T["ray_s"].set_color(str(1 - 0.85 * min(1.0, bs / 600)))
    else:
        T["ray_s"].set_segments([])
    T["fbar"].set_width(bf)
    T["sbar"].set_height(bs)

    for a in T["leg_arrow"]:
        a.set_visible(False)
    for key in ("halo", "ring", "fx", "newdot"):
        T[key].set_data([], [])
    T["rtxt"].set_text("")
    T["dtxt"].set_text("")
    T["fpeak"].set_visible(False)
    T["speak"].set_visible(False)
    T["gv"].set_visible(False)
    T["gh"].set_visible(False)
    T["unit"].set_visible(False)

    i = single_now(f)
    if i is not None:
        T["leg_arrow"][S1_T[i]].set_visible(True)
        hf = FSC[i] if f >= E1[i] else min(FSC[i], BAR_F[S1_ON[i]:f + 1].max())
        hs = SSC[i] if f >= E1[i] else min(SSC[i], BAR_S[S1_ON[i]:f + 1].max())
        T["fticks"].set_segments([[(hf, -0.5), (hf, 1.5)]])
        T["sticks"].set_segments([[(-0.5, hs), (1.5, hs)]])
        if f >= E1[i]:
            if TYP[i] == 3:
                T["fx"].set_data([FSC[i]], [0.5])
                T["fticks"].set_segments([])
                T["sticks"].set_segments([])
                T["dtxt"].set_text("debris: FSC below threshold\nso it is not recorded")
            else:
                x, y = FSC[i], SSC[i]
                T["newdot"].set_data([x], [y])
                T["halo"].set_data([x], [y])
                T["ring"].set_data([x], [y])
                T["rtxt"].set_position((x + 60, y + 52))
                T["rtxt"].set_text(S1_TXT[i])
                gx_ = bx(x)
                T["gv"].set_xdata([gx_, gx_])
                T["gv"].set_visible(True)
                T["gh"].set_data([gx_, AX_SM[0]], [by(y), by(y)])
                T["gh"].set_visible(True)
                b = BIN_R[int(np.searchsorted(REC_IDX, i))]
                hb = np.bincount(BIN_R[:n], minlength=NB)[b]
                T["unit"].set_xy((b * BW, hb - 1))
                T["unit"].set_visible(True)
                if i == 0:
                    T["fpeak"].set_x(x)
                    T["fpeak"].set_visible(True)
                    T["speak"].set_y(y)
                    T["speak"].set_visible(True)
    else:
        tk = TICKS[f]
        T["fticks"].set_segments([[(v, -0.5), (v, 1.5)] for v in tk[:, 0]])
        T["sticks"].set_segments([[(-0.5, v), (1.5, v)] for v in tk[:, 1]])

    # ------- (b)
    T["dots"].set_offsets(XY_R[:n])
    show_g = n >= N_GATE_SHOW
    for e, t in zip(T["gates"], T["glabels"]):
        e.set_visible(show_g)
        t.set_visible(show_g)
    if show_g:
        g = GCUM[n].astype(float)
        sh = g / max(1.0, g.sum()) * 100
        for row, v in zip(T["rows"], sh):
            row.set_text(rf"{v:.0f}\%")
    else:
        for row in T["rows"]:
            row.set_text(r"$\ldots$")

    # ------- (c)
    h = np.bincount(BIN_R[:n], minlength=NB).astype(float)
    T["meas"].set_data(values=h)
    show_e = n >= N_EXP_SHOW
    T["exp"].set_data(values=PBIN * n)
    T["exp"].set_visible(show_e)
    for t in T["clab"]:
        t.set_visible(show_e)
    T["axc"].set_ylim(0, YTOP[f])
    return []


def main():
    mode = sys.argv[1]
    if mode == "scan":
        seed_scan(int(sys.argv[2]), int(sys.argv[3]))
        return
    if mode == "info":
        print(f"seed {SEED}, u_max {U_MAX:.4f}, end slack {END_SLACK:.2f} w, particles {NPART}")
        print("gate coverage", np.round(GATE_COVER, 4), " expected shares",
              np.round(SHARE_EXP * 100, 2))
        print(f"recorded {N_REC[-1]}, debris skipped {N_DEB[-1]}")
        g = GCUM[N_REC[-1]].astype(float)
        print("final shares", np.round(g / g.sum() * 100, 2))
        print("singles: land", LAND[:6], " pulse start", PSTART[:6], " windows", S1_ON)
        print("S_LASER", round(S_LASER, 3), " s range", round(_SG[-1], 3))
        for f in (0, 40, 96, 152, 208, 264, 289, 300, 320, 360, 420, 500, 700, 731, 745,
                  751, 759):
            print(f"f={f:3d} u={U[min(f, N_ANIM - 1)]:6.3f} N={N_REC[f]:5d} deb={N_DEB[f]:4d} "
                  f"barF={BAR_F[f]:6.1f} barS={BAR_S[f]:6.1f} ytop={YTOP[f]:6.1f} "
                  f"events={_ev_start[f + 1] - _ev_start[f]}")
        print("max events per frame", np.max(np.diff(_ev_start)))
        return
    fig, T = build()
    if mode == "still":
        update(int(sys.argv[2]), T)
        fig.savefig(sys.argv[3], dpi=100)
    elif mode == "stills":                       # stills F1,F2,... DIR
        for fr in sys.argv[2].split(","):
            update(int(fr), T)
            fig.savefig(os.path.join(sys.argv[3], f"f{int(fr):03d}.png"), dpi=100)
    elif mode == "render":
        a, b, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
        anim = FuncAnimation(fig, update, frames=range(a, b), fargs=(T,),
                             blit=False, cache_frame_data=False)
        writer = FFMpegWriter(fps=FPS, codec="libx264",
                              extra_args=["-pix_fmt", "yuv420p", "-preset", "veryfast",
                                          "-crf", "18", "-bf", "0"])
        anim.save(out, writer=writer, dpi=100)


if __name__ == "__main__":
    main()
