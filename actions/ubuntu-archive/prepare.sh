#!/usr/bin/env bash
set -euo pipefail

test "$RUNNER_ENVIRONMENT" = github-hosted
. /etc/os-release
test "$ID" = ubuntu
test "$(dpkg --print-architecture)" = amd64
case "$VERSION_CODENAME" in jammy|noble) ;; *) exit 1 ;; esac
keyring=/usr/share/keyrings/ubuntu-archive-keyring.gpg
test -s "$keyring"

root=()
if (( EUID != 0 )); then root=(sudo -n); fi
archive=$(mktemp -d /tmp/volparossa-apt.XXXXXXXXXX)
chmod 755 "$archive"
pockets=("$VERSION_CODENAME" "$VERSION_CODENAME-updates" "$VERSION_CODENAME-security")

complete_indices() {
  local config=$1 pocket component filename
  for pocket in "${pockets[@]}"; do
    for component in main universe; do
      filename=$(apt-get -c "$config" indextargets --format '$(FILENAME)' \
        'Identifier: Packages' "Release: $pocket" "Component: $component" 'Architecture: amd64') || return 1
      [[ -s "$filename" ]] || return 1
    done
  done
}

for mirror in https://azure.archive.ubuntu.com/ubuntu https://mirrors.mit.edu/ubuntu https://archive.ubuntu.com/ubuntu; do
  # Each mirror starts with empty lists. A failed refresh can never satisfy a later attempt.
  candidate=$(mktemp -d "$archive/mirror.XXXXXXXX")
  mkdir "$candidate/lists"
  chmod 755 "$candidate" "$candidate/lists"
  for pocket in "${pockets[@]}"; do
    printf 'deb [arch=amd64 signed-by=%s target=Packages] %s %s main universe\n' "$keyring" "$mirror" "$pocket"
  done > "$candidate/ubuntu.list"
  config="$candidate/apt.conf"
  cat > "$config" <<CONF
Dir::Etc::sourcelist "$candidate/ubuntu.list";
Dir::Etc::sourceparts "-";
Dir::State::lists "$candidate/lists";
Acquire::Languages "none";
Acquire::Retries "1";
Acquire::https::Timeout "15";
APT::Update::Error-Mode "any";
CONF
  chmod 644 "$config" "$candidate/ubuntu.list"
  # APT's per-request timeout allows a stalled update to outlive an entire job.
  if "${root[@]}" timeout --kill-after=5s 90s apt-get -c "$config" -o Acquire::Retries=0 update \
      && complete_indices "$config"; then
    printf 'Verified six signed Ubuntu package indices from %s\n' "$mirror"
    printf 'config=%s\n' "$config" >> "$GITHUB_OUTPUT"
    exit 0
  fi
  printf 'Failed to fetch complete signed Ubuntu package indices from %s\n' "$mirror" >&2
  "${root[@]}" rm -r -- "$candidate"
done
rmdir "$archive"
exit 1
