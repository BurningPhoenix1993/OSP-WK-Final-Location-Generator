# OSP-WK-Final-Location-Generator
A simple yet powerful Streamlit app that helps supply chain or planning teams generate OSP (Outbound Shipment Point) Final Locations dynamically across weeks using logic based on realignment, exceptions, and default location fallback.

What this app does
Accepts an Excel file with columns like SKU, Ship to, IPAG, SCH, and week-based realignment columns like OSP Realignment WK1, WK2, etc.
For each week:
Uses the value from the corresponding OSP Realignment WKx column.
If missing, falls back to OSP Excep, OSP Def, or finally the base Location.
For weeks beyond 1, if missing, it reuses the value from the previous week.
Displays the final OSP plan.
Allows export of the result as a formatted Excel file.

**Algorithm Logic (Pseudocode)**
for each realignment week column:
    if it's WK1:
        use value from OSP Realignment WK1
        if empty → use OSP Excep
        if still empty → use OSP Def
        if still empty → use Location
    else:
        use value from OSP Realignment WKx
        if empty → use previous week's final location

**How to run Locally :** 
pip install streamlit pandas openpyxl xlsxwriter
streamlit run osp_final_location_generator.py
