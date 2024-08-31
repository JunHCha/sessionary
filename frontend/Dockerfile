# Use an official node image as the base image
FROM node:21 AS builder

WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile
COPY . .
RUN npm run build
RUN yarn install --frozen-lockfile --production

# Expose port 3000
EXPOSE 3000

# Start the server
CMD ["npm", "run", "start"]
