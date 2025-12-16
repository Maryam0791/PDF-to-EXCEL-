import pdfplumber
import pandas as pd
import re
from io import BytesIO


PRODUCT_CODE_REGEX = r"(HW|SW)\d{8}"
DATE_RANGE_REGEX = r"from\s+(.*?)\s+to\s+(.*?)\s*\("
REGION_REGEX = r"(WESTERN|EASTERN|CENTRAL)\s+REGION"
QTY_REGEX = r"\((\d+)\s+Store"


def convert_pdf_to_dataframe(pdf_bytes):
    rows = []
    current_row = None

    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            for line in text.split("\n"):
                line = line.strip()

                # Skip headers / footers
                if line.startswith(("Sr", "Order", "VAT", "Thursday", "Wednesday", "FAMA")):
                    continue

                # PRODUCT LINE
                code_match = re.search(PRODUCT_CODE_REGEX, line)
                if code_match:
                    current_row = {
                        "S.No": len(rows) + 1,
                        "Product Code": code_match.group(),
                        "Description": re.sub(PRODUCT_CODE_REGEX, "", line).strip(),
                        "Region": "",
                        "Start Date": "",
                        "End Date": "",
                        "Quantity": ""
                    }

                    qty_match = re.search(QTY_REGEX, line)
                    if qty_match:
                        current_row["Quantity"] = qty_match.group(1)

                    rows.append(current_row)
                    continue

                # REGION LINE
                if current_row:
                    region_match = re.search(REGION_REGEX, line)
                    if region_match:
                        current_row["Region"] = region_match.group(1)
                        continue

                # DATE RANGE LINE
                if current_row:
                    date_match = re.search(DATE_RANGE_REGEX, line, re.IGNORECASE)
                    if date_match:
                        current_row["Start Date"] = date_match.group(1)
                        current_row["End Date"] = date_match.group(2)
                        continue

                # CONTINUATION OF DESCRIPTION
                if current_row and line and not line.lower().startswith("unit"):
                    current_row["Description"] += " " + line

    return pd.DataFrame(rows)

