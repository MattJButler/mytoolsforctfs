


# Stego

 - steghide



# Port Bruteforcing:
 - nmap -sV -sC -oN nmap/initial: this is for first enumerations 
 - rustscan: for quicker enumerations

# Directory Bruteforcing:
 - gobuster: commandline tool that bruteforces web directories and pages.
 - dirbuster: gui tool that bruteforces web directories and pages (dont really use this because of gui)
 - look at own tool and see if its fast
# SQL
 - Burpsuite intruder mode with wfuzz payload
 - sqlmap.py for easier
 - try blind
# Payloads
- go to pentestmonkey for rev shells
- msfconsole 
- https://www.exploit-db.com

# Hashes
 - Johntheripper for any rsa based stuff
 - hashcat for bruteforcing hashes
 
 # Bruteforcing 
 - For ssh and ftp use hydra
 - for website bruteforcing using either burpsuite intruder module or make one with python
# Encryption
 - https://github.com/nlitsme/vimdecrypt for vim encryption
# PrivEsc
 - if lazy use linpeas.sh
 # if not here are the steps
 - sudo -l # allow to run a program as a certain user
 - find . -perm /4000 2>/dev/null # SUID   
 - find . -perm /2000 2>/dev/null # SGID
 - find . -perm /6000 2>/dev/null # Both SUID and SGID
 - if find a not normal suid and sgid consult https://gtfobins.github.io/
  

