import tkinter as tk
from tkinter import ttk, messagebox
import math
import json
from collections import Counter

# -------------------------------------------------
# 1️⃣ ALL ALGORITHMS (RLE, MTF, WMTF, PWMTF, SHANNON, SHANNON-FANO, HUFFMAN, ARITHMETIC, LZW)
# -------------------------------------------------

def rle_encode(text):
    if not text: return ""
    result = []
    count = 1
    for i in range(1, len(text)):
        if text[i] == text[i-1]:
            count += 1
        else:
            result.append(f"{text[i-1]}{count}")
            count = 1
    result.append(f"{text[-1]}{count}")
    return ''.join(result)

def rle_decode(text):
    if not text: return ""
    result = ""
    char = ""
    count = ""
    for c in text:
        if c.isdigit():
            count += c
        else:
            if char: result += char * int(count)
            char = c
            count = ""
    if char: result += char * int(count)
    return result

def mtf_encode(text, alphabet_str):
    alphabet = list(alphabet_str)
    encoded = []
    for c in text:
        idx = alphabet.index(c)
        encoded.append(idx)
        alphabet.pop(idx)
        alphabet.insert(0, c)
    return json.dumps(encoded)

def mtf_decode(data_str, alphabet_str):
    alphabet = list(alphabet_str)
    decoded = ""
    data = json.loads(data_str)
    for idx in data:
        c = alphabet[idx]
        decoded += c
        alphabet.pop(idx)
        alphabet.insert(0, c)
    return decoded

def wmtf_encode(text, alphabet_str):
    alphabet = list(alphabet_str)
    weights = {c: 1 for c in alphabet}
    working_alphabet = alphabet.copy()
    encoded = []
    for c in text:
        working_alphabet.sort(key=lambda x: (-weights[x], alphabet.index(x)))
        idx = working_alphabet.index(c)
        encoded.append(idx)
        weights[c] += 1
    return json.dumps(encoded)

def wmtf_decode(data_str, alphabet_str):
    alphabet = list(alphabet_str)
    weights = {c: 1 for c in alphabet}
    working_alphabet = alphabet.copy()
    decoded = ""
    data = json.loads(data_str)
    for idx in data:
        working_alphabet.sort(key=lambda x: (-weights[x], alphabet.index(x)))
        c = working_alphabet[idx]
        decoded += c
        weights[c] += 1
    return decoded

def pwmtf_encode(text, alphabet_str):
    alphabet = list(alphabet_str)
    prob = {c: 1.0/len(alphabet) for c in alphabet}
    working_alphabet = alphabet.copy()
    encoded = []
    for i, c in enumerate(text, start=1):
        working_alphabet.sort(key=lambda x: (-prob[x], alphabet.index(x)))
        idx = working_alphabet.index(c)
        encoded.append(idx)
        prob[c] = max(1, math.floor(i * prob[c]))
    return json.dumps(encoded)

def pwmtf_decode(data_str, alphabet_str):
    alphabet = list(alphabet_str)
    prob = {c: 1.0/len(alphabet) for c in alphabet}
    working_alphabet = alphabet.copy()
    decoded = ""
    data = json.loads(data_str)
    for i, idx in enumerate(data, start=1):
        working_alphabet.sort(key=lambda x: (-prob[x], alphabet.index(x)))
        c = working_alphabet[idx]
        decoded += c
        prob[c] = max(1, math.floor(i * prob[c]))
    return decoded

def shannon_encode(text):
    freq = Counter(text)
    total = sum(freq.values())
    symbols = sorted(freq.items(), key=lambda x: -x[1])
    codes, cumulative = {}, 0
    for char, f in symbols:
        p = f / total
        length = math.ceil(-math.log2(p)) if p > 0 else 1
        code = format(int(cumulative * (2**length)), f"0{length}b")
        codes[char] = code
        cumulative += p
    return ''.join(codes[c] for c in text), codes

def shannon_decode(encoded, codes):
    reverse = {v: k for k, v in codes.items()}
    buffer, result = "", ""
    for bit in encoded:
        buffer += bit
        if buffer in reverse:
            result += reverse[buffer]
            buffer = ""
    return result

