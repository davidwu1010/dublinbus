FROM node:12 as build
WORKDIR /usr/src/app
COPY ./package.json ./
RUN npm install --production
COPY ./ ./
RUN npm run build

FROM nginx:1.18
COPY --from=build /usr/src/app/build /usr/share/nginx/html
COPY letsencrypt /etc/letsencrypt
COPY nginx.conf /etc/nginx/nginx.conf
CMD ["nginx", "-g", "daemon off;"]
