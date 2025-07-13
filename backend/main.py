from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import random

app = FastAPI(title="BioFlowMaster API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to BioFlowMaster API!"}

@app.post("/workflow/crispr")
async def design_crispr(request: Request):
    data = await request.json()
    sequence = data.get("sequence", "").upper()
    gene_symbol = data.get("gene", "").strip()

    # If gene symbol is provided, override the sequence by fetching it
    if gene_symbol and not sequence:
        try:
            # Step 1: Get Ensembl gene ID
            gene_resp = httpx.get(f"https://rest.ensembl.org/xrefs/symbol/homo_sapiens/{gene_symbol}?content-type=application/json")
            gene_resp.raise_for_status()
            ensembl_id = gene_resp.json()[0]["id"]

            # Step 2: Get canonical transcript
            lookup = httpx.get(f"https://rest.ensembl.org/lookup/id/{ensembl_id}?expand=1")
            lookup.raise_for_status()
            transcript_id = lookup.json()["Transcript"][0]["id"]

            # Step 3: Get CDS
            seq_resp = httpx.get(f"https://rest.ensembl.org/sequence/id/{transcript_id}?type=cds")
            seq_resp.raise_for_status()
            sequence = seq_resp.json()["seq"]
        except Exception as e:
            return {"error": f"Gene lookup failed: {str(e)}"}

    if not sequence or len(sequence) < 23:
        return {"error": "Please provide a valid DNA sequence (or valid gene symbol)."}

    guides = []
    for i in range(0, len(sequence) - 23):
        pam = sequence[i + 20:i + 23]
        if pam.endswith("GG"):
            guides.append({
                "gRNA": sequence[i:i + 20],
                "PAM": pam,
                "position": i,
                "score": round(random.uniform(0.5, 1.0), 3)  # Mock off-target score
            })

    return {
        "guides": guides[:10],
        "source": gene_symbol if gene_symbol else "custom",
        "sequence": sequence
    }
