import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="OSP Final Location Generator", layout="wide")
st.title("📍 OSP WK Final Location Generator")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, dtype=str).fillna("")

        # Identify all Realignment columns dynamically
        realign_cols = [col for col in df.columns if col.startswith("OSP Realignment WK")]

        # Start with base columns
        final_df = df[["SKU", "Ship to", "IPAG", "SCH"]].copy()
        previous_column = ""

        for i, col in enumerate(realign_cols):
            week_num = i + 1
            output_col = f"OSP WK{week_num} Final Location"

            if week_num == 1:
                # WK1 logic
                final_df[output_col] = df[col]
                final_df[output_col] = final_df[output_col].mask(final_df[output_col] == "", df["OSP Excep"])
                final_df[output_col] = final_df[output_col].mask(final_df[output_col] == "", df["OSP Def"])
                final_df[output_col] = final_df[output_col].mask(final_df[output_col] == "", df["Location"])
            else:
                # WK2+ logic
                final_df[output_col] = df[col]
                final_df[output_col] = final_df[output_col].mask(final_df[output_col] == "", final_df[previous_column])

            previous_column = output_col

        st.success("✅ OSP Final Location Table Generated")

        st.dataframe(final_df)

        # Export to Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            final_df.to_excel(writer, index=False, sheet_name="OSP Final")
            worksheet = writer.sheets["OSP Final"]
            for i, col in enumerate(final_df.columns):
                max_len = max(final_df[col].astype(str).map(len).max(), len(col)) + 2
                worksheet.set_column(i, i, max_len)

        output.seek(0)

        st.download_button(
            label="📥 Download Final Excel",
            data=output,
            file_name="OSP_Final_Locations.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.info("📂 Upload an Excel file with SKU and OSP columns to begin.")
