# Stage 1: Build React app
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Just output the static build for Nginx
FROM alpine:3.19
WORKDIR /build
COPY --from=build /app/build ./
