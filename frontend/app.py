import streamlit as st
import requests
import pandas as pd
import io
from Bio import SeqIO

st.set_page_config(page_title="BioFlowMaster", layout="wide")
st.title("🧬 BioFlowMaster – Guided Bioinformatics Workflows")
st.markdown("This is your bioinformatics assistant. Choose a workflow below:")

# ---------------- Example Workflow ---------------- #
with st.expander("📊 Example RNA-Seq Workflow", expanded=True):
    steps = [
        "Step 1: Upload FASTQ files",
        "Step 2: Run quality check (FastQC)",
        "Step 3: Trim reads (Trimmomatic)",
        "Step 4: Align to genome (STAR)",
        "Step 5: Quantify and analyze (DESeq2)"
    ]
    for step in steps:
        st.markdown(f"• {step}")

# ---------------- CRISPR gRNA Design Tool ---------------- #
st.markdown("---")
st.subheader("🧬 CRISPR gRNA Design Tool")

col1, col2 = st.columns(2)
with col1:
    gene_input = st.text_input("Gene symbol (e.g., TP53, NANOG)")
with col2:
    sequence_input = st.text_area("Or paste your DNA sequence (≥ 23 bp):", height=150)

# Optional FASTA upload
uploaded_fasta = st.file_uploader("Or upload a FASTA file (.fa, .fasta)", type=["fasta", "fa"])
if uploaded_fasta:
    fasta_text = uploaded_fasta.read().decode("utf-8")
    record = next(SeqIO.parse(io.StringIO(fasta_text), "fasta"))
    sequence_input = str(record.seq)
    st.info(f"Loaded sequence from FASTA: {record.id}")

if st.button("Design gRNAs"):
    if not gene_input and len(sequence_input.strip()) < 23:
        st.error("⚠️ Please provide a gene symbol or a sequence with at least 23 base pairs.")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/workflow/crispr",
                json={"gene": gene_input, "sequence": sequence_input}
            )
            result = response.json()

            if "error" in result:
                st.error(f"❌ {result['error']}")
            elif result.get("guides"):
                guides = result["guides"]
                sequence_used = result.get("sequence", "")
                st.success(f"✅ Found {len(guides)} gRNAs from source: {result.get('source', 'N/A')}")

                for g in guides:
                    st.markdown(
                        f"🔹 `{g['gRNA']}` ({g['PAM']}) at position `{g['position']}` – "
                        f"**Score:** {g['score']}"
                    )

                # Download button
                df = pd.DataFrame(guides)
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="📥 Download gRNAs as CSV",
                    data=csv_buffer.getvalue().encode('utf-8'),
                    file_name="gRNA_candidates.csv",
                    mime="text/csv"
                )

                # Visual map
                st.markdown("### 🧬 gRNA Position Map")
                highlighted = list(sequence_used)
                for g in guides:
                    start = g["position"]
                    end = start + 20
                    for i in range(start, end):
                        if i < len(highlighted):
                            highlighted[i] = f"<span style='background-color:#FFDD57;color:black'>{highlighted[i]}</span>"
                    pam_end = end + 3
                    for i in range(end, pam_end):
                        if i < len(highlighted):
                            highlighted[i] = f"<span style='background-color:#FF5733;color:white'>{highlighted[i]}</span>"

                highlighted_seq = ''.join(highlighted)
                st.markdown(
                    f"<div style='font-family: monospace; word-wrap: break-word'>{highlighted_seq}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.warning("⚠️ No suitable gRNAs found.")
        except Exception as e:
            st.error("❌ Failed to contact backend or Ensembl API.")
            st.exception(e)

# ---------------- Footer ---------------- #
st.markdown("---")
st.caption("BioFlowMaster © 2025 – Built by Henry Mwaka")
