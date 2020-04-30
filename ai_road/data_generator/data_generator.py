import os
import json
from tqdm import tqdm

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



gd = GenerateData()
gd.run()

