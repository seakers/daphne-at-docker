FROM node:16

# The working directory where interface is placed is /usr/src/app/daphne-at-interface
WORKDIR /usr/src/app/
# Copy everything in the daphne_brain directory to /usr/src/app/daphne-at-interface
COPY package*.json ./

RUN npm install --silent

# Copy Interface
COPY . ./

EXPOSE 8080

#CMD npm run dev
CMD [ "npm", "run", "dev"]