import torch
from torch import nn
import torch.nn.functional as F

class BeatlesNet(nn.Module):

    __inti__(self, device=None):
        super().__init__()

        # Set device to run model on
        if device:
            self.device = device
        else:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # FIXME: load from '../../data/meta/num_unique_characters.csv'
        self.NUM_EMBEDDINGS = FIXME

        self.EMBEDDING_DIM = 16

        # Define network:
        self.embedding_layer = Embedding(self.NUM_EMBEDDINGS, self.EMBEDDING_DIM)


    def forward(self, x):
        z = self.embedding_layer(x)
        
        return z
