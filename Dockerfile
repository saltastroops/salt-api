FROM node:14 AS builder
WORKDIR /web-manager
ARG RUN_MODE
COPY . .
RUN npm install

RUN  if ["$RUN_MODE" = "staging"] ; then npm run build-staging ; fi
RUN  if ["$RUN_MODE" = "development"] ; then npm run watch ; fi
RUN  if ["$RUN_MODE" = "production"] ; then npm run build-production ; fi

FROM nginx:1.23.1
COPY --from=builder /web-manager/dist/web-manager/ /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80
