#!/bin/bash -xe

cmd_clean() {
    docker ps -aq --filter label=dsopz_dev | xargs docker rm -f || true
    docker system prune --volumes --filter label=dsopz_dev -f || true
}

cmd_docker_build() {
    docker build -t dsopz/dsopz:dev .
}

cmd_docker_run() {
    cmd_docker_build
    docker volume create --label dsopz_dev dsopz_config || true
    docker run -it --rm --label dsopz_dev \
        -v "$(pwd):/opt/dsopz" \
        -w "/opt/dsopz" \
        --mount "type=volume,src=dsopz_config,dst=/root/.dsopz" \
        dsopz/dsopz:dev "$@"
        #python:3.8-buster "$@"
}

cmd_docker_login() {
    cmd_docker_run python -m dsopz.dsopz login-text
}

cmd_docker_test() {
    cmd_docker_run ./test/test.sh "$@"
}

cmd_encrypt() {
    [[ "x$DSOPZ_SECRET" != "x" ]]
    dsopz_file="${1?'dsopz_file is required'}"
    [[ -f "$dsopz_file" ]]
    rm "$dsopz_file.gpg" || true
    gpg --symmetric --cipher-algo AES256 --batch --passphrase "$DSOPZ_SECRET" "$dsopz_file"
}

cmd_decrypt() {
    [[ "x$DSOPZ_SECRET" != "x" ]]
    find  . -name "*.gpg" | while read k; do
        echo "decrypt: $k";
        rm "$(echo "$k" | sed "s/\.gpg$//g")" || true
        gpg --decrypt --batch --passphrase "$DSOPZ_SECRET" -o "$(echo "$k" | sed "s/\.gpg$//g")" "$k" 
    done
}

cd "$(dirname "$0")"; _cmd="${1?"cmd is required"}"; shift; "cmd_${_cmd}" "$@"