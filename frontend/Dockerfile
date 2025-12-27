# Use an official node image as the base image
FROM node:20 AS base

WORKDIR /app

# Development stage
FROM base AS dev
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile
EXPOSE 3000 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# Production builder stage
FROM base AS builder
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile
COPY . .
RUN npm run build
RUN yarn install --frozen-lockfile --production

# Production stage
FROM base AS production
COPY --from=builder /app/build ./build
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
EXPOSE 3000
CMD ["npm", "run", "start"]
