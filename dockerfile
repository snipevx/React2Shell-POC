FROM node:20-bookworm

WORKDIR /app

# 1. Create package.json with the necessary scripts
RUN echo '{\
  "name": "vulnerable-nextjs",\
  "version": "0.1.0",\
  "private": true,\
  "scripts": {\
    "build": "next build",\
    "start": "next start"\
  }\
}' > package.json

# 2. Install the specific vulnerable versions (forcing bypass of peer conflicts)
RUN npm install next@15.0.0 react@19.0.0 react-dom@19.0.0 --legacy-peer-deps

# 3. Create a minimal JS-based App Router structure
RUN mkdir -p src/app
RUN echo 'export default function Page() { return <h1>Vulnerable Environment Running</h1>; }' > src/app/page.js
RUN echo 'export default function RootLayout({ children }) { return <html lang="en"><body>{children}</body></html>; }' > src/app/layout.js

# 4. Build the application
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "start"]