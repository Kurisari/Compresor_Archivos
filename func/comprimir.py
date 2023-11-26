import heapq
import pickle
from bitarray import bitarray
import cv2
import numpy as np

class ColorQuantization:
    def __init__(self, num_colors=16):
        self.num_colors = num_colors
    def quantize_video(self, input_file, output_file):
        cap = cv2.VideoCapture(input_file)
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter(output_file, fourcc, cap.get(5), (int(cap.get(3)), int(cap.get(4))))
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            quantized_frame = self.quantize_frame(frame)
            out.write(quantized_frame)
        cap.release()
        out.release()
    
    def quantize_frame(self, frame):
        pixels = frame.reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        _, labels, centers = cv2.kmeans(np.float32(pixels), self.num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)
        quantized_frame = centers[labels.flatten()]
        quantized_frame = quantized_frame.reshape(frame.shape)
        return quantized_frame

# class LZWCompressor:
#     def compress_lzw(self, input_file, output_file):
#         with open(input_file, 'rb') as file:
#             content = file.read()
#         compressed_content = self.compress_lzw_string(content)
#         with open(output_file, 'wb') as file:
#             pickle.dump(compressed_content, file)
#     def decompress_lzw(self, input_file, output_file):
#         with open(input_file, 'rb') as file:
#             compressed_content = pickle.load(file)
#         decompressed_content = self.decompress_lzw_string(compressed_content)
#         with open(output_file, 'w') as file:
#             file.write(decompressed_content)
#     def compress_lzw_string(self, data):
#         dictionary = {i.to_bytes(1, 'big'): i for i in range(256)}
#         current_code = 256
#         result = []
#         current_sequence = []
#         for char in data:
#             new_sequence = current_sequence + [char.to_bytes(1, 'big')]
#             # Convert new_sequence to a bytes object before checking if it's in the dictionary
#             new_sequence_bytes = b''.join(new_sequence)
#             if new_sequence_bytes in dictionary:
#                 current_sequence = new_sequence
#             else:
#                 if current_sequence:
#                     result.append(dictionary[b''.join(current_sequence)])
#                 dictionary[new_sequence_bytes] = current_code
#                 current_code += 1
#                 current_sequence = [char.to_bytes(1, 'big')]
#         if current_sequence:
#             result.append(dictionary[''.join(map(str, current_sequence))])
#         return result
#     def decompress_lzw_string(self, compressed_data):
#         dictionary = {i: chr(i) for i in range(256)}
#         current_code = 256
#         result = []
#         current_sequence = [compressed_data[0]]
#         for code in compressed_data[1:]:
#             if code in dictionary:
#                 new_sequence = dictionary[code]
#             elif code == current_code:
#                 new_sequence = current_sequence + [current_sequence[0]]
#             else:
#                 raise ValueError("Invalid compressed data")
#             result.append(new_sequence)
#             dictionary[current_code] = current_sequence + [new_sequence[0]]
#             current_code += 1
#             current_sequence = new_sequence
#         return ''.join(result)

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq
    
    def is_leaf(self):
        return self.left is None and self.right is None

class HuffmanTree:
    def __init__(self, char_freq=None):
        self.huffman_codes = {}
        self.root = None
        if char_freq is not None:
            self.nodes = [HuffmanNode(char, freq) for char, freq in char_freq.items()]
            heapq.heapify(self.nodes)
            self.build_huffman_tree()

    def build_huffman_tree(self):
        while len(self.nodes) > 1:
            left_node = heapq.heappop(self.nodes)
            right_node = heapq.heappop(self.nodes)
            internal_node = HuffmanNode(None, left_node.freq + right_node.freq)
            internal_node.left = left_node
            internal_node.right = right_node
            heapq.heappush(self.nodes, internal_node)
        self.root = self.nodes[0]
        self.generate_huffman_codes(self.root)

    def generate_huffman_codes(self, node, current_code=""):
        if node is None:
            return
        if node.is_leaf():
            self.huffman_codes[node.char] = current_code
        self.generate_huffman_codes(node.left, current_code + "0")
        self.generate_huffman_codes(node.right, current_code + "1")
    
    def serialize_huffman_tree(self, file):
        pickle.dump(self.root, file)
    
    def process_text(self, file_path):
        char_freq = {}
        with open(file_path, 'r') as file:
            content = file.read()
            for char in content:
                if char in char_freq:
                    char_freq[char] += 1
                else:
                    char_freq[char] = 1
        self.__init__(char_freq)

    def process_image(self, image_path):
        char_freq = {}
        with open(image_path, 'rb') as img_file:
            image_data = img_file.read()
            for byte in image_data:
                if byte in char_freq:
                    char_freq[byte] += 1
                else:
                    char_freq[byte] = 1
        return char_freq
    
    def process_video(self, video_path):
        char_freq = {}
        with open(video_path, 'rb') as video_file:
            video_data = video_file.read()
            for byte in video_data:
                if byte in char_freq:
                    char_freq[byte] += 1
                else:
                    char_freq[byte] = 1
        return char_freq
    
    def process_audio(self, audio_path):
        char_freq = {}
        with open(audio_path, 'rb') as audio_file:
            audio_data = audio_file.read()
            for byte in audio_data:
                if byte in char_freq:
                    char_freq[byte] += 1
                else:
                    char_freq[byte] = 1
        return char_freq

    def compress_file(self, input_file, output_file):
        with open(input_file, 'r') as file:
            content = file.read()
        compressed_content = bitarray()
        compressed_content.encode({char: bitarray(code) for char, code in self.huffman_codes.items()}, content)
        with open(output_file, 'wb') as file:
            compressed_content.tofile(file)
    
    def compress_img_file(self, input_file, output_file):
        with open(input_file, 'rb') as file:
            content = file.read()
        compressed_content = bitarray()
        compressed_content.encode({char: bitarray(code) for char, code in self.huffman_codes.items()}, content)
        with open(output_file, 'wb') as file:
            compressed_content.tofile(file)
    
    def compress_video_file(self, input_file, output_file):
        with open(input_file, 'rb') as file:
            content = file.read()
        compressed_content = bitarray()
        compressed_content.encode({byte: bitarray(code) for byte, code in self.huffman_codes.items()}, content)
        with open(output_file, 'wb') as file:
            compressed_content.tofile(file)
    
    def compress_audio_file(self, input_file, output_file):
        with open(input_file, 'rb') as file:
            content = file.read()
        compressed_content = bitarray()
        compressed_content.encode({byte: bitarray(code) for byte, code in self.huffman_codes.items()}, content)
        with open(output_file, 'wb') as file:
            compressed_content.tofile(file)