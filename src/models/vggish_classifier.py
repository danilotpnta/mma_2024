import torch.nn as nn
from torch.hub import load

class VGGishModel(nn.Module):
    def __init__(self):
        super(VGGishModel, self).__init__()
        self.model = load('harritaylor/torchvggish', 'vggish')

    def forward(self, x):
        return self.model(x)

    def encode_audio(self, audio_path):
        return self.model.forward(audio_path)