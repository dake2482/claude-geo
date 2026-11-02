#!/usr/bin/env bash
set -euo pipefail

# claude-geo → Claude Code manual installer
SRC="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="${HOME}/.claude/skills"
SKILL_DIR="${SKILL_ROOT}/geo"
AGENT_DIR="${HOME}/.claude/agents"

echo "→ Installing claude-geo into Claude Code..."
mkdir -p "${SKILL_DIR}" "${AGENT_DIR}"

for skill_dir in "${SRC}/skills"/*/; do
    name=$(basename "${skill_dir}")
    target="${SKILL_ROOT}/${name}"
    mkdir -p "${target}"
    cp -R "${skill_dir}"* "${target}/"
done
mkdir -p "${SKILL_DIR}/docs"; cp -R "${SRC}/docs/"* "${SKILL_DIR}/docs/"
cp "${SRC}/agents/"*.md "${AGENT_DIR}/"
mkdir -p "${SKILL_DIR}/scripts"
cp -R "${SRC}/scripts/"* "${SKILL_DIR}/scripts/"
rm -rf "${SKILL_DIR}/scripts/__pycache__}"
chmod +x "${SKILL_DIR}/scripts/claude-geo"
cp "${SRC}/requirements.txt" "${SKILL_DIR}/requirements.txt"
mkdir -p "${SKILL_DIR}/.claude-plugin"; cp "${SRC}/.claude-plugin/plugin.json" "${SKILL_DIR}/.claude-plugin/plugin.json"

launcher="${SKILL_DIR}/scripts/claude-geo"
rewrite() {
    local doc="$1" tmp="${1}.tmp"
    sed "s#/Users/dake/.zcode/skills/geo/scripts/claude-geo#${launcher}#g" "${doc}" > "${tmp}" \
      && sed "s#\${GEO_SKILL_ROOT}#${SKILL_DIR}#g" "${tmp}" > "${doc}" && rm -f "${tmp}"
}
while IFS= read -r -d '' doc; do rewrite "${doc}"; done < <(find "${SKILL_ROOT}/geo" "${SKILL_ROOT}/geo-audit" "${SKILL_ROOT}/geo-page" "${SKILL_ROOT}/geo-llms" "${SKILL_ROOT}/geo-report" -type f -name '*.md' -print0 2>/dev/null)
while IFS= read -r -d '' doc; do rewrite "${doc}"; done < <(find "${AGENT_DIR}" -name 'geo-*.md' -print0)

"${launcher}" setup || echo "⚠ runtime setup incomplete; retry: ${launcher} setup"
echo "✓ done. claude → /geo audit <url>"
