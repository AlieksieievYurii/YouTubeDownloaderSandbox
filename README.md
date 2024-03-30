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

## Frontend

The frontend is built using NextJS 14. 

### How to run

1. First of all, create .env.local, in _front_ folder, containing the following:
    ```
    NEXT_PUBLIC_GATEWAY_URL=<URL path to gateway>
    NEXT_PUBLIC_SERVER_SIDE_GATEWAY_URL=<This is optional. Using this variable you can override URL for accessing gateway from fronted's server>
    ```

2. Run `npm install` to install dependencies.
3. Run `npm run dev` to start the development instance.
4. Run `npm run build` to build the sources for production
   
