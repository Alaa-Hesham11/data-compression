# data-compression
Data Fairy Compression Studio 
A stylish, Python-based graphical user interface (GUI) application that implements various Lossless Data Compression algorithms. This tool allows users to visualize how different encoding techniques transform text data to reduce its size and how they can be perfectly decoded back to the original message.

🚀 Features
Girly & Intuitive UI: Built with tkinter featuring a cream-and-gold aesthetic ("Girly Studio" theme).

Multi-Algorithm Support: Compare different compression techniques in one place.

Auto-Alphabet Magic: Automatically generates the required alphabet/dictionary from your input text if not manually provided.

Two-Way Processing: Full support for both Encoding (Compression) and Decoding (Decompression).

📂 Supported Algorithms
The studio includes 9 powerful algorithms categorized by their logic:

1. Dictionary & Transformation Based
RLE (Run-Length Encoding): Summarizes repeated characters (e.g., AAA -> A3).

LZW (Lempel-Ziv-Welch): A dictionary-based compression used in GIF and ZIP formats.

MTF (Move-To-Front): Improves entropy by moving recently used characters to the front of a list.

W-MTF & PW-MTF: Weighted and Probabilistic variations of the Move-To-Front algorithm for advanced entropy coding.

2. Statistical & Entropy Coding
Huffman Coding: Uses a frequency-sorted binary tree to assign variable-length codes.

Shannon-Fano: A prefix coding technique based on dividing probabilities into equal halves.

Shannon: The classic entropy-based coding method.

Arithmetic Coding: Encodes the entire message into a single floating-point number between 0 and 1.

🛠️ Requirements
Python 3.x

Standard libraries: tkinter, json, math, collections. (No external pip installs required!)

💻 How to Use
Run the application:

Bash

python compression_studio.py
Select your "Magic Algorithm" from the dropdown menu.

Type your secret message in the top text box.

Click ✨ ENCODE ✨ to see the compressed result and the generated alphabet.

Click 🔓 DECODE 🔓 to transform the compressed data back into the original text.
