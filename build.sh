#!/bin/bash -xe

cmd_clean() {
    docker ps -aq --filter label=dsopz_dev | xargs docker rm -f || true
    docker system prune --volumes --filter label=dsopz_dev -f || true
}

cmd_docker_build_python() {
    docker build -t dsopz/dsopz:dev .
}

cmd_docker_build_go() {
    docker build -f Dockerfile.go -t dsopz/dsopz-go:dev . 
}

cmd_docker_go() {
    docker run -i --rm --label dsopz_dev \
        -v "$(pwd):/opt/dsopz" \
        -w "/opt/dsopz" \
        -e "GITHUB_TOKEN=$GITHUB_TOKEN" \
        dsopz/dsopz-go:dev "$@"
}

cmd_docker_run() {
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

cmd_docker_serviceaccount() {
    cmd_docker_run python -m dsopz.dsopz login-serviceaccount -f test/dsopzit.secret.json
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

cmd_release() {
    CLOSE_VERSION="${1?'CLOSE_VERSION is required: 0.0.0'}"

    if git status -s | grep ".\\+"; then
        exit 1
    fi

    cmd_docker_run python -m dsopz.dsopz version

    echo "version=\"$CLOSE_VERSION\"" > dsopz/config.py
    git commit -am "releasing $CLOSE_VERSION"
    git tag "dsopz-$CLOSE_VERSION"
    git push origin "dsopz-$CLOSE_VERSION"

    cmd_docker_run python -m dsopz.dsopz version

    git push
}

cmd_docker_package() {
    cmd_docker_run python setup.py bdist_egg
}

cmd_docker_gh_release() {
    DSOPZ_VERSION="${1?'DSOPZ_VERSION to delete'}"
    cmd_docker_go github-release release --user murer --repo dsopz --tag "dsopz-$DSOPZ_VERSION" --name "dsopz-$DSOPZ_VERSION" --description "dsopz" || true
    cmd_docker_go github-release edit --user murer --repo dsopz --tag "dsopz-$DSOPZ_VERSION" --name "dsopz-$DSOPZ_VERSION" --description "dsopz"
    cd dist
    ls | while read k; do
        cmd_docker_go github-release upload --user murer --repo dsopz --tag "dsopz-$DSOPZ_VERSION" --name "$k" --file "$k"
    done
    cd -
}

cmd_docker_gh_delete() {
    DSOPZ_VERSION="${1?'DSOPZ_VERSION to delete'}"
    DSOPZ_VERSION_TWICE="${2?'DSOPZ_VERSION_TWICE to delete'}"
    [[ "$DSOPZ_VERSION_TWICE" == "$DSOPZ_VERSION" ]]
    cmd_docker_go github-release delete --user murer --repo dsopz --tag "dsopz-$DSOPZ_VERSION"
}

cd "$(dirname "$0")"; _cmd="${1?"cmd is required"}"; shift; "cmd_${_cmd}" "$@"