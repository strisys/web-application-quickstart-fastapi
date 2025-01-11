# Web Application QuickStart with FastAPI

## Getting Started

The repository has two workspaces: client and API (server). The JavaScript client is an [HTML5 boilerplate-derived](https://html5boilerplate.com/) single-page web application. It will be bundled using Webpack and then copied to the public folder with the following commands.

``` bash
$ cd client
$ npm run build
...
```

The Python-based API project uses [FastAPI](https://fastapi.tiangolo.com/) and will serve as API endpoints, including one that returns static client assets from its public folder to run in the browser.  The api project can be run as follows from a PowerShell prompt in the api directory.

```bash
$ cd api
$ .\scripts\run-server.ps1

INFO:     Will watch for changes in these directories: ['...\\web-application-quickstart-fastapi\\api']
INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
INFO:     Started reloader process [23564] using StatReload
INFO:     Started server process [19024]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

To see the simple JSON returned, navigate to http://locahost:8080. This demonstrates that the client was successfully copied to the server and called one of its API endpoints.

## References

- [HTML5 Boilerplate](https://html5boilerplate.com/) & [Webpack](https://webpack.js.org/)
- [FastAPI](https://fastapi.tiangolo.com/)

