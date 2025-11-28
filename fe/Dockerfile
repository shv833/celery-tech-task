FROM node:20-alpine AS builder
WORKDIR /usr/src/app

COPY ./app/package.json ./app/yarn.lock ./
RUN yarn install
COPY ./app ./

FROM node:20-alpine AS runner
WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/yarn.lock ./
COPY --from=builder /usr/src/app/package.json ./
COPY --from=builder /usr/src/app/vite.config.js ./
COPY --from=builder /usr/src/app/index.html ./
COPY --from=builder /usr/src/app/public ./public
COPY --from=builder /usr/src/app/node_modules ./node_modules

ENTRYPOINT ["yarn", "dev"]
