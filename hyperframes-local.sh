#!/bin/sh
set -eu

NODE="/Users/xp/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node"
TSX="/Users/Wiselaw- video/hyperframes/node_modules/.bin/tsx"
CLI="/Users/Wiselaw- video/hyperframes/packages/cli/src/cli.ts"

exec "$NODE" "$TSX" "$CLI" "$@"
