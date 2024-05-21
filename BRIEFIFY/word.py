def total_word_count_from_file(file_path):
    # Initialize total word count
    total_words = 0
    
    # Read the file with UTF-8 encoding
    with open(file_path, 'r', encoding='utf-8') as file:
        # Iterate through each line in the file
        for line in file:
            # Split each line into words
            words = line.split()
            # Update total word count
            total_words += len(words)
    
    return total_words

def main():
    file_path = input("Enter the file path: ")
    total_words = total_word_count_from_file(file_path)
    print(f'Total words in the file: {total_words}')

if __name__ == "__main__":
    main()
