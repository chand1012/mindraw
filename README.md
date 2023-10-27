# Mindraw

Mindraw (pronounced Mind-draw) is an image generation tool inspired by [Midjourney](https://www.midjourney.com/home/?callbackUrl=%2Fapp%2F) using [Stable Diffusion](https://stability.ai/blog/stable-diffusion-public-release) and my own [Simple Stable Diffusion API](https://github.com/chand1012/simple-stable-diffusion).

## Installation

1. Install [Simple Stable Diffusion API](https://github.com/chand1012/simple-stable-diffusion) somewhere this bot can access the HTTP API.
2. Clone this repo.
3. `docker build -t mindraw .`
4. Copy `.env.example` and populate the values. `cp .env.example .env`
5. `docker run --env-file .env mindraw`
