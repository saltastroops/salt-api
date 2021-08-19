FROM node:12 AS builder
WORKDIR /web-manager
COPY . .
RUN npm install
RUN npm run build --prod

FROM nginx:1.21.0
COPY --from=builder /web-manager/dist/web-manager/ /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
RUN sed "s/API_SERVER_URL/${API_SERVER_URL}/g"

# Expose port 80
EXPOSE 80
