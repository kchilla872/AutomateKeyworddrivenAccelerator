import csv
import keywords


def execute_test_case(testcase_id, page):
    with open('test_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        # Filter steps for this test case and sort by StepNumber
        steps = sorted(
            [row for row in reader if row['TestCaseID'] == testcase_id],
            key=lambda x: int(x['StepNumber'])
        )
        for step in steps:
            keyword = step['Keyword']
            params = step['Parameters'].strip()
            func = getattr(keywords, keyword, None)
            if func is None:
                raise Exception(f"Keyword '{keyword}' is not implemented in keywords.py")

            if params:
                print(f"Executing keyword: {keyword} with params: {params}")
                func(page, params)
            else:
                print(f"Executing keyword: {keyword} with no params")
                func(page)
