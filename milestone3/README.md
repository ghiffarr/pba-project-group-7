# Group 7 - Milestone 3
Submit output/Group7_Milestone3.pdf.

## Run
Python 3.12 was used. Install dependencies with:
pip install pandas numpy reportlab
Recreate the figures and report from the supplied cleaned data:
python 02_figures_report.py

Rebuild from original public source files (network required):
python 00_download.py
python 01_build_data.py
python 02_figures_report.py

The code runs relative to its own directory. No R installation or API key is needed.
Raw compressed source files are excluded from this ZIP (~62 MB combined).
source_manifest.json stores exact URLs, byte sizes and SHA256 checksums from the download on 2026-11-13.
00_download.py rejects changed source bytes instead of silently claiming exact reproduction.
The supplied cleaned CSV and summary files reproduce the submitted figures without downloading anything.
The report script reads summaries produced by 01_build_data.py; rerun the build after changing sample rules.
output/ contains the submission PDF and standalone PDF/SVG figures.
data/codebook.md defines the fields and sample rules. data/audit.json records sample attrition. data/league_summary.csv and position_summary.csv are chart inputs.
No model has been fitted. This milestone is descriptive.
The original proposal's statistics were unverified. The verified report uses 2015/16-2024/25 (ten seasons).
2025/26 is excluded because source valuations stop before July 2026.
