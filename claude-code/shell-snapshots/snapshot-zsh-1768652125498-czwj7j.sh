# Snapshot file
# Unset all aliases to avoid conflicts with functions
unalias -a 2>/dev/null || true
# Functions
# Shell Options
# Aliases
# Check for rg availability
if ! command -v rg >/dev/null 2>&1; then
  alias rg='/Users/yahelraviv/.local/share/claude/versions/2.1.11 --ripgrep'
fi
export PATH=/Users/yahelraviv/.local/bin\:/Users/yahelraviv/.local/bin\:~/.local/bin/claude
