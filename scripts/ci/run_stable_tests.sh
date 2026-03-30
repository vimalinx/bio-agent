#!/usr/bin/env bash
set -euo pipefail

python -m pytest \
  tests/test_project_template_validation.py \
  tests/test_workspace_project_cli.py \
  tests/test_workspace_validation_project.py \
  tests/test_project_type_templates.py \
  tests/test_example_project_sync.py \
  tests/test_project_template_module_integration.py \
  tests/test_demo_project_shared_runtime.py \
  tests/test_ai_design_playground_shared_runtime.py \
  tests/test_demo_project_validation_entrypoints.py \
  tests/test_workspace_runtime_consistency.py \
  tests/test_workspace_validation_mock_data.py \
  tests/test_special_project_minimal_integration.py \
  tests/test_project_validation_helpers.py \
  tests/test_design_mcp_server.py \
  tests/test_lab_mcp_server.py \
  tests/test_mcp_config_render.py \
  tests/test_mcp_server_entrypoints.py \
  tests/test_mcp_readme_paths.py \
  tests/test_database_mcp_server_config.py \
  tests/test_design_tool_script_compat.py \
  tests/test_litefold_bridge.py \
  tests/test_github_actions_ci.py \
  -q
