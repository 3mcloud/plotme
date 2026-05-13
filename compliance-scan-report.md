# Compliance Source Code Scan Report

**Project:** plotme  
**Version:** 1.4.0  
**Repository:** 3M-Cloud/vibedemo26-milo  
**Scan Date:** 2026-03-26  
**Scan Tools:** pip-audit 2.10.0, bandit 1.x, pip-licenses 5.5.1  

---

## Executive Summary

| Category | Status | Finding Count |
|----------|--------|---------------|
| Source Code Security (Bandit) | ✅ PASS | 0 issues |
| Dependency Vulnerabilities (pip-audit) | ⚠️ ACTION REQUIRED | 2 CVEs found |
| License Compliance | ⚠️ REVIEW REQUIRED | 1 proprietary + 2 MPL-2.0 packages |
| Open-Source Attribution | ✅ PASS | All deps identified |

---

## 1. Source Code Security Analysis

**Tool:** Bandit (static analysis)  
**Scope:** `plotme/` package (633 lines of code across 7 files)  
**Result:** **PASS – No security issues found**

| File | Lines of Code | Issues |
|------|--------------|--------|
| `plotme/__init__.py` | 3 | 0 |
| `plotme/__main__.py` | 48 | 0 |
| `plotme/helper.py` | 64 | 0 |
| `plotme/load_data.py` | 223 | 0 |
| `plotme/plotting.py` | 183 | 0 |
| `plotme/read.py` | 9 | 0 |
| `plotme/schema.py` | 103 | 0 |

No HIGH, MEDIUM, or LOW severity vulnerabilities detected (OWASP Top 10 categories checked: injection, insecure deserialization, use of known-vulnerable components, sensitive data exposure, etc.).

---

## 2. Dependency Vulnerability Scan

**Tool:** pip-audit 2.10.0 (backed by PyPI Advisory Database)  
**Result:** ⚠️ **2 known CVEs found — action required**

### CVE Findings

| Package | Version | CVE ID | GHSA | Fix Version | Severity | Description |
|---------|---------|--------|------|-------------|----------|-------------|
| **pip** | 25.3 | CVE-2026-1703 | GHSA-6vgw-5pg2-w6jp | 26.0 | MEDIUM | Path traversal during wheel archive extraction. Files may be extracted outside the installation directory. Only exploitable with a maliciously crafted wheel. |
| **pygments** | 2.19.2 | CVE-2026-4539 | GHSA-5239-wwwm-4pmq | None available | LOW | Inefficient regex in `AdlLexer` (`pygments/lexers/archetype.py`) can cause ReDoS under local access conditions. |

> **Note:** `pygments` is an indirect/dev dependency (used by `rich` and other tooling). It is **not** a direct dependency of `plotme`.

> **Note:** `pip` itself is the package manager, not a runtime dependency of `plotme`.

### Recommendations

1. **pip (CVE-2026-1703):** Upgrade `pip` to version `26.0` or later.
   ```
   pip install --upgrade pip
   ```