# ---------------- Shannon-Fano -------------------
def shannon_fano_encode(text):
    freq = Counter(text)
    symbols = sorted(freq.items(), key=lambda x: -x[1])
    codes = {c: "" for c in freq}
    def assign_codes(symbols_list, prefix=""):
        if len(symbols_list) == 1:
            c, _ = symbols_list[0]
            codes[c] = prefix or "0"
            return
        total = sum(f for _, f in symbols_list)
        acc = 0
        split_index = 0
        for i, (_, f) in enumerate(symbols_list):
            acc += f
            if acc >= total / 2:
                split_index = i + 1
                break
        assign_codes(symbols_list[:split_index], prefix + "0")
        assign_codes(symbols_list[split_index:], prefix + "1")
    assign_codes(symbols)
    encoded_text = ''.join(codes[c] for c in text)
    return encoded_text, codes

def shannon_fano_decode(encoded, codes):
    reverse = {v: k for k, v in codes.items()}
    buffer, result = "", ""
    for bit in encoded:
        buffer += bit
        if buffer in reverse:
            result += reverse[buffer]
            buffer = ""
    return result
# ---------------- End Shannon-Fano -------------------

def huffman_encode(text):
    freq = Counter(text)
    if not freq: return "", {}
    nodes = [[f, [c, ""]] for c, f in freq.items()]
    while len(nodes) > 1:
        nodes.sort()
        l, r = nodes.pop(0), nodes.pop(0)
        for pair in l[1:]: pair[1] = '0' + pair[1]
        for pair in r[1:]: pair[1] = '1' + pair[1]
        nodes.append([l[0] + r[0]] + l[1:] + r[1:])
    codes = dict(nodes[0][1:])
    return ''.join(codes[c] for c in text), codes

def huffman_decode(encoded, codes):
    reverse = {v: k for k, v in codes.items()}
    buffer, result = "", ""
    for bit in encoded:
        buffer += bit
        if buffer in reverse:
            result += reverse[buffer]
            buffer = ""
    return result

def arithmetic_encode(text):
    freq = Counter(text)
    total = sum(freq.values())
    low, high, probs, cdf = 0.0, 1.0, {}, 0.0
    for c, f in sorted(freq.items()):
        probs[c] = (cdf, cdf + f / total)
        cdf += f / total
    for c in text:
        range_ = high - low
        high = low + range_ * probs[c][1]
        low = low + range_ * probs[c][0]
    return str((low + high) / 2), probs, len(text)

def arithmetic_decode(value, probs, length):
    value = float(value)
    result = ""
    for _ in range(length):
        for c, (l, h) in probs.items():
            if l <= value < h:
                result += c
                value = (value - l) / (h - l)
                break
    return result

def lzw_encode(text):
    if not text: return ""
    dict_size, dictionary, w, result = 256, {chr(i): i for i in range(256)}, "", []
    for c in text:
        wc = w + c
        if wc in dictionary: w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc], dict_size, w = dict_size, dict_size + 1, c
    if w: result.append(dictionary[w])
    return json.dumps(result)

def lzw_decode(data_str):
    if not data_str: return ""
    compressed = json.loads(data_str)
    dict_size, dictionary = 256, {i: chr(i) for i in range(256)}
    w = chr(compressed.pop(0))
    result = [w]
    for k in compressed:
        if k in dictionary: entry = dictionary[k]
        elif k == dict_size: entry = w + w[0]
        else: raise ValueError(f"Bad k: {k}")
        result.append(entry)
        dictionary[dict_size], dict_size, w = w + entry[0], dict_size + 1, entry
    return "".join(result)

# -------------------------------------------------
# ✨ GIRLY GUI LOGIC ✨
# -------------------------------------------------

root = tk.Tk()
root.title("✨ Data Fairy Compression ✨")
root.geometry("750x750")

BG_CREAM = "#FFFBEB"
PRIMARY_YELLOW = "#FEF3C7"
ACCENT_GOLD = "#D97706"
BTN_COLOR = "#FDE68A"
WHITE = "#FFFFFF"

root.configure(bg=BG_CREAM)
style = ttk.Style()
style.theme_use('clam')
style.configure("TLabel", background=BG_CREAM, foreground=ACCENT_GOLD, font=("Segoe UI", 12, "bold"))
style.configure("TButton", background=BTN_COLOR, font=("Segoe UI", 10, "bold"), borderwidth=0)
style.map("TButton", background=[('active', PRIMARY_YELLOW)])

header = tk.Label(root, text="Compression Studio ✨", font=("Georgia", 24, "italic"), bg=BG_CREAM, fg=ACCENT_GOLD)
header.pack(pady=20)

frame_top = tk.Frame(root, bg=BG_CREAM)
frame_top.pack(pady=5)
ttk.Label(frame_top, text="Select Magic Algorithm:").pack(side=tk.LEFT, padx=10)

algo = tk.StringVar(value="RLE")
algorithms = ["RLE", "MTF", "W-MTF", "PW-MTF", "Shannon", "Shannon-Fano", "Huffman", "Arithmetic", "LZW"]
dropdown = ttk.OptionMenu(frame_top, algo, algo.get(), *algorithms)
dropdown.pack(side=tk.LEFT)

ttk.Label(root, text="Type your secret message here:").pack(anchor="w", padx=80)
input_text = tk.Text(root, height=6, width=60, font=("Consolas", 11), bg=WHITE, relief="flat", padx=10, pady=10)
input_text.pack(pady=5)

extra_input = tk.Entry(root, width=70, font=("Segoe UI", 10), bg=WHITE, relief="flat", fg="#9CA3AF")
extra_input.pack(pady=10, ipady=5)
extra_input.insert(0, " 🪄 Alphabet magic happens here automatically...")

def on_entry_click(event):
    if "Alphabet" in extra_input.get():
       extra_input.delete(0, "end")
       extra_input.configure(fg="black")
extra_input.bind('<FocusIn>', on_entry_click)

ttk.Label(root, text="Compressed Result:").pack(anchor="w", padx=80)
output_text = tk.Text(root, height=6, width=60, font=("Consolas", 11), bg=WHITE, relief="flat", padx=10, pady=10)
output_text.pack(pady=5)

stored_codes = {}

def encode():
    text = input_text.get("1.0", tk.END).strip()
    if not text: return
    
    alpha = extra_input.get().strip()
    if not alpha or "Alphabet" in alpha:
        alpha = "".join(sorted(list(set(text))))
        extra_input.delete(0, tk.END)
        extra_input.insert(0, alpha)
    
    a = algo.get()
    try:
        res = ""
        if a == "RLE": res = rle_encode(text)
        elif a == "MTF": res = mtf_encode(text, alpha)
        elif a == "W-MTF": res = wmtf_encode(text, alpha)
        elif a == "PW-MTF": res = pwmtf_encode(text, alpha)
        elif a == "Shannon": res, stored_codes['c'] = shannon_encode(text)
        elif a == "Shannon-Fano": res, stored_codes['sf'] = shannon_fano_encode(text)
        elif a == "Huffman": res, stored_codes['c'] = huffman_encode(text)
        elif a == "Arithmetic": res, stored_codes['p'], stored_codes['l'] = arithmetic_encode(text)
        elif a == "LZW": res = lzw_encode(text)
        
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, str(res))
    except Exception as e:
        messagebox.showerror("Error", f"Magic failed: {str(e)}")

def decode():
    text = output_text.get("1.0", tk.END).strip()
    if not text: return
    alpha = extra_input.get().strip()
    a = algo.get()
    try:
        res = ""
        if a == "RLE": res = rle_decode(text)
        elif a == "MTF": res = mtf_decode(text, alpha)
        elif a == "W-MTF": res = wmtf_decode(text, alpha)
        elif a == "PW-MTF": res = pwmtf_decode(text, alpha)
        elif a == "Shannon": res = shannon_decode(text, stored_codes['c'])
        elif a == "Shannon-Fano": res = shannon_fano_decode(text, stored_codes['sf'])
        elif a == "Huffman": res = huffman_decode(text, stored_codes['c'])
        elif a == "Arithmetic": res = arithmetic_decode(text, stored_codes['p'], stored_codes['l'])
        elif a == "LZW": res = lzw_decode(text)
        
        input_text.delete("1.0", tk.END)
        input_text.insert(tk.END, res)
    except Exception as e:
        messagebox.showerror("Error", f"Unlocking failed: {str(e)}")

btn_frame = tk.Frame(root, bg=BG_CREAM)
btn_frame.pack(pady=20)

encode_btn = tk.Button(btn_frame, text="✨ ENCODE ✨", command=encode, bg=BTN_COLOR, fg=ACCENT_GOLD, 
                       font=("Segoe UI", 12, "bold"), relief="flat", padx=20, pady=10, cursor="heart")
encode_btn.grid(row=0, column=0, padx=20)

decode_btn = tk.Button(btn_frame, text="🔓 DECODE 🔓", command=decode, bg=BTN_COLOR, fg=ACCENT_GOLD, 
                       font=("Segoe UI", 12, "bold"), relief="flat", padx=20, pady=10, cursor="heart")
decode_btn.grid(row=0, column=1, padx=20)

footer = tk.Label(root, text="Made with ✨ and Logic", font=("Segoe UI", 9), bg=BG_CREAM, fg="#D1D5DB")
footer.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
