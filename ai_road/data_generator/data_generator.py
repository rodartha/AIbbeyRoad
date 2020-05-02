import os
import json
from tqdm import tqdm
import numpy as np

# NOTE: still need to tensorize all of this data

class GenerateData:
    def __init__(self):
        self.directory = '../../data/unstructured/'

        self.full_embeddings = []


    def save_embeddings(self):
        print("Total unique embeddings: {}".format(len(self.full_embeddings)))
        with open('../../data/structured/embeddings.json', 'w') as embedding_file:
            json.dump(self.full_embeddings, embedding_file)


    def load_all_lyrics(self):
        for file in tqdm(os.listdir(self.directory)):
            if file.endswith('.txt'):
                file_path = os.path.join(self.directory, file)
                self.full_embeddings = self.full_embeddings + self.load_file(file_path)

        # Remove duplicate lines from the data:
        # NOTE: may need to remove duplicates where the line is different but content is the same
        self.full_embeddings = list(set(self.full_embeddings))
        print("Finished loading all the embeddings")


    def load_file(self, file_path):
        file_embeddings = []

        with open(file_path, 'r') as text_file:
            full_text = text_file.readlines()

            i = 0
            while i < len(full_text):
                # Remove lines that are just indentation
                if full_text[i][0] == '\n':
                    full_text.pop(i)
                    if i >= len(full_text) - 1:
                        break
                    continue

                file_embeddings = file_embeddings + self.generate_line(i, full_text[i])
                i += 1

        return file_embeddings


    def generate_line(self, line_num, line):
        """
        NOTE: the line number is specified here so that the model has some semblance
        of what line to generate when, may want to remove this later
        """
        prefix = "{} ".format(line_num)
        line_embeddings = []
        for i in range(len(line)):
            embedding = None
            label = None
            if i == 0:
                embedding = prefix
                label = line[i]
            else:
                embedding = prefix + line[0:i]
                label = line[i]
            line_embeddings.append((embedding, label))

        return line_embeddings


    def run(self):
        self.load_all_lyrics()
        self.save_embeddings()


class TensorizeEmbeddings():
    def __init__(self):
        self.full_embeddings = []
        self.load_embeddings()

        self.training_data = [row[0] for row in self.full_embeddings]
        self.training_labels = [row[1] for row in self.full_embeddings]

        # Because the longest line length is 844 and 1024 is the smallest number greater than 844 that is divisible perfectly by 2
        self.MAX_PADDING_LENGTH = 1024

        self.char_to_int = {}
        self.chars_to_ints()

        self.tensorized_training_data = []
        self.tensorized_labels = []


    def load_embeddings(self):
        with open('../../data/structured/embeddings.json') as embedding_file:
            self.full_embeddings = json.load(embedding_file)


    def tensorize_data(self):
        for datum in self.training_data:
            tensor = []
            for char in datum:
                tensor.append(self.char_to_int[char])

            # NOTE: need to decide whether to pad to the front or back of the tensor
            tensor += [0] * (self.MAX_PADDING_LENGTH - len(tensor))
            self.tensorized_training_data.append(tensor)


    def tensorize_labels(self):
        for label in self.training_labels:
            self.tensorized_labels.append(self.char_to_int[label[0]])


    def chars_to_ints(self):
        num_of_chars = {}
        for datum in self.training_data:
            for char in datum:
                if char in num_of_chars.keys():
                    num_of_chars[char] += 1
                else:
                    num_of_chars[char] = 1

        chars_sorted = sorted(num_of_chars.items(), key=operator.itemgetter(1), reverse=True)

        # Save them
        with open('../../data/meta/character_frequency.json', 'w') as freq_file:
            json.dump(chars_sorted, freq_file)

        # Generate mapping from characters to indexes
        index = 1
        for char in chars_sorted:
            self.char_to_int[char] = index
            index += 1

        with open('../../data/meta/num_unique_characters.csv', 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow([index])


    def save_tensorized_training_data(self):
        with open('../../data/structured/training_data.json', 'w') as training_file:
            json.dump(self.tensorized_training_dataed, training_file)


    def save_tensorized_label_data(self):
        with open('../../data/structured/training_labels.json', 'w') as labels_file:
            json.dump(self.tensorized_labels, labels_file)


    def run(self):
        pass



gd = GenerateData()
gd.run()

