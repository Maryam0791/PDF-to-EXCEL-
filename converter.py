import pdfplumber
import pandas as pd
import re
import os


def pdf_to_excel(pdf_path, excel_path):
    rows = []
    s_no = 1

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            lines = text.split("\n")
            i = 0

            while i < len(lines):
                line = lines[i].strip()

                # -------------------------------
                # PRODUCT LINE (HW or SW)
                # -------------------------------
                product_match = re.match(
                    r"\s*\d+\s*-?\s*(HW\d+|SW\d+)\s*-?\s*(.*?)\s+(\d+)\s+Unit",
                    line
                )

                if product_match:
                    product_code = product_match.group(1)
                    description = product_match.group(2).strip()
                    quantity = product_match.group(3)

                    region = ""
                    start_date = ""
                    end_date = ""

                    # -------------------------------
                    # CHECK NEXT LINE → REGION
                    # -------------------------------
                    if i + 1 < len(lines):
                        region_match = re.search(
                            r"(WESTERN|EASTERN|CENTRAL)\s+REGION",
                            lines[i + 1],
                            re.IGNORECASE
                        )
                        if region_match:
                            region = region_match.group(1).upper()

                    # -------------------------------
                    # CHECK NEXT LINE → DATE RANGE
                    # -------------------------------
                    if i + 2 < len(lines):
                        date_match = re.search(
                            r"from\s+(.*?)\s+to\s+(.*?)(\(|$)",
                            lines[i + 2],
                            re.IGNORECASE
                        )
                        if date_match:
                            start_date = date_match.group(1).strip()
                            end_date = date_match.group(2).strip()

                    rows.append({
                        "S.No": s_no,
                        "Product Code": product_code,
                        "Description": description,
                        "Quantity": quantity,
                        "Region": region,
                        "Start Date": start_date,
                        "End Date": end_date
                    })

                    s_no += 1
                    i += 3
                else:
                    i += 1

    df = pd.DataFrame(
        rows,
        columns=[
            "S.No",
            "Product Code",
            "Description",
            "Quantity",
            "Region",
            "Start Date",
            "End Date"
        ]
    )

    os.makedirs(os.path.dirname(excel_path), exist_ok=True)
    df.to_excel(excel_path, index=False)
