#!/usr/bin/env bash
set -euo pipefail

# claude-geo → ZCode installer(模式照搬 claude-seo/install-zcode.sh)
SRC="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="${HOME}/.zcode/skills"
SKILL_DIR="${SKILL_ROOT}/geo"
AGENT_DIR="${HOME}/.zcode/agents"

echo "→ Installing claude-geo into ZCode..."
mkdir -p "${SKILL_DIR}" "${AGENT_DIR}"

# 技能(全部)
for skill_dir in "${SRC}/skills"/*/; do
    name=$(basename "${skill_dir}")
    target="${SKILL_ROOT}/${name}"
    mkdir -p "${target}"
    cp -R "${skill_dir}"* "${target}/"
done

# 共享 docs 进主技能目录
mkdir -p "${SKILL_DIR}/docs"
cp -R "${SRC}/docs/"* "${SKILL_DIR}/docs/"

# 代理
cp "${SRC}/agents/"*.md "${AGENT_DIR}/"

# runtime(仓库级 scripts/ 复制进主技能目录,与 claude-seo 布局一致)
mkdir -p "${SKILL_DIR}/scripts"
cp -R "${SRC}/scripts/"* "${SKILL_DIR}/scripts/"
rm -rf "${SKILL_DIR}/scripts/__pycache__"
chmod +x "${SKILL_DIR}/scripts/claude-geo"
cp "${SRC}/requirements.txt" "${SKILL_DIR}/requirements.txt" 2>/dev/null || true
mkdir -p "${SKILL_DIR}/.claude-plugin"
cp "${SRC}/.claude-plugin/plugin.json" "${SKILL_DIR}/.claude-plugin/plugin.json"

# 路径重写:${SKILL_PLACEHOLDER}/skills/geo/scripts/claude-geo → 绝对路径
launcher="${SKILL_DIR}/scripts/claude-geo"
rewrite() {
    local doc="$1" tmp="${1}.tmp"
    sed "s#/Users/dake/.zcode/skills/geo/scripts/claude-geo#${launcher}#g" "${doc}" > "${tmp}" \
      && sed "s#\${GEO_SKILL_ROOT}#${SKILL_DIR}#g" "${tmp}" > "${doc}" && rm -f "${tmp}"
}
while IFS= read -r -d '' doc; do rewrite "${doc}"; done < <(find "${SKILL_ROOT}/geo" "${SKILL_ROOT}/geo-audit" "${SKILL_ROOT}/geo-page" "${SKILL_ROOT}/geo-llms" "${SKILL_ROOT}/geo-report" -type f -name '*.md' -print0 2>/dev/null)
while IFS= read -r -d '' doc; do rewrite "${doc}"; done < <(find "${AGENT_DIR}" -name 'geo-*.md' -print0)

# runtime setup
echo "→ Creating isolated Python runtime..."
set +e
"${launcher}" setup
status=$?
set -e
[ "${status}" -ne 0 ] && echo "⚠ runtime setup failed(可稍后跑 ${launcher} setup)" || true

echo ""
echo "✓ claude-geo installed for ZCode."
echo "  Skills:  ${SKILL_ROOT}/geo* ($(ls "${SKILL_ROOT}" | grep -c '^geo'))"
echo "  Agents:  ${AGENT_DIR} ($(ls "${AGENT_DIR}" | grep -c '^geo-'))"
echo "  新开会话 → /geo audit https://example.com"
