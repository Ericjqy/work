import bitio
import huffman
import pickle


def read_tree(tree_stream):
    '''Read a description of a Huffman tree from the given compressed
    tree stream, and use the pickle module to construct the tree object.
    Then, return the root node of the tree itself.

    Args:
      tree_stream: The compressed stream to read the tree from.

    Returns:
      A Huffman tree root constructed according to the given description.
    '''
    tree = pickle.load(tree_stream)
    return(tree)


def decode_byte(tree, bitreader):
    """
    Reads bits from the bit reader and traverses the tree from
    the root to a leaf. Once a leaf is reached, bits are no longer read
    and the value of that leaf is returned.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.
      tree: A Huffman tree.

    Returns:
      Next byte of the compressed bit stream.
    """
    while (isinstance(tree, huffman.TreeLeaf) is False):
        bit = bitreader.readbit()
        if bit == 0:
            tree = tree.getLeft()
        else:
            tree = tree.getRight()
    return tree.getValue()


def decompress(compressed, uncompressed):
    '''First, read a Huffman tree from the 'compressed' stream using your
    read_tree function. Then use that tree to decode the rest of the
    stream and write the resulting symbols to the 'uncompressed'
    stream.

    Args:
      compressed: A file stream from which compressed input is read.
      uncompressed: A writable file stream to which the uncompressed
          output is written.
    '''
    tree = read_tree(compressed)
    mybitReader = bitio.BitReader(compressed)
    mybitWriter = bitio.BitWriter(uncompressed)
    end_of_file = False
    while end_of_file is False:
        try:
            nextByte = decode_byte(tree, mybitReader)
            # EOF read, break the program
            if nextByte is None:
                break
            mybitWriter.writebits(nextByte, 8)
        except EOFError:
            end_of_file = True
    mybitWriter.flush()


def write_tree(tree, tree_stream):
    '''Write the specified Huffman tree to the given tree_stream
    using pickle.

    Args:
      tree: A Huffman tree.
      tree_stream: The binary file to write the tree to.
    '''
    pickle.dump(tree, tree_stream)
    return


def compress(tree, uncompressed, compressed):
    '''First write the given tree to the stream 'compressed' using the
    write_tree function. Then use the same tree to encode the data
    from the input stream 'uncompressed' and write it to 'compressed'.
    If there are any partially-written bytes remaining at the end,
    write 0 bits to form a complete byte.

    Flush the bitwriter after writing the entire compressed file.

    Args:
      tree: A Huffman tree.
      uncompressed: A file stream from which you can read the input.
      compressed: A file stream that will receive the tree description
          and the coded input data.
    '''
    write_tree(tree, compressed)
    mybitReader = bitio.BitReader(uncompressed)
    mybitwriter = bitio.BitWriter(compressed)
    # encodingTable will return a dictionary indicate each treeleaf
    # and its path
    encodingTable = huffman.make_encoding_table(tree)
    end_of_stream = False
    while not end_of_stream:
        try:
            output = mybitReader.readbits(8)
            for i in encodingTable[output]:
                mybitwriter.writebit(i)
        except EOFError:
            for j in encodingTable[None]:
                mybitwriter.writebit(j)
            end_of_stream = True
    mybitwriter.flush()
