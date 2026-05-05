"""
Commande Django pour remplir MongoDB avec des articles d'exemple.
python manage.py populate_articles
"""
from django.core.management.base import BaseCommand
from articles.models import Article
import random

SAMPLE_DATA = [
    {
        "title": "Deep Learning Applications in Medical Image Analysis",
        "abstract": "This comprehensive review examines the latest deep learning techniques applied to medical imaging, including CT, MRI, and X-ray analysis.",
        "journal": "Nature Medicine",
        "year": "2024",
        "authors": ["John Smith", "Sarah Johnson", "Michael Chen"],
        "mesh_terms": ["Deep Learning", "Medical Imaging", "AI", "Computer Vision"],
        "keywords": ["neural networks", "image classification", "diagnosis"],
        "source": "pubmed",
        "domain": "Medical Imaging",
        "domain_confidence": 0.95,
        "pmid": "12345001",
        "url": "https://example.com/article1"
    },
    {
        "title": "CRISPR Gene Editing: Recent Advances and Clinical Applications",
        "abstract": "A review of CRISPR-Cas9 technology and its emerging therapeutic applications in genetic disorders.",
        "journal": "Cell Research",
        "year": "2024",
        "authors": ["Lisa Wang", "James Wilson"],
        "mesh_terms": ["CRISPR", "Gene Therapy", "Genetic Engineering"],
        "keywords": ["genome editing", "molecular therapy"],
        "source": "pubmed",
        "domain": "Genetic Engineering",
        "domain_confidence": 0.92,
        "pmid": "12345002",
        "url": "https://example.com/article2"
    },
    {
        "title": "Neuroplasticity in Adult Brain: Mechanisms and Therapeutic Implications",
        "abstract": "Exploring the mechanisms of neuroplasticity and its potential for treating neurodegenerative diseases.",
        "journal": "Brain",
        "year": "2023",
        "authors": ["David Martinez", "Emily Davis"],
        "mesh_terms": ["Neuroplasticity", "Neuroscience", "Brain Repair"],
        "keywords": ["synaptic plasticity", "neurogenesis"],
        "source": "pmc",
        "domain": "Neuroscience",
        "domain_confidence": 0.88,
        "pmcid": "PMC9876543",
        "url": "https://example.com/article3"
    },
    {
        "title": "Immunotherapy Revolution: CAR-T Cell Therapy Advances",
        "abstract": "Review of CAR-T cell engineering approaches and their applications in hematologic malignancies.",
        "journal": "Cancer Immunology Research",
        "year": "2024",
        "authors": ["Robert Brown", "Jennifer Lee"],
        "mesh_terms": ["Immunotherapy", "CAR-T", "Cancer Biology"],
        "keywords": ["engineered cells", "lymphocytes"],
        "source": "pubmed",
        "domain": "Oncology",
        "domain_confidence": 0.93,
        "pmid": "12345003",
        "doi": "10.1234/cancer.2024.001",
        "url": "https://example.com/article4"
    },
    {
        "title": "Microbiome Research and Human Health: Recent Discoveries",
        "abstract": "Comprehensive review of the human microbiome and its role in health and disease.",
        "journal": "Microbiome Journal",
        "year": "2024",
        "authors": ["Susan Garcia", "Paul White"],
        "mesh_terms": ["Microbiome", "Bacterial Taxonomy", "Dysbiosis"],
        "keywords": ["gut bacteria", "microbial diversity"],
        "source": "semantic_scholar",
        "domain": "Microbiology",
        "domain_confidence": 0.89,
        "ss_id": "12345abc",
        "url": "https://example.com/article5"
    },
    {
        "title": "Machine Learning in Drug Discovery and Development",
        "abstract": "Exploring ML algorithms for accelerating drug discovery processes.",
        "journal": "Nature Reviews Drug Discovery",
        "year": "2024",
        "authors": ["Alex Kumar", "Maria Santos"],
        "mesh_terms": ["Machine Learning", "Drug Discovery", "Pharma"],
        "keywords": ["compound screening", "molecular prediction"],
        "source": "pubmed",
        "domain": "Pharmaceutical",
        "domain_confidence": 0.91,
        "pmid": "12345004",
        "url": "https://example.com/article6"
    },
    {
        "title": "Biomarkers for Early Cancer Detection: State of the Art",
        "abstract": "Current biomarkers and emerging methods for early detection of various cancers.",
        "journal": "Cancer Letters",
        "year": "2023",
        "authors": ["Thomas Anderson", "Victoria Lopez"],
        "mesh_terms": ["Biomarkers", "Cancer", "Diagnostic"],
        "keywords": ["tumor markers", "early detection"],
        "source": "pmc",
        "domain": "Oncology",
        "domain_confidence": 0.94,
        "pmcid": "PMC9876544",
        "url": "https://example.com/article7"
    },
    {
        "title": "Cardiovascular Health: Role of Inflammation and Novel Therapeutics",
        "abstract": "Review of inflammatory pathways in cardiovascular disease and emerging treatments.",
        "journal": "Circulation",
        "year": "2024",
        "authors": ["Christopher Hall", "Nicole Taylor"],
        "mesh_terms": ["Cardiovascular", "Inflammation", "Heart Disease"],
        "keywords": ["atherosclerosis", "vascular disease"],
        "source": "pubmed",
        "domain": "Cardiology",
        "domain_confidence": 0.90,
        "pmid": "12345005",
        "url": "https://example.com/article8"
    },
    {
        "title": "Precision Medicine: Genomics and Personalized Treatment",
        "abstract": "How genomic information enables tailored medical treatments.",
        "journal": "The Lancet",
        "year": "2024",
        "authors": ["Rachel Green", "Kevin Moore"],
        "mesh_terms": ["Precision Medicine", "Genomics", "Personalized"],
        "keywords": ["genotyping", "pharmacogenomics"],
        "source": "semantic_scholar",
        "domain": "Genomics",
        "domain_confidence": 0.92,
        "ss_id": "12345def",
        "url": "https://example.com/article9"
    },
    {
        "title": "Neuroinflammation in Alzheimer's Disease: Mechanisms and Targets",
        "abstract": "Exploring neuroinflammatory pathways as targets for Alzheimer's therapeutics.",
        "journal": "Neurobiology of Aging",
        "year": "2023",
        "authors": ["Patricia Walker", "George Lewis"],
        "mesh_terms": ["Neuroinflammation", "Alzheimer's", "Neurodegenerative"],
        "keywords": ["amyloid", "tau pathology"],
        "source": "pubmed",
        "domain": "Neuroscience",
        "domain_confidence": 0.87,
        "pmid": "12345006",
        "url": "https://example.com/article10"
    },
    {
        "title": "RNA Therapeutics: From Bench to Bedside",
        "abstract": "Overview of RNA-based therapeutic approaches and clinical trials.",
        "journal": "Nature Biotechnology",
        "year": "2024",
        "authors": ["Mark Young", "Angela Harris"],
        "mesh_terms": ["RNA", "Therapeutics", "Molecular"],
        "keywords": ["antisense", "siRNA", "mRNA"],
        "source": "pmc",
        "domain": "Molecular Medicine",
        "domain_confidence": 0.93,
        "pmcid": "PMC9876545",
        "url": "https://example.com/article11"
    },
]

class Command(BaseCommand):
    help = "Populate MongoDB with sample biomedical articles"

    def handle(self, *args, **options):
        # Clear existing articles
        Article.objects.delete()
        self.stdout.write(self.style.SUCCESS("✓ Cleared existing articles"))

        # Insert sample articles multiple times to create 50+ articles
        articles = []
        for i in range(5):
            for data in SAMPLE_DATA:
                article_data = data.copy()
                # Make each article unique
                article_data["title"] = f"{data['title']} (Variant {i+1})"
                article_data["pmid"] = str(int(data.get("pmid", "12345000")) + i) if data.get("pmid") else ""
                article_data["pmcid"] = f"PMC{int(data.get('pmcid', '9876543').replace('PMC', '')) + i}" if data.get("pmcid") else ""
                articles.append(Article(**article_data))

        Article.objects.insert(articles)
        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(articles)} sample articles"))
