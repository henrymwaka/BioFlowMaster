# 🧬 BioFlowMaster

**BioFlowMaster** is a modular, guided bioinformatics assistant that helps scientists perform complex molecular analyse, like CRISPR guide RNA design or RNA-Seq workflows — using a clean, step-by-step web interface powered by modern tools.

---

## 🚀 Current Features

### ✅ CRISPR gRNA Design (MVP Complete)
- Accepts either a **gene symbol** (e.g., `TP53`, `NANOG`) or a raw **DNA sequence**
- Automatically fetches coding sequences (CDS) from Ensembl API
- Detects candidate gRNAs (20-mer + NGG PAM)
- Displays matched guides, positions, and PAM sites
- Allows **CSV export** of gRNAs

### ✅ RNA-Seq Workflow (Scaffolded)
- Placeholder wizard displaying steps for:
  - FASTQ upload
  - Quality control (FastQC)
  - Trimming (Trimmomatic)
  - Alignment (STAR)
  - Expression analysis (DESeq2)

---

## 📁 Project Structure

BioFlowMaster/
├── backend/ # FastAPI backend
│ ├── main.py # CRISPR API logic and Ensembl integration
│ └── requirements.txt
├── frontend/ # Streamlit UI
│ ├── app.py # Web interface with CRISPR workflow
│ └── requirements.txt
├── workflows/ # Snakemake/Nextflow (future)
├── examples/ # Sample inputs or gene sets
├── scripts/ # Helper scripts/utilities
├── docs/ # Documentation and developer notes
├── .gitignore
├── LICENSE
└── README.md


🧠 Future Roadmap
CRISPR off-target scoring integration (e.g., CRISPOR or CHOPCHOP)

Interactive visualization of gRNA sites on sequences

Uploadable FASTA batch processing

Full RNA-Seq pipeline integration using Snakemake or Galaxy API

BrAPI or Galaxy history integration

User authentication and workflow history saving

👨‍🔬 Author
Henry Mwaka
Lab Manager, National Agricultural Research Laboratories – Uganda
GitHub: @henrymwaka

Designed to make bioinformatics feel intuitive — one workflow at a time.