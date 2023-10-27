IMAGE_NAME := "ghcr.io/chand1012/mindraw"

build:
  docker build -t {{IMAGE_NAME}} .

run:
  docker run --env-file=.env {{IMAGE_NAME}}
