## To run the app in production mode
- [Install docker engine](https://docs.docker.com/engine/install/)
- [Install docker compose](https://docs.docker.com/compose/install/)
- `docker-compose up -d --force-recreate --no-deps --build` (Please make sure port 80 and port 443 are not occupied by other processes.)
- The app will be available at http://localhost
## Shutdown
`docker-compose stop`