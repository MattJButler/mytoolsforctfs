import string
from typing import Set, Tuple, List

def load_wordlist(path: str = "/usr/share/dict/words") -> Set[str]:
    #Load a list of lowercase English words from the given file path.
    try:
        with open(path, "r") as file:
            return {word.strip().lower() for word in file}
    except FileNotFoundError:
        print(f" Error: Cannot find the native word list of mac ({path})")
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
    #Calculate the percentage of valid english words in the text compared from just the mac inbuilt wordlist
    words = text.lower().split()
    valid = sum(1 for word in words if word.strip(string.punctuation) in wordlist)
    return valid / len(words) if words else 0.0

def auto_crack_caesar(ciphertext: str, wordlist: Set[str], threshold: float = 0.9) -> Tuple[int, str, float]:
    #try to crack Caesar cipher by evaluating all shifts and scoring against English wordlist.
    candidates: List[Tuple[int, str, float]] = []

    for shift in range(26):
        decrypted = decrypt_caesar(ciphertext, shift)
        score = english_score(decrypted, wordlist)
        candidates.append((shift, decrypted, score))

    candidates.sort(key=lambda x: x[2], reverse=True)

    print("\n Top 3 Most English Decryptions and percentages:")
    for i, (shift, text, score) in enumerate(candidates[:3], start=1):
        preview = text[:100] + ("..." if len(text) > 100 else "")
        print(f"\n#{i}: Shift = {shift}, Score = {score:.2%}")
        print(f"Preview: {preview}")

    for shift, text, score in candidates:
        if score >= threshold:
            return shift, text, score

    print("\n⚠️ No shift reached the 90% threshold. Falling back to best match.")
    return candidates[0]

def main():
    wordlist = load_wordlist()
    if not wordlist:
        return 0

    ciphertext = input("Enter Caesar ciphertext: ").strip()
    shift, plaintext, score = auto_crack_caesar(ciphertext, wordlist)
    
    print(f"\n final shift chosen: {shift}")
    print(f"highest english Match Score: {score:.2%}")
    print("decrypted message:\n", plaintext)

if __name__ == "__main__":
    main()
