import string
import argparse
import platform
from typing import Set, Tuple, List

def detect_os_wordlist_path() -> str:
    #determine the default wordlist path based on the operating system.
    os_name = platform.system().lower()

    if 'darwin' in os_name:  
        return "/usr/share/dict/words"
    elif 'linux' in os_name:
        return "/usr/share/dict/american-english"
    elif 'windows' in os_name:
        print(" no default wordlist available for Windows.")
        custom_path = input("please provide the path to a wordlist file: ").strip()
        return custom_path
    else:
        print(" unsupported OS. Please provide the path to a wordlist file.")
        custom_path = input("path to wordlist: ").strip()
        return custom_path

def load_wordlist(path: str) -> Set[str]:
    #Load a list of lowercase English words from the given file path.
    try:
        with open(path, "r") as file:
            return {word.strip().lower() for word in file}
    except FileNotFoundError:
        print(f"error: cannot find the word list at: {path}")
        return set()

def decrypt_caesar(text: str, shift: int) -> str:
    #Decrypt a Caesar cipher text using the given shift.
    decrypted = []
    for char in text:
        if char.isalpha():
            offset = ord('A') if char.isupper() else ord('a')
            decrypted_char = chr((ord(char) - offset - shift) % 26 + offset)
            decrypted.append(decrypted_char)
        else:
            decrypted.append(char)
    return ''.join(decrypted)

def english_score(text: str, wordlist: Set[str]) -> float:
    #Calculate the percentage of valid english words in the text compared from system wordlist
    words = text.lower().split()
    valid = sum(1 for word in words if word.strip(string.punctuation) in wordlist)
    return valid / len(words) if words else 0.0

def auto_crack_caesar(ciphertext: str, wordlist: Set[str], threshold: float = 0.9) -> Tuple[int, str, float]:
    #Try to crack Caesar cipher by evaluating all shifts and scoring against English wordlist.
    candidates: List[Tuple[int, str, float]] = []

    for shift in range(26):
        decrypted = decrypt_caesar(ciphertext, shift)
        score = english_score(decrypted, wordlist)
        candidates.append((shift, decrypted, score))

    candidates.sort(key=lambda x: x[2], reverse=True)

    print("\n top 3 Most English Decryptions and percentages:")
    for i, (shift, text, score) in enumerate(candidates[:3], start=1):
        preview = text[:100] + ("..." if len(text) > 100 else "")
        print(f"\n#{i}: Shift = {shift}, Score = {score:.2%}")
        print(f"preview: {preview}")

    for shift, text, score in candidates:
        if score >= threshold:
            return shift, text, score

    print("\n⚠️ no shift reached the 90% threshold,Falling back to best match.")
    return candidates[0]

def main():
    parser = argparse.ArgumentParser(description="Caesar Cipher Auto-Cracker")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", type=str, help="path to file containing ciphertext")
    group.add_argument("-t", "--text", type=str, help="ciphertext string passed inline")

    args = parser.parse_args()

    wordlist_path = detect_os_wordlist_path()
    wordlist = load_wordlist(wordlist_path)
    if not wordlist:
        print("stopping: Wordlist could not be loaded.")
        return 1

    if args.file:
        try:
            with open(args.file, 'r') as f:
                ciphertext = f.read().strip()
        except FileNotFoundError:
            print(f"Error: File not found - {args.file}")
            return 1
    else:
        ciphertext = args.text.strip()

    shift, plaintext, score = auto_crack_caesar(ciphertext, wordlist)
    
    print(f"\n final shift chosen: {shift}")
    print(f"highest english Match Score: {score:.2%}")
    print("decrypted message:\n", plaintext)

if __name__ == "__main__":
    main()
