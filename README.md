# YouTube Music Downloader

## Overview

This is my sandbox where I integrate different DevOps stuff and more.
The project itself is a simple service for downloading audio from given YouTube videos.
The current version is built using Microservice architecture.

The service consists of the following components:

- FrontEnd (TypeScript, NextJS) - a web portal where a user must log in and then enter YouTube video URL and download audio.
- Gateway (Python, Flask) - a gateway to the services network.
- Auth (Python, Flask) - an authorization microservice.
- Downloader (Python) - a service responsible for downloading audio files from YouTube.

## CI

Each service has its own pipeline that tests, builds the image, and then publishes it to Dockerhub.

[![Release Auth Image](https://github.com/AlieksieievYurii/YouTubeDownloaderSandbox/actions/workflows/build-auth-image.yml/badge.svg?branch=main)](https://github.com/AlieksieievYurii/YouTubeDownloaderSandbox/actions/workflows/build-auth-image.yml)

[![Release Gateway Image](https://github.com/AlieksieievYurii/YouTubeDownloaderSandbox/actions/workflows/build-gateway-image.yml/badge.svg?branch=main)](https://github.com/AlieksieievYurii/YouTubeDownloaderSandbox/actions/workflows/build-gateway-image.yml)

[![Release YT Downloader Image](https://github.com/AlieksieievYurii/YouTubeDownloaderSandbox/actions/workflows/build-downloader-image.yml/badge.svg?branch=main)](https://github.com/AlieksieievYurii/YouTubeDownloaderSandbox/actions/workflows/build-downloader-image.yml)
