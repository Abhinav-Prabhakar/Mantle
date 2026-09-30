"""R3: heavy-oil viscosity-temperature literature data (open access, CC BY 4.0).

Source: Alomair, Jumaa, Alkoriem, Hamed (2016) "Heavy oil viscosity and density prediction at normal and
elevated temperatures", J Pet Explor Prod Technol 6:253-263, doi:10.1007/s13202-015-0184-8 (30 heavy oils,
11.7-18.8 API, 20-160 C). Licence CC BY 4.0 (verified on the publisher page and in the PDF back matter).

LIMITATION: the article publishes only descriptive statistics of its 376 measurements (Table 1) and the
correlation coefficients (Table 6), not the per-sample viscosity-vs-temperature table. This module extracts
what is tabulated (Table 1: mean/min/max of API, T, viscosity, density) and labels those rows
``data_kind = column_statistic``: each row is a statistic of every column separately, NOT a measured
(T, viscosity) pair. They are usable as an envelope for sanity checks of the Walther fit, not as calibration
points. Replace with a sample-level dataset when one is available (same CSV columns).
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

from ..paths import raw_dir, reference_dir
from .common import download, sha256_file, update_licenses

PDF_URL = "https://d-nb.info/1102404020/34"
PDF_NAME = "visc_paper.pdf"
CITATION = ("Alomair O., Jumaa M., Alkoriem A., Hamed M. (2016) Heavy oil viscosity and density prediction at "
            "normal and elevated temperatures. J Pet Explor Prod Technol 6:253-263. "
            "doi:10.1007/s13202-015-0184-8")
LICENCE = "CC BY 4.0"
COLUMNS = ["sample_id", "api", "temperature_c", "viscosity_cp", "density_g_cc", "citation", "licence", "data_kind"]
# Table 1, transcribed (extraction verified against the PDF text in ``extract_table1``).
TABLE1 = {
    "mean": (16.1, 81.0, 281.2, 0.9),
    "min": (11.7, 20.0, 1.7, 0.8),
    "max": (18.8, 160.0, 11900.0, 1.0),
}


def extract_table1(pdf: Path) -> dict[str, tuple[float, float, float, float]]:
    """Parse Table 1 from the PDF text; falls back to the transcription when the layout differs."""
    import pdfplumber

    found: dict[str, tuple[float, float, float, float]] = {}
    with pdfplumber.open(pdf) as doc:
        text = "\n".join((p.extract_text() or "") for p in doc.pages[:3])
    for key, label in (("mean", "Mean"), ("min", "Minimum"), ("max", "Maximum")):
        m = re.search(rf"^{label}\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*$", text, re.M)
        if m and key != "max":
            found[key] = tuple(float(x) for x in m.groups())  # type: ignore[assignment]
    for key, ref in TABLE1.items():
        got = found.get(key)
        if got is None:
            found[key] = ref
        elif any(abs(a - b) > 1e-9 for a, b in zip(got, ref, strict=True)):
            raise ValueError(f"Table 1 {key} row differs from the transcription: {got} vs {ref}")
    return found


def rows_from(t1: dict[str, tuple[float, float, float, float]]) -> list[dict]:
    out = []
    for key, (api, t, mu, rho) in t1.items():
        out.append({
            "sample_id": f"ALOMAIR2016-T1-{key}", "api": api, "temperature_c": t, "viscosity_cp": mu,
            "density_g_cc": rho, "citation": CITATION, "licence": LICENCE, "data_kind": "column_statistic",
        })
    return out


def write_csv(rows: list[dict], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    return path


def fetch_viscosity(pdf: Path | None = None) -> Path:
    """Download (idempotent) the OA PDF, extract the tabulated data, write the raw + reference CSV."""
    pdf = pdf or raw_dir() / PDF_NAME
    if not pdf.exists():
        download(PDF_URL, pdf)
    rows = rows_from(extract_table1(pdf))
    raw_csv = write_csv(rows, raw_dir() / "viscosity_literature.csv")
    write_csv(rows, reference_dir() / "viscosity_literature.csv")
    update_licenses(
        raw_dir(), "R3 Viscosity literature",
        f"{CITATION}. Licence: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). PDF sha256 "
        f"{sha256_file(pdf)[:16]}... Only Table 1 (descriptive statistics) is tabulated in the article.",
    )
    return raw_csv
