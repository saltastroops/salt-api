FROM node:14 AS builder
WORKDIR /web-manager
ARG RUN_MODE
COPY package.json .
COPY package-lock.json .
RUN CYPRESS_INSTALL_BINARY=0 npm ci --omit=dev
COPY . .

RUN  if [ "$RUN_MODE" = "staging" ] ; then npm run build-staging ; fi
RUN  if [ "$RUN_MODE" = "production" ] ; then npm run build-production ; fi

FROM nginx:1.23.1
COPY --from=builder /web-manager/dist/web-manager/ /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80
