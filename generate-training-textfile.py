import os
import random

#! Change these
wordcount = 150
startnumbers = [5, 4, 7, 8, 9]

#! Script starts here

sourcefolder = r"textfiles"
output_filename = "mytext.txt"

# Initialize an empty list to hold all the words
all_words = []

# Loop through each file in the source folder
for filename in os.listdir(sourcefolder):
    # Check if the file name starts with one of the specified numbers
    if any(filename.startswith(str(num)) for num in startnumbers):
        # Construct the full path to the file
        filepath = os.path.join(sourcefolder, filename)

        # Open the file and read its content
        with open(filepath, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Extract all words from each line
        for line in lines:
            words = line.split()  # Split the line into words based on whitespace
            all_words.extend(words)  # Add the words to the list

# Check the number of words collected
print(f"Total words collected: {len(all_words)}")

# Randomly sample the specified number of words
selected_words = random.sample(all_words, min(wordcount, len(all_words)))

# Combine the selected words into a single line
output_content = " ".join(selected_words)

# Save the result to a new file
output_path = os.path.join(output_filename)
with open(output_path, "w", encoding="utf-8") as output_file:
    output_file.write(output_content)

# Verify the word count in the output file
print(f"Words written to {output_filename}: {len(output_content.split())}")
