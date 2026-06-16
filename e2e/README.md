# E2E test instructions (pytest + selenium)

- Install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

- Build and serve the Flutter web app locally (example):

```powershell
# from repo root
flutter build web --release
pushd build\web
python -m http.server 5000
popd
```

- Run the Selenium tests (assumes ChromeDriver on PATH):

```powershell
cd e2e
pytest -n auto -q
```

- Generate the Excel test case workbook:

```powershell
python generate_testcases_excel.py
```
