# Use the official Ubuntu 18.04 as the base image
FROM ubuntu:18.04

# Set environment variables to avoid user interaction during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install necessary packages
RUN apt-get update
RUN apt-get install -y wget gnupg
# gnupg  ca-certificates

# Add MongoDB GPG key and repository
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" > /etc/apt/sources.list.d/mongodb-org-4.2.list

# Install MongoDB
RUN apt-get update
RUN apt-get install -y mongodb-org

# Create the MongoDB data directory
RUN mkdir -p /data/db

# Expose the default MongoDB port
EXPOSE 27017

# Start MongoDB
# CMD ["mongod"]
