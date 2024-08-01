# Use an official Node runtime as a parent image
FROM node:18.20.3-slim

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the current directory contents into the container at /app
COPY . .

# Expose port 5173 for the app (default Vite port)
EXPOSE 5173

# Run the application
CMD ["npm", "run", "dev"]