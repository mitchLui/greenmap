FROM node:16

# Create app directory
WORKDIR /client

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN npm install

# Bundle app source
COPY . .


# Build app and serve
RUN npm run build

RUN npm install -g serve

EXPOSE $PORT
CMD serve -s build -l $PORT