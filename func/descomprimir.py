import heapq
import pickle
from bitarray import bitarray

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

class HuffmanDecoder:
    def __init__(self, char_freq=None):
        if char_freq is not None:
            self.nodes = [HuffmanNode(char, freq) for char, freq in char_freq.items()]
            heapq.heapify(self.nodes)
            while len(self.nodes) > 1:
                left_node = heapq.heappop(self.nodes)
                right_node = heapq.heappop(self.nodes)
                internal_node = HuffmanNode(None, left_node.freq + right_node.freq)
                internal_node.left = left_node
                internal_node.right = right_node
                heapq.heappush(self.nodes, internal_node)

            self.root = self.nodes[0]
        else:
            self.root = None
            self.huffman_codes = {}
    
    def deserialize_huffman_tree(self, file):
        self.root = pickle.load(file)
    
    def decompress_file(self, input_file, output_file):
        with open(input_file, 'rb') as file:
            compressed_content = bitarray()
            compressed_content.fromfile(file)
        decompressed_content = self.decode_huffman(compressed_content)
        with open(output_file, 'w') as file:
            file.write(decompressed_content)
    
    def decompress_img_file(self, input_file, output_file):
        with open(input_file, 'rb') as file:
            compressed_content = bitarray()
            compressed_content.fromfile(file)
        decompressed_content = self.decode_huffman_img(compressed_content)
        with open(output_file, 'wb') as file:
            file.write(decompressed_content)
    
    def decompress_vid_file(self, input_file, output_file):
        with open(input_file, 'rb') as file:
            compressed_content = bitarray()
            compressed_content.fromfile(file)
        decompressed_content = self.decode_huffman_img(compressed_content)
        with open(output_file, 'wb') as file:
            file.write(decompressed_content)

    def decode_huffman(self, compressed_content):
        current_node = self.root
        decompressed_content = []
        for bit in compressed_content:
            if bit:
                current_node = current_node.right
            else:
                current_node = current_node.left
            if current_node.is_leaf():
                decompressed_content.append(current_node.char)
                current_node = self.root
        return ''.join(decompressed_content)
    
    def decode_huffman_img(self, compressed_content):
        current_node = self.root
        decompressed_content = bytearray()
        for bit in compressed_content:
            if bit:
                current_node = current_node.right
            else:
                current_node = current_node.left
            if current_node.is_leaf():
                decompressed_content.append(current_node.char)
                current_node = self.root
        return bytes(decompressed_content)