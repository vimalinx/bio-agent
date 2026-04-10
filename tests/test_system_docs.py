from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_console_page_exists_and_references_demo_bundle() -> None:
    console_page = ROOT / "docs" / "system" / "bio-skill-console.html"
    html = console_page.read_text(encoding="utf-8")

    assert "Bio Skill System Control Console" in html
    assert 'const DEMO_BUNDLE_URL = "data/bio-skill-console-demo.json"' in html
    assert '?bundle=' in html
    assert "Bundle Source" in html
    assert "Upload JSON" in html
    assert "What can I help you model today?" in html
    assert "Session Timeline" in html
    assert "Candidate Plans" in html
    assert "Operator Actions" in html
    assert "Plan Editor" in html
    assert "Analysis Flow" in html
    assert "Workflow Families" in html
    assert "Strategy" in html
    assert "Use Family" in html
    assert "Use Strategy" in html
    assert "Rebuild Plans" in html
    assert "Approve Edited" in html
    assert 'id="new-session-button"' in html
    assert "Start Session" in html
    assert "family-select" in html or "data-family-strategy" in html
    assert "Filter sessions..." in html
    assert "Needs Plan" in html
    assert "In Run" in html
    assert "Archived" in html
    assert "Flat" in html
    assert "Grouped" in html
    assert "Pin Visible" in html
    assert "Archive Visible" in html
    assert "Clear Visible Notes" in html
    assert "Saved view name..." in html
    assert "Save View" in html
    assert "session-group-title" in html or "data-group-label" in html
    assert "Pin session" in html or "data-pin-session" in html
    assert "Hide session" in html or "data-archive-session" in html
    assert "Session Notes" in html
    assert "Label for active session..." in html
    assert "Short note for the active session..." in html
    assert "Delivery Bundle" in html
    assert "Metadata Inputs" in html
    assert 'id="analysis-flow-panel"' in html
    assert 'id="delivery-list"' in html
    assert "session-export-console" in html
    assert "session-serve-console" in html or "/api/session/action" in html
    assert "/api/sessions" in html
    assert "/api/session/start" in html
    assert "/api/session/plan-markdown" in html


def test_console_demo_bundle_contains_expected_runtime_shape() -> None:
    demo_path = ROOT / "docs" / "system" / "data" / "bio-skill-console-demo.json"
    payload = json.loads(demo_path.read_text(encoding="utf-8"))

    assert payload["review"]["recommended_plan_id"].endswith("_conservative")
    assert payload["run_status"]["status"] == "paused"
    assert payload["run_status"]["current_stage"] == "s2"
    assert payload["run_status"]["next_action"] == "Confirm and resume stage s2."
    assert payload["run_review"]["verdict"] == "awaiting_confirmation"
    assert any(item["type"] == "future_unresolved_skills" for item in payload["run_review"]["future_issues"])
    assert "pydeseq2" in payload["execution_draft"]["unresolved_skill_ids"]
    assert payload["analysis_flow"]["workflow_id"] == "rnaseq-differential-expression"
    assert payload["analysis_flow"]["stage_flows"][0]["stage_id"] == "s1"
    assert payload["session"]["status"] == "awaiting_confirmation"
    assert payload["session"]["latest_approval_reason"]
    assert payload["history"]["events"][-1]["type"] == "run_advanced"


def test_architecture_page_links_to_console() -> None:
    architecture_page = ROOT / "docs" / "system" / "bio-skill-system.html"
    html = architecture_page.read_text(encoding="utf-8")

    assert "bio-skill-console.html" in html


def test_real_workflow_map_page_and_catalog_exist() -> None:
    workflow_page = ROOT / "docs" / "system" / "real-bioinformatics-workflow-map.html"
    catalog_path = ROOT / "docs" / "system" / "data" / "real-bioinformatics-workflows.json"

    html = workflow_page.read_text(encoding="utf-8")
    payload = json.loads(catalog_path.read_text(encoding="utf-8"))

    assert "Real Bioinformatics Workflow Map" in html
    assert "nf-core/rnaseq" in html
    assert "nf-core/scrnaseq" in html
    assert "nf-core/atacseq" in html
    assert "GATK Germline short variant discovery" in html
    assert "training.galaxyproject.org" in html
    workflow_ids = {item["id"] for item in payload["workflows"]}
    assert {"rnaseq-differential-expression", "scrnaseq-preprocessing", "atacseq-differential-accessibility", "germline-short-variant-discovery"}.issubset(workflow_ids)


def test_real_analysis_flow_page_and_catalog_exist() -> None:
    flow_page = ROOT / "docs" / "system" / "real-analysis-information-flows.html"
    flow_catalog_path = ROOT / "docs" / "system" / "data" / "real-analysis-information-flows.json"
    registry_path = ROOT / "registry" / "analysis_flows.yaml"

    html = flow_page.read_text(encoding="utf-8")
    payload = json.loads(flow_catalog_path.read_text(encoding="utf-8"))
    registry_text = registry_path.read_text(encoding="utf-8")

    assert "Real Analysis Information Flows" in html
    assert "Bulk RNA-seq differential expression" in html
    assert "Single-cell RNA-seq preprocessing" in html
    assert "ATAC-seq differential accessibility" in html
    assert "Germline SNP/Indel discovery for WGS/WES" in html
    flow_ids = {item["workflow_id"] for item in payload["flows"]}
    assert {"rnaseq-differential-expression", "scrnaseq-preprocessing", "atacseq-differential-accessibility", "germline-short-variant-discovery"}.issubset(flow_ids)
    assert "workflow_id: rnaseq-differential-expression" in registry_text
    assert "delivery_bundle:" in registry_text


def test_architecture_and_index_link_to_real_workflow_map_and_analysis_flows() -> None:
    architecture_page = ROOT / "docs" / "system" / "bio-skill-system.html"
    index_page = ROOT / "docs" / "index.html"
    workflow_map_page = ROOT / "docs" / "system" / "real-bioinformatics-workflow-map.html"

    architecture_html = architecture_page.read_text(encoding="utf-8")
    index_html = index_page.read_text(encoding="utf-8")
    workflow_map_html = workflow_map_page.read_text(encoding="utf-8")

    assert "real-bioinformatics-workflow-map.html" in architecture_html
    assert "real-bioinformatics-workflow-map.html" in index_html
    assert "real-analysis-information-flows.html" in architecture_html
    assert "real-analysis-information-flows.html" in index_html
    assert "real-analysis-information-flows.html" in workflow_map_html


def test_workflow_knowledge_base_files_exist() -> None:
    knowledge_md = ROOT / "docs" / "context" / "WORKFLOW_KNOWLEDGE_BASE.md"
    knowledge_yaml = ROOT / "registry" / "workflow_knowledge.yaml"
    analysis_flow_yaml = ROOT / "registry" / "analysis_flows.yaml"

    md_text = knowledge_md.read_text(encoding="utf-8")
    yaml_text = knowledge_yaml.read_text(encoding="utf-8")
    flow_text = analysis_flow_yaml.read_text(encoding="utf-8")

    assert "WORKFLOW_KNOWLEDGE_BASE" in md_text
    assert "bulk-rnaseq" in md_text
    assert "scrnaseq" in md_text
    assert "germline-short-variants" in md_text
    assert "organization_principles:" in yaml_text
    assert "family_templates:" in yaml_text
    assert "flows:" in flow_text
    assert "rnaseq-differential-expression" in flow_text
