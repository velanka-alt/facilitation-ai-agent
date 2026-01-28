# Tests (Samples)

This folder stores manual sample cases for each mode.
Each file includes input and expected output following the templates.

Guidelines:
- Keep inputs realistic and minimal.
- Ensure outputs follow the exact template order.
- Update samples whenever templates change.

Sample corpus (gesia_all):
- Location: `samples/gesia_all/`
- Index: `samples/gesia_all/_index.csv` (Category, ProgramName, DocType, Time, FileName, SourcePath)
- Files are text extracts (`.txt`) converted from the local originals.
- Use the index to pick representative cases across categories and doc types.
- Keep all anonymized tokens (e.g., `조직NN`, `프로젝트NN`) as-is.
- Do not add extra sections to templates. If you need provenance, add a one-line HTML comment at the top, e.g.
  `<!-- Source: samples/gesia_all/교육자료/교육자료_조직05 ... -->`
