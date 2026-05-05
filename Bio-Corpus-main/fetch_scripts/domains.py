"""
Biomedical domain definitions: keywords + MeSH-style query terms.
Used both for QUERYING the sources and for CLASSIFYING fetched articles.
"""

DOMAINS = {
    "genetique": {
        "label": "Génétique",
        "query": '("genetics"[MeSH Terms] OR "gene expression" OR "genome" OR "DNA" OR "genetic variation")',
        "ss_query": "genetics genome DNA gene expression",
        "keywords": [
            "gene", "genome", "genetic", "dna", "rna", "chromosome", "allele",
            "mutation", "genotype", "phenotype", "crispr", "sequencing",
            "transcriptome", "epigenetic", "heredity", "genomics",
        ],
    },
    "neurosciences": {
        "label": "Neurosciences",
        "query": '("neurosciences"[MeSH Terms] OR "brain" OR "neuron" OR "neural" OR "neurological")',
        "ss_query": "neuroscience brain neuron neural",
        "keywords": [
            "brain", "neuron", "neural", "neuro", "cortex", "synapse", "neurology",
            "alzheimer", "parkinson", "cognitive", "neurodegenerative", "axon",
            "dendrite", "neurotransmitter", "cerebral", "hippocampus",
        ],
    },
    "immunologie": {
        "label": "Immunologie",
        "query": '("immunology"[MeSH Terms] OR "immune" OR "antibody" OR "antigen" OR "vaccine")',
        "ss_query": "immunology immune antibody vaccine",
        "keywords": [
            "immune", "immunity", "antibody", "antigen", "vaccine", "vaccination",
            "lymphocyte", "t cell", "b cell", "cytokine", "inflammation",
            "autoimmune", "immunoglobulin", "macrophage", "innate",
        ],
    },
    "oncologie": {
        "label": "Oncologie",
        "query": '("neoplasms"[MeSH Terms] OR "cancer" OR "tumor" OR "oncology" OR "carcinoma")',
        "ss_query": "cancer oncology tumor carcinoma",
        "keywords": [
            "cancer", "tumor", "tumour", "oncology", "carcinoma", "metastasis",
            "chemotherapy", "leukemia", "lymphoma", "melanoma", "sarcoma",
            "neoplasm", "malignant", "biopsy", "radiotherapy",
        ],
    },
    "cardiologie": {
        "label": "Cardiologie",
        "query": '("cardiology"[MeSH Terms] OR "heart" OR "cardiac" OR "cardiovascular")',
        "ss_query": "cardiology heart cardiovascular",
        "keywords": [
            "heart", "cardiac", "cardiovascular", "cardiology", "myocardial",
            "infarction", "atherosclerosis", "arrhythmia", "hypertension",
            "ischemia", "coronary", "valvular", "stroke", "vascular",
        ],
    },
    "microbiologie": {
        "label": "Microbiologie",
        "query": '("microbiology"[MeSH Terms] OR "bacteria" OR "virus" OR "pathogen" OR "microbiome")',
        "ss_query": "microbiology bacteria virus microbiome",
        "keywords": [
            "bacteria", "bacterial", "virus", "viral", "pathogen", "microbiome",
            "microbial", "antibiotic", "infection", "fungal", "parasite",
            "microorganism", "antimicrobial", "biofilm",
        ],
    },
    "pharmacologie": {
        "label": "Pharmacologie",
        "query": '("pharmacology"[MeSH Terms] OR "drug" OR "pharmaceutical" OR "pharmacokinetics")',
        "ss_query": "pharmacology drug pharmacokinetics",
        "keywords": [
            "drug", "pharmaceutical", "pharmacology", "pharmacokinetic",
            "dosage", "therapeutic", "compound", "inhibitor", "agonist",
            "antagonist", "clinical trial", "efficacy", "toxicity",
        ],
    },
    "psychiatrie": {
        "label": "Psychiatrie",
        "query": '("psychiatry"[MeSH Terms] OR "depression" OR "schizophrenia" OR "anxiety" OR "mental disorder")',
        "ss_query": "psychiatry depression mental health",
        "keywords": [
            "psychiatry", "psychiatric", "depression", "anxiety", "schizophrenia",
            "bipolar", "mental health", "psychosis", "ptsd", "addiction",
            "psychological", "mood disorder", "antidepressant",
        ],
    },
}


def all_domain_keys():
    return list(DOMAINS.keys())
