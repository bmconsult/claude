#!/bin/bash
# .claude/scripts/compare_versions.sh
# Archivist utility: Compare CLAUDE.md and RAPID.md versions across branches
# Usage: ./compare_versions.sh [--detailed]

set -e

DETAILED=false
if [ "$1" == "--detailed" ]; then
    DETAILED=true
fi

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║           CLAUDE.md & RAPID.md Branch Comparison               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Fetch latest
git fetch --all --quiet 2>/dev/null || true

# Get main versions
MAIN_CLAUDE_VER=$(git show origin/main:claude/CLAUDE.md 2>/dev/null | grep -E "^\| v5\.[0-9]+" | head -1 | awk '{print $2}')
MAIN_CLAUDE_LINES=$(git show origin/main:claude/CLAUDE.md 2>/dev/null | wc -l)
MAIN_RAPID_VER=$(git show origin/main:claude/RAPID.md 2>/dev/null | grep -E "^\| v7\.[0-9]+" | head -1 | awk '{print $2}')
MAIN_RAPID_LINES=$(git show origin/main:claude/RAPID.md 2>/dev/null | wc -l)

echo "📌 MAIN BRANCH (baseline):"
echo "   CLAUDE.md: ${MAIN_CLAUDE_VER:-unknown} (${MAIN_CLAUDE_LINES} lines)"
echo "   RAPID.md:  ${MAIN_RAPID_VER:-unknown} (${MAIN_RAPID_LINES} lines)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check all claude/* branches
echo "🔍 Scanning claude/* branches..."
echo ""

BRANCHES_WITH_CHANGES=""

for branch in $(git branch -r 2>/dev/null | grep "origin/claude/" | grep -v HEAD | sed 's/^[[:space:]]*//'); do
    BRANCH_NAME=$(echo "$branch" | sed 's|origin/||')

    # Get CLAUDE.md info
    CLAUDE_VER=$(git show "$branch:claude/CLAUDE.md" 2>/dev/null | grep -E "^\| v5\.[0-9]+" | head -1 | awk '{print $2}')
    CLAUDE_LINES=$(git show "$branch:claude/CLAUDE.md" 2>/dev/null | wc -l)

    # Get RAPID.md info
    RAPID_VER=$(git show "$branch:claude/RAPID.md" 2>/dev/null | grep -E "^\| v7\.[0-9]+" | head -1 | awk '{print $2}')
    RAPID_LINES=$(git show "$branch:claude/RAPID.md" 2>/dev/null | wc -l)

    # Check for differences
    CLAUDE_DIFF=false
    RAPID_DIFF=false

    if [ "$CLAUDE_VER" != "$MAIN_CLAUDE_VER" ] || [ "$CLAUDE_LINES" != "$MAIN_CLAUDE_LINES" ]; then
        CLAUDE_DIFF=true
    fi

    if [ "$RAPID_VER" != "$MAIN_RAPID_VER" ] || [ "$RAPID_LINES" != "$MAIN_RAPID_LINES" ]; then
        RAPID_DIFF=true
    fi

    # Only show branches with differences
    if [ "$CLAUDE_DIFF" = true ] || [ "$RAPID_DIFF" = true ]; then
        echo "📁 $BRANCH_NAME"

        if [ "$CLAUDE_DIFF" = true ]; then
            LINE_DELTA=$((CLAUDE_LINES - MAIN_CLAUDE_LINES))
            if [ $LINE_DELTA -gt 0 ]; then
                echo "   ⚠️  CLAUDE.md: ${CLAUDE_VER:-unknown} (${CLAUDE_LINES} lines, +${LINE_DELTA})"
            else
                echo "   📉 CLAUDE.md: ${CLAUDE_VER:-unknown} (${CLAUDE_LINES} lines, ${LINE_DELTA})"
            fi
        fi

        if [ "$RAPID_DIFF" = true ]; then
            LINE_DELTA=$((RAPID_LINES - MAIN_RAPID_LINES))
            if [ $LINE_DELTA -gt 0 ]; then
                echo "   ⚠️  RAPID.md:  ${RAPID_VER:-unknown} (${RAPID_LINES} lines, +${LINE_DELTA})"
            else
                echo "   📉 RAPID.md:  ${RAPID_VER:-unknown} (${RAPID_LINES} lines, ${LINE_DELTA})"
            fi
        fi

        if [ "$DETAILED" = true ]; then
            echo "   ─────────────────────────────────────"
            echo "   Unique sections in CLAUDE.md:"
            git diff origin/main:"claude/CLAUDE.md" "$branch:claude/CLAUDE.md" 2>/dev/null | grep "^+##" | head -5 || echo "   (none found)"
            echo ""
        fi

        BRANCHES_WITH_CHANGES="${BRANCHES_WITH_CHANGES}${BRANCH_NAME}\n"
        echo ""
    fi
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ -z "$BRANCHES_WITH_CHANGES" ]; then
    echo "✅ All branches are in sync with main."
else
    echo "📋 SUMMARY: Branches with differences:"
    echo -e "$BRANCHES_WITH_CHANGES" | grep -v "^$" | while read b; do
        echo "   - $b"
    done
    echo ""
    echo "💡 TIP: Run with --detailed for section-level diffs"
    echo "💡 TIP: Use 'git diff origin/main:claude/CLAUDE.md origin/<branch>:claude/CLAUDE.md' for full diff"
fi

echo ""
echo "Done. $(date)"
