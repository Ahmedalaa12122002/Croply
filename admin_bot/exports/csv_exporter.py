import csv
from io import StringIO

def export_to_csv(headers: list, rows: list) -> StringIO:
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)
    output.seek(0)
    return output
