import os
import json
import requests
import xlsxwriter
import re


def load_cases(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_path(steps: str):
    m = re.search(r"BASE_URL(/[^\s>]*)", steps)
    if m:
        return m.group(1)
    return "/"


def main():
    base = os.path.dirname(__file__)
    tc_path = os.path.join(base, 'testcases.json')
    out_xlsx = os.path.join(base, 'E2E_Test_Results_veritask-share.xlsx')
    base_url = os.environ.get('BASE_URL', 'https://example.com').rstrip('/')

    cases = load_cases(tc_path)

    wb = xlsxwriter.Workbook(out_xlsx)
    ws = wb.add_worksheet('Results')
    bold = wb.add_format({'bold': True})
    ws.write_row(0, 0, ['ID', 'Title', 'Type', 'Steps', 'Expected', 'Priority', 'Status', 'HTTP Code'], bold)

    session = requests.Session()
    for r, c in enumerate(cases, start=1):
        path = extract_path(c.get('steps', ''))
        url = base_url + path
        status = 'not executed'
        code = ''
        try:
            resp = session.get(url, timeout=10)
            code = resp.status_code
            if resp.status_code < 400:
                status = 'passed'
            else:
                status = 'failed'
        except Exception as e:
            status = 'error'
            code = str(e)

        ws.write_row(r, 0, [c['id'], c['title'], c['type'], c['steps'], c['expected'], c.get('priority', ''), status, code])

    wb.close()
    print(f"Wrote {out_xlsx} with {len(cases)} results (base_url={base_url})")


if __name__ == '__main__':
    main()