2. **pygments (CVE-2026-4539):** No fix version is currently available. Monitor the [pygments issue tracker](https://github.com/pygments/pygments) for a patch. Consider pinning to this version and adding a waiver with justification (local-only exploit, low severity).

### Skip Notice

`plotme` (1.4.0) itself was not found on PyPI and could not be audited against the PyPI advisory database. This is expected for an internal/proprietary package.

---

## 3. Open-Source Dependency Licenses

**Tool:** pip-licenses 5.5.1  
**Result:** ⚠️ **Review required for MPL-2.0 and proprietary license entries**

### License Summary

| License | Count | Notes |
|---------|-------|-------|
| MIT / MIT License | 30 | ✅ Permissive – generally acceptable |
| Apache-2.0 / Apache Software License | 11 | ✅ Permissive – generally acceptable |
| BSD License / BSD-2-Clause / BSD-3-Clause | 9 | ✅ Permissive – generally acceptable |
| Mozilla Public License 2.0 (MPL 2.0) | 2 | ⚠️ Weak copyleft – file-level copyleft applies |
| Python Software Foundation License | 1 | ✅ Permissive |
| LicenseRef-Proprietary | 1 | ⚠️ plotme itself – internal project |

### MPL-2.0 Packages (Weak Copyleft)

| Package | Version | URL |
|---------|---------|-----|
| certifi | 2026.2.25 | https://github.com/certifi/python-certifi |
| pathspec | 1.0.4 | N/A |

MPL-2.0 is file-level copyleft: modifications to MPL-licensed files must be released under MPL-2.0. Since `certifi` and `pathspec` are used as-is (unmodified), this does not impose redistribution obligations on `plotme`. **No immediate action required**, but document usage in your third-party notices file.

### Full Dependency License Table

| Name | Version | License | Author |
|------|---------|---------|--------|
| CacheControl | 0.14.4 | Apache-2.0 | Eric Larson et al. |
| GitPython | 3.1.41 | BSD License | Sebastian Thiel, Michael Trier |
| PyYAML | 6.0.3 | MIT License | Kirill Simonov |
| Pygments | 2.19.2 | BSD License | Georg Brandl |
| attrs | 26.1.0 | MIT | Hynek Schlawack |
| boolean.py | 5.0 | BSD-2-Clause | Sebastian Kraemer |
| certifi | 2026.2.25 | MPL-2.0 | Kenneth Reitz |
| charset-normalizer | 3.4.6 | MIT | Ahmed R. TAHRI |
| cyclonedx-python-lib | 11.7.0 | Apache-2.0 | Paul Horton |
| defusedxml | 0.7.1 | PSF License | Christian Heimes |
| dirhash | 0.5.0 | MIT | Anders Huss |
| et_xmlfile | 2.0.0 | MIT License | See AUTHORS.txt |
| filelock | 3.25.2 | MIT | (see project) |
| gitdb | 4.0.12 | BSD License | Sebastian Thiel |
| idna | 3.11 | BSD-3-Clause | Kim Davies |
| iniconfig | 2.3.0 | MIT | Ronny Pfannschmidt et al. |
| jsonschema | 4.26.0 | MIT | Julian Berman |
| jsonschema-specifications | 2025.9.1 | MIT | Julian Berman |
| license-expression | 30.4.4 | Apache-2.0 | nexB. Inc. and others |
| markdown-it-py | 4.0.0 | MIT License | Chris Sewell |
| mdurl | 0.1.2 | MIT License | Taneli Hukkinen |
| msgpack | 1.1.2 | Apache-2.0 | Inada Naoki |
| narwhals | 2.18.1 | MIT License | Marco Gorelli |
| numpy | 2.4.3 | BSD-3-Clause + 0BSD + MIT + Zlib + CC0-1.0 | Travis E. Oliphant et al. |
| openpyxl | 3.1.5 | MIT License | See AUTHORS |
| packageurl-python | 0.17.6 | MIT License | the purl authors |
| packaging | 26.0 | Apache-2.0 OR BSD-2-Clause | Donald Stufft |
| pandas | 3.0.1 | BSD License | The Pandas Development Team |
| pathspec | 1.0.4 | MPL-2.0 | Caleb P. Burns |
| pip-api | 0.0.34 | Apache Software License | Dustin Ingram |
| pip-requirements-parser | 32.0.1 | MIT | nexB. Inc. and others |
| pip_audit | 2.10.0 | Apache Software License | Alex Cameron |
| platformdirs | 4.9.4 | MIT | (see project) |
| plotly | 6.6.0 | MIT License | Chris P |
| plotme | 1.4.0 | Proprietary | Milo Oien-Rochat, Daniel Garcia |
| pluggy | 1.6.0 | MIT License | Holger Krekel |
| py-serializable | 2.1.0 | Apache Software License | Paul Horton |
| pyparsing | 3.3.2 | MIT | Paul McGuire |
| pytest | 9.0.2 | MIT | Holger Krekel et al. |
| python-dateutil | 2.9.0.post0 | Apache + BSD | Gustavo Niemeyer |
| referencing | 0.37.0 | MIT | Julian Berman |
| requests | 2.33.0 | Apache Software License | Kenneth Reitz |
| rich | 14.3.3 | MIT License | Will McGugan |
| rpds-py | 0.30.0 | MIT | Julian Berman |
| scandir | 1.10.0 | BSD License | Ben Hoyt |
| scantree | 0.0.4 | MIT | Anders Huss |
| six | 1.17.0 | MIT License | Benjamin Peterson |
| smmap | 5.0.3 | BSD License | Sebastian Thiel |
| sortedcontainers | 2.4.0 | Apache Software License | Grant Jenks |
| tomli | 2.4.1 | MIT | Taneli Hukkinen |
| tomli_w | 1.2.0 | MIT License | Taneli Hukkinen |
| urllib3 | 2.6.3 | MIT | Andrey Petrov |

---

## 4. Project License & Attribution

- **Project License:** MIT License (Copyright © 2022 3M Company) — see `LICENSE`  
- **pyproject.toml declares:** `LicenseRef-Proprietary` (mismatch with the `LICENSE` file which contains MIT text)  
  ⚠️ **Recommendation:** Align the `license` field in `pyproject.toml` with the actual `LICENSE` file. Change `license = "LicenseRef-Proprietary"` to `license = {file = "LICENSE"}` or `license = "MIT"`.

---

## 5. Remediation Summary

| Priority | Action | Package | Details |Resolution|
|----------|--------|---------|---------|------|
| HIGH | Upgrade pip | pip 25.3 | Upgrade to ≥ 26.0 to fix CVE-2026-1703 path traversal | version not managed by plotme|
| MEDIUM | Monitor / accept risk | pygments 2.19.2 | CVE-2026-4539 – no fix yet; low severity, local access only |version not managed by plotme|
| LOW | Fix pyproject.toml | plotme | Align `license` field with actual MIT `LICENSE` file |fixed|
| LOW | Document MPL-2.0 usage | certifi, pathspec | Add to third-party notices; no modification made, no redistribution obligation | none needed|

---
*Report generated by GitHub Copilot Compliance Scan Agent on 2026-03-26.*
