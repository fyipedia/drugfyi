# drugfyi

[![PyPI version](https://agentgif.com/badge/pypi/drugfyi/version.svg)](https://pypi.org/project/drugfyi/)
[![Python](https://img.shields.io/pypi/pyversions/drugfyi)](https://pypi.org/project/drugfyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-0-brightgreen)](https://pypi.org/project/drugfyi/)

Python API client for drug interaction and pharmacology data. Check drug-drug interactions, look up side effect profiles, explore pharmacokinetic properties (absorption, metabolism, half-life), and query mechanism of action — all from [DrugFYI](https://drugfyi.com/), a drug reference platform built for healthcare developers and pharmacists.

DrugFYI aggregates pharmacological data including interaction severity ratings, cytochrome P450 enzyme pathways, therapeutic drug classes, contraindications, and adverse reaction frequencies — providing structured access to critical medication safety information.

> **Check drug interactions at [drugfyi.com](https://drugfyi.com/)** — search [drugs](https://drugfyi.com/drugs/), explore [interactions](https://drugfyi.com/interactions/), and browse [drug classes](https://drugfyi.com/classes/).

<p align="center">
  <img src="https://raw.githubusercontent.com/fyipedia/drugfyi/main/demo.gif" alt="drugfyi demo — drug interactions, pharmacology, and side effect lookup in Python" width="800">
</p>

## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [What You Can Do](#what-you-can-do)
  - [Drug-Drug Interactions](#drug-drug-interactions)
  - [Side Effect Profiles](#side-effect-profiles)
  - [Pharmacokinetics](#pharmacokinetics)
  - [Drug Classifications](#drug-classifications)
- [Command-Line Interface](#command-line-interface)
- [MCP Server (Claude, Cursor, Windsurf)](#mcp-server-claude-cursor-windsurf)
- [REST API Client](#rest-api-client)
- [API Reference](#api-reference)
- [Learn More About Drugs](#learn-more-about-drugs)
- [Also Available](#also-available)
- [Health FYI Family](#health-fyi-family)
- [License](#license)

## Install

```bash
pip install drugfyi                # Core (zero deps)
pip install "drugfyi[cli]"         # + Command-line interface
pip install "drugfyi[mcp]"         # + MCP server for AI assistants
pip install "drugfyi[api]"         # + HTTP client for drugfyi.com API
pip install "drugfyi[all]"         # Everything
```

## Quick Start

```python
from drugfyi.api import DrugFYI

with DrugFYI() as api:
    # Check interaction between two drugs
    interaction = api.get_interaction("warfarin", "aspirin")
    print(interaction["severity"])       # Major
    print(interaction["description"])    # Increased bleeding risk

    # Get complete drug profile
    drug = api.get_drug("metformin")
    print(drug["class"])                 # Biguanides
    print(drug["mechanism"])             # Decreases hepatic glucose production

    # Search across all drugs
    results = api.search("statin")
```

## What You Can Do

### Drug-Drug Interactions

Drug interactions occur when one medication affects the activity of another, potentially causing therapeutic failure or adverse effects. Interactions are classified by severity (major, moderate, minor) and mechanism (pharmacokinetic vs pharmacodynamic).

| Severity | Clinical Significance | Action Required |
|----------|----------------------|----------------|
| Major | Life-threatening or permanent damage | Avoid combination |
| Moderate | May require therapy modification | Monitor closely |
| Minor | Minimal clinical significance | Awareness only |
| Contraindicated | Absolutely avoid | Never co-prescribe |

```python
from drugfyi.api import DrugFYI

with DrugFYI() as api:
    # Check specific drug pair interaction
    interaction = api.get_interaction("warfarin", "ibuprofen")
    print(interaction["severity"])       # Major
    print(interaction["mechanism"])      # CYP2C9 inhibition + antiplatelet effect
    print(interaction["recommendation"])

    # Get all interactions for a drug
    interactions = api.list_interactions("warfarin")
    major = [i for i in interactions if i["severity"] == "Major"]
    print(f"Warfarin has {len(major)} major interactions")
```

Learn more: [Drug Interactions](https://drugfyi.com/interactions/) · [Glossary](https://drugfyi.com/glossary/)

### Side Effect Profiles

Every medication carries a side effect profile derived from clinical trials and post-marketing surveillance. Side effects are categorized by frequency (very common >10%, common 1-10%, uncommon 0.1-1%, rare <0.1%) and organ system affected.

```python
from drugfyi.api import DrugFYI

with DrugFYI() as api:
    # Get side effect profile
    drug = api.get_drug("metoprolol")
    for effect in drug["side_effects"]:
        print(f"{effect['name']}: {effect['frequency']}")
        # Fatigue: Very Common (>10%)
        # Dizziness: Common (1-10%)
        # Bradycardia: Common (1-10%)
```

Learn more: [Drug Side Effects](https://drugfyi.com/drugs/) · [Guides](https://drugfyi.com/guides/)

### Pharmacokinetics

Pharmacokinetics — how the body processes a drug — follows four phases: Absorption (A), Distribution (D), Metabolism (M), and Elimination (E). Understanding ADME properties is critical for dosing, timing, and predicting interactions via shared metabolic pathways.

| Parameter | Meaning | Clinical Relevance |
|-----------|---------|-------------------|
| Bioavailability | % reaching systemic circulation | Oral vs IV dosing |
| Half-life | Time for 50% elimination | Dosing frequency |
| CYP enzymes | Metabolic pathway | Interaction prediction |
| Protein binding | % bound to albumin | Drug displacement interactions |

```python
from drugfyi.api import DrugFYI

with DrugFYI() as api:
    # Pharmacokinetic properties
    drug = api.get_drug("atorvastatin")
    pk = drug["pharmacokinetics"]
    print(pk["bioavailability"])      # 14%
    print(pk["half_life"])            # 14 hours
    print(pk["metabolism"])           # CYP3A4
    print(pk["protein_binding"])      # >98%
```

Learn more: [Pharmacokinetics](https://drugfyi.com/guides/) · [Glossary](https://drugfyi.com/glossary/)

### Drug Classifications

Drugs are organized by therapeutic class (what they treat), pharmacological class (how they work), and chemical class (molecular structure). The ATC (Anatomical Therapeutic Chemical) classification system provides a standardized 5-level hierarchy.

| Level | ATC Code | Meaning | Example |
|-------|----------|---------|---------|
| 1st | C | Cardiovascular system | — |
| 2nd | C10 | Lipid modifying agents | — |
| 3rd | C10A | Cholesterol/triglyceride reducers | — |
| 4th | C10AA | HMG-CoA reductase inhibitors | Statins |
| 5th | C10AA05 | Specific chemical | Atorvastatin |

```python
from drugfyi.api import DrugFYI

with DrugFYI() as api:
    # Browse drug classes
    classes = api.list_classes()
    for cls in classes[:5]:
        print(f"{cls['name']}: {cls['drug_count']} drugs")

    # Get all drugs in a class
    statins = api.get_class("statins")
    for drug in statins["drugs"]:
        print(drug["name"])
```

Learn more: [Drug Classes](https://drugfyi.com/classes/) · [API Documentation](https://drugfyi.com/developers/)

## Command-Line Interface

```bash
pip install "drugfyi[cli]"

drugfyi drug metformin                          # Drug details
drugfyi interaction warfarin aspirin             # Check interaction
drugfyi interactions warfarin                    # All interactions for a drug
drugfyi search "ACE inhibitor"                   # Search drugs
drugfyi classes                                  # List drug classes
```

## MCP Server (Claude, Cursor, Windsurf)

```bash
pip install "drugfyi[mcp]"
```

```json
{
    "mcpServers": {
        "drugfyi": {
            "command": "uvx",
            "args": ["--from", "drugfyi[mcp]", "python", "-m", "drugfyi.mcp_server"]
        }
    }
}
```

## REST API Client

```python
from drugfyi.api import DrugFYI

with DrugFYI() as api:
    drug = api.get_drug("metformin")                    # GET /api/v1/drugs/metformin/
    interaction = api.get_interaction("warfarin", "aspirin")  # GET /api/v1/interactions/warfarin/aspirin/
    classes = api.list_classes()                         # GET /api/v1/classes/
    results = api.search("beta blocker")                # GET /api/v1/search/?q=beta+blocker
```

### Example

```bash
curl -s "https://drugfyi.com/api/v1/drugs/metformin/"
```

```json
{
    "slug": "metformin",
    "generic_name": "Metformin",
    "class": "Biguanides",
    "mechanism": "Decreases hepatic glucose production",
    "route": "Oral"
}
```

Full API documentation at [drugfyi.com/developers/](https://drugfyi.com/developers/).

## API Reference

| Function | Description |
|----------|-------------|
| `api.get_drug(slug)` | Complete drug profile |
| `api.list_drugs()` | List all drugs |
| `api.get_interaction(drug1, drug2)` | Check specific interaction |
| `api.list_interactions(drug)` | All interactions for a drug |
| `api.list_classes()` | All therapeutic drug classes |
| `api.get_class(slug)` | Drug class details with member drugs |
| `api.search(query)` | Search across drugs and classes |

## Learn More About Drugs

- **Browse**: [Drug Database](https://drugfyi.com/drugs/) · [Interactions](https://drugfyi.com/interactions/) · [Drug Classes](https://drugfyi.com/classes/)
- **Guides**: [Pharmacology Guides](https://drugfyi.com/guides/) · [Glossary](https://drugfyi.com/glossary/)
- **API**: [REST API Docs](https://drugfyi.com/developers/) · [OpenAPI Spec](https://drugfyi.com/api/openapi.json)

## Also Available

| Platform | Install | Link |
|----------|---------|------|
| **npm** | `npm install drugfyi` | [npm](https://www.npmjs.com/package/drugfyi) |
| **MCP** | `uvx --from "drugfyi[mcp]" python -m drugfyi.mcp_server` | [Config](#mcp-server-claude-cursor-windsurf) |

## Health FYI Family

Part of the [FYIPedia](https://fyipedia.com) open-source developer tools ecosystem — human body, medicine, and nutrition.

| Package | PyPI | npm | Description |
|---------|------|-----|-------------|
| anatomyfyi | [PyPI](https://pypi.org/project/anatomyfyi/) | [npm](https://www.npmjs.com/package/anatomyfyi) | 14,692 anatomical structures, body systems, organs — [anatomyfyi.com](https://anatomyfyi.com/) |
| pillfyi | [PyPI](https://pypi.org/project/pillfyi/) | [npm](https://www.npmjs.com/package/pillfyi) | Pill identification, FDA drug database — [pillfyi.com](https://pillfyi.com/) |
| **drugfyi** | [PyPI](https://pypi.org/project/drugfyi/) | [npm](https://www.npmjs.com/package/drugfyi) | **Drug interactions, pharmacology, side effects — [drugfyi.com](https://drugfyi.com/)** |
| nutrifyi | [PyPI](https://pypi.org/project/nutrifyi/) | [npm](https://www.npmjs.com/package/nutrifyi) | Nutrition data, food composition, dietary analysis — [nutrifyi.com](https://nutrifyi.com/) |

## License

MIT
