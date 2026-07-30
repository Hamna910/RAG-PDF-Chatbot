def chunk_text(text, chunk_size=500):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)

    return chunks


if __name__ == "__main__":
    sample_text = "This is a test document " * 100

    result = chunk_text(sample_text)

    print("Total Chunks:", len(result))
    print(result[0])