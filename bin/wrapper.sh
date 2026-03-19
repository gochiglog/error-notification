#!/usr/bin/env bash
#
# wrapper.sh
# "ユーザーはトークン不要。開発者サーバがPushする" モデル用
# ------------------------------------------------------------
# 1) ユーザーが "wrapper.sh python main.py" のようにコマンドを指定
# 2) wrapper.sh がコマンド成否を判定し、サーバへ結果情報をHTTP POST
# 3) サーバ(Lambda等)が受け取って、LINEへのPush通知を実行する仕組み
#
# ※ .env.sample 例:
#   NOTIFY_API_URL="https://example.com/notifyError"
#   USER_ID="Uxxxxxxxxx..."

set -e
trap 'on_exit' EXIT

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/.."

# .env 読み込み
if [ -f "${PROJECT_ROOT}/resources/.env" ]; then
  source "${PROJECT_ROOT}/resources/.env"
else
  echo "[ERROR] .env file not found in resources/."
  exit 1
fi

# ログファイル
LOG_FILE="${PROJECT_ROOT}/logs/error_monitor.log"

#--------------------------------------
# on_exit: コマンド終了時に呼ばれる
#--------------------------------------
on_exit() {
  local exit_code=$?
  local cmd="$*"

  # 成否判定
  if [ "${exit_code}" -eq 0 ]; then
    local message="Success: Command '${cmd}' exited with code 0."
  else
    local message="Error: Command '${cmd}' failed with code ${exit_code}."
  fi

  # ログに記録
  echo "$(date '+%Y-%m-%d %H:%M:%S') - ${message}" >> "${LOG_FILE}"

  # サーバへエラー情報などを送信 (ユーザーID, メッセージ)
  send_to_server "${USER_ID}" "${message}"
}

#--------------------------------------
# send_to_server: サーバにエラー情報を渡す
#--------------------------------------
send_to_server() {
  local user_id="$1"
  local info_msg="$2"

  # ユーザの .env に設定されたサーバエンドポイント
  if [ -z "${NOTIFY_API_URL}" ]; then
    echo "[ERROR] NOTIFY_API_URL is not set in .env"
    return
  fi

  # JSONペイロード
  local payload=$(cat << EOF
{
  "userId": "${user_id}",
  "message": "${info_msg}"
}
EOF
)

  # HTTP POST
  curl -s -X POST "${NOTIFY_API_URL}" \
    -H "Content-Type: application/json" \
    -d "${payload}"

  # ↑サーバ(開発者管理)側で push 用のトークン等を保持し、
  #  ユーザの userId宛に LINE Messaging APIを呼び出す想定。
}

#--------------------------------------
# "$@" でユーザコマンドを実行
#--------------------------------------
"$@"