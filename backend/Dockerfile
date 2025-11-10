
# ---- Base build image ----
FROM node:20-alpine AS build
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Build (if using NestJS or TypeScript)
# Comment this out if you're using plain JS
RUN npm run build

# ---- Production runtime ----
FROM node:20-alpine
WORKDIR /app

# Copy only necessary files
COPY package*.json ./
RUN npm ci --omit=dev

# Copy compiled code or src files
# If you built TypeScript, copy /dist
# If plain JS, copy source directly
COPY --from=build /app/dist ./dist
# or COPY --from=build /app ./  (for non-TS projects)

# Expose port
EXPOSE 4000

# Start command
CMD ["npm", "run", "start:prod"]
