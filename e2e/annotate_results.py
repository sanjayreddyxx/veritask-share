import os
import json
import xml.etree.ElementTree as ET
import xlsxwriter


def load_cases(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_junit(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    results = {}
    for testcase in root.findall('.//testcase'):
        name = testcase.get('name') or ''
        # find TC id in name
        import re
        m = re.search(r'TC(\d+)', name)
        tcid = None
        if m:
            tcid = int(m.group(1))
        # determine status
        status = 'passed'
        if testcase.find('failure') is not None:
            status = 'failed'
        elif testcase.find('error') is not None:
            status = 'error'
        elif testcase.find('skipped') is not None:
            status = 'skipped'
        if tcid:
            results[tcid] = status
    return results


def main():
    base = os.path.dirname(__file__)
    tc_path = os.path.join(base, 'testcases.json')
    xml_path = os.path.join(base, 'results.xml')
    out_xlsx = os.path.join(base, 'E2E_Test_Results_veritask-share.xlsx')

    cases = load_cases(tc_path)
    junit = parse_junit(xml_path) if os.path.exists(xml_path) else {}

    wb = xlsxwriter.Workbook(out_xlsx)
    ws = wb.add_worksheet('Results')
    bold = wb.add_format({'bold': True})
    ws.write_row(0, 0, ['ID', 'Title', 'Type', 'Preconditions', 'Steps', 'Expected', 'Priority', 'Status'], bold)

    for r, c in enumerate(cases, start=1):
        status = junit.get(c['id'], 'not executed')
        ws.write_row(r, 0, [c['id'], c['title'], c['type'], c['preconditions'], c['steps'], c['expected'], c.get('priority', ''), status])

    wb.close()
    print(f"Wrote {out_xlsx}")


if __name__ == '__main__':
    main()
