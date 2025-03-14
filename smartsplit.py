#!/usr/bin/env python3
import re

def split_paragraph_into_chunks(paragraph, max_length):
    """
    Given a paragraph (a long string), split it into chunks that are at most max_length.
    The split is done at word boundaries.
    """
    words = paragraph.split()
    chunks = []
    current_chunk = ""
    
    for word in words:
        # If current_chunk is empty, then just assign the word.
        # Otherwise, check if adding a space and the word would exceed max_length.
        if not current_chunk:
            # In case a single word is longer than max_length, you may decide to forcibly split it.
            if len(word) > max_length:
                # Force-split the word (this is optional)
                for i in range(0, len(word), max_length):
                    chunks.append(word[i:i+max_length])
                continue
            else:
                current_chunk = word
        else:
            # Check with a preceding space.
            if len(current_chunk) + 1 + len(word) <= max_length:
                current_chunk += " " + word
            else:
                chunks.append(current_chunk)
                # If the word is itself too long, force-split it (this rarely happens)
                if len(word) > max_length:
                    for i in range(0, len(word), max_length):
                        chunks.append(word[i:i+max_length])
                    current_chunk = ""
                else:
                    current_chunk = word
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def split_text_into_chunks(text, max_length=4096):
    """
    Split a long text into chunks of at most max_length characters.
    The splitting is done by paragraphs when possible (paragraphs are separated by blank lines).
    If a paragraph is too long, it is further split at word boundaries.
    """
    # Split the text using blank lines (one or more newlines with optional whitespace).
    paragraphs = re.split(r'\n\s*\n', text.strip())
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        # Remove leading/trailing whitespace from the paragraph.
        para = para.strip()
        if not para:
            continue
        
        # Decide how to add this paragraph to the current_chunk.
        if current_chunk:
            candidate = current_chunk + "\n\n" + para
        else:
            candidate = para
        
        if len(candidate) <= max_length:
            # Append the paragraph to the current chunk.
            current_chunk = candidate
        else:
            # The candidate would be too long.
            # First, if there is anything in current_chunk, flush it.
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""
            
            # Now check if the paragraph itself is short enough.
            if len(para) <= max_length:
                current_chunk = para
            else:
                # The paragraph is too long on its own; split it at word boundaries.
                subchunks = split_paragraph_into_chunks(para, max_length)
                # Append all subchunks (each subchunk should be <= max_length)
                for sub in subchunks:
                    chunks.append(sub)
                # Start fresh for the next paragraph.
                current_chunk = ""
    
    # Append any remaining text.
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

# Example usage:
if __name__ == '__main__':
    # This is an example string. In real use, your text may be loaded from a file or elsewhere.
    sample_text = (
        "This is a sample paragraph with some words. It should be kept together if possible. "
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus luctus urna sed urna ultricies ac tempor dui sagittis.\n\n"
        "This is another paragraph that might be a bit longer or shorter depending on the content. "
        "Praesent id massa eget neque dignissim fermentum. "
        "Cras tincidunt, sem in condimentum facilisis, metus odio tempor metus, ac ultrices nisi sapien eget orci.\n\n"
        "Yet another paragraph. " * 10  # repeat to simulate a long paragraph
    )

    sample_text = "abcdef" * 1000
    
    chunks = split_text_into_chunks(sample_text, max_length=4096)
    print(f"Total chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {i} (length: {len(chunk)} characters) ---")
        print(chunk)
