import pandas as pd
import json
import os
from datetime import datetime

def create_allure_result(test_name, status, details=""):
    now = int(datetime.now().timestamp() * 1000)
    return {
        "name": test_name,
        "status": status,
        "statusDetails": {
            "message": details
        },
        "start": now,
        "stop": now + 1
    }

def convert_excel_to_allure(excel_path, output_dir):
    df = pd.read_excel(excel_path)
    os.makedirs(output_dir, exist_ok=True)

    for index, row in df.iterrows():
        test_name = f"{row['OWASP']} | {row['Group']} | {row['Subgroup']} | {row['Category']}"
        status = "passed" if row['Success'] else "failed"
        details = (
            f"Risk: {row['Risk']}\n\n"
            f"Attack prompt: {row['Attack prompt']}\n\n"
            f"Response: {row['Response']}"
        )

        allure_result = create_allure_result(test_name, status, details)
        filename = os.path.join(output_dir, f"result-{index}.json")

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(allure_result, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    excel_path = os.getenv("REPORT_FILE_PATH")
    output_dir = 'allure-results'

    convert_excel_to_allure(excel_path, output_dir)
    print(f"✅ Allure results created in {output_dir}")