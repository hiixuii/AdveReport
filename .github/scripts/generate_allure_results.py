import pandas as pd
import json
from datetime import datetime
import os
import uuid

def generate_allure_results(excel_path, allure_results_dir="allure-results"):
     # Verify file exists
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"Excel file not found at: {excel_path}")
        
    # Read Excel sheets
    responses_df = pd.read_excel(excel_path, sheet_name="Responses")
    result_owasp_df = pd.read_excel(excel_path, sheet_name="Result (OWASP)")
    
    # Create Allure results directory structure
    history_dir = os.path.join(allure_results_dir, "history")
    os.makedirs(history_dir, exist_ok=True)
    
    # Process each OWASP test case
    for _, row in responses_df.iterrows():
        owasp_id = row["OWASP"]
        success = row["Success"]
        full_prompt = row["Full prompt"]
        decision = row["Decision"]
        
        # Get success rate from Result (OWASP) sheet
        success_rate = result_owasp_df.loc[result_owasp_df["OWASP"] == owasp_id, "Attack success rate"].values[0]
        
        # Allure test case data
        test_case = {
            "name": f"{owasp_id}: {row['Category']}",
            "status": "failed" if success else "passed",
            "statusDetails": {"known": False, "muted": False, "flaky": False},
            "uuid": str(uuid.uuid4()),
            "historyId": owasp_id,
            "fullName": row["Category"],
            "labels": [
                {"name": "suite", "value": row["Group"]},
                {"name": "subSuite", "value": row["Subgroup"]},
                {"name": "OWASP", "value": owasp_id}
            ],
            "links": [],
            "start": int(datetime.now().timestamp() * 1000),
            "stop": int((datetime.now().timestamp() + 1) * 1000),
            "parameters": [
                {"name": "Risk", "value": str(row["Risk"])},
                {"name": "Success Rate", "value": str(success_rate)}
            ],
            "description": f"**Prompt**: {full_prompt}\n\n**Decision**: {decision}"
        }
        
        # Save as JSON file
        with open(os.path.join(allure_results_dir, f"{test_case['uuid']}-result.json"), "w") as f:
            json.dump(test_case, f)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python generate_allure_report.py <path_to_excel>")
        sys.exit(1)
    generate_allure_results(sys.argv[1])
