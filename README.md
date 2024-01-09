# `compresor_archivos` Project

## Author

This project was developed by:
- [@Kurisari](https://www.github.com/kurisari)

## Project Overview

The `compresor_archivos` project is a file compression and decompression tool implemented in Python. The project includes three main files: `main.py`, `comprimir.py`, and `descomprimir.py`. The application utilizes the Huffman coding algorithm for text, image, video, and audio file compression.

## Files

### `main.py`

This file contains the main application code, which uses the Tkinter library for the graphical user interface (GUI). The application allows users to select a file for compression or decompression and provides options for different file types. It supports compression and decompression of text, image, video, and audio files using the Huffman coding algorithm.

### `comprimir.py`

This file includes the implementation of the file compression functionality. It defines a `HuffmanTree` class, which is used for Huffman coding. Additionally, there is a `ColorQuantization` class for quantizing colors in video files. Currently, the LZW compression code is commented out, and it can be uncommented if needed, but it is not functional yet.

### `descomprimir.py`

This file contains the implementation of the file decompression functionality. It defines a `HuffmanDecoder` class, which is responsible for decoding Huffman-coded files. The `descomprimir.py` file mirrors the structure of `comprimir.py` and is designed to work with the corresponding compression logic.

## Usage

To run the application, execute the `main.py` file. This will launch the graphical user interface where you can select files for compression or decompression.

**Note:** Make sure to install the necessary Python packages before running the application. You can install the required packages using the following command:

```bash
pip install bitarray opencv-python numpy
```

## Supported File Types

The application supports the compression of the following file types:

- Text files: `.txt`
- Image files: `.png`, `.jpg`, `.jpeg`
- Video files: `.mp4`, `.avi`, `.mkv`
- Audio files: `.mp3`, `.wav`, `.ogg`

The aplication supports the descompression of the following file types:

- Text files: `.crtxt`
- Image files: `.crpng`, `.crjpg`, `.crjpeg`
- Video files: `.crmp4`, `.cravi`, `.crmkv`
- Audio files: `.crmp3`, `.crwav`, `.crogg`

The output file extensions are derived from the first two letters of my name, Cristian.

## Compression Algorithm

The Huffman coding algorithm is used for file compression. It generates Huffman codes based on the frequency of characters in the input file, creating an optimal prefix-free binary tree.

## Decompression

The decompression process involves decoding the compressed file using the Huffman codes generated during compression. The application supports the decompression of text, image, video, and audio files.