#!/usr/bin/env bash
set -euo pipefail

if [ ! -f .env.deploy ]; then
  echo "Missing .env.deploy"
  exit 1
fi

set -a
source ./.env.deploy
set +a

echo "[1/6] push branch"
git push origin "$BRANCH"

echo "[2/6] sync repo on server (force clean state)"
ssh "$VDS_HOST" "
  set -e
  cd '$REMOTE_DIR'
  git fetch origin
  git reset --hard
  git clean -fd
  git checkout '$BRANCH'
  git pull origin '$BRANCH'
"

echo "[3/6] rebuild containers"
ssh "$VDS_HOST" "
  set -e
  cd '$REMOTE_DIR/deploy'
  docker compose -f '$COMPOSE_FILE' up -d --build
"

echo "[4/6] run migrations"
ssh "$VDS_HOST" "
  set -e
  cd '$REMOTE_DIR/deploy'
  docker compose -f '$COMPOSE_FILE' exec -T api alembic upgrade head
"

echo "[5/6] status"
ssh "$VDS_HOST" "
  set -e
  cd '$REMOTE_DIR/deploy'
  docker compose -f '$COMPOSE_FILE' ps
"

echo "[6/6] done"
