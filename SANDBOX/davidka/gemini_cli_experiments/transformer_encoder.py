

import torch
import torch.nn as nn
import torch.nn.functional as F
import math

class MultiHeadSelfAttention(nn.Module):
    def __init__(self, embed_dim, num_heads, dropout=0.1):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        assert self.head_dim * num_heads == self.embed_dim, "embed_dim must be divisible by num_heads"

        self.q_linear = nn.Linear(embed_dim, embed_dim)
        self.k_linear = nn.Linear(embed_dim, embed_dim)
        self.v_linear = nn.Linear(embed_dim, embed_dim)
        self.out_linear = nn.Linear(embed_dim, embed_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)

        # 1. Linear projections (Q, K, V)
        Q = self.q_linear(query).view(batch_size, -1, self.num_heads, self.head_dim).transpose(1, 2)
        K = self.k_linear(key).view(batch_size, -1, self.num_heads, self.head_dim).transpose(1, 2)
        V = self.v_linear(value).view(batch_size, -1, self.num_heads, self.head_dim).transpose(1, 2)

        # 2. Scaled Dot-Product Attention
        # (batch_size, num_heads, seq_len, head_dim) @ (batch_size, num_heads, head_dim, seq_len) -> (batch_size, num_heads, seq_len, seq_len)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.head_dim)

        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9) # Apply mask

        attention_weights = F.softmax(scores, dim=-1)
        attention_weights = self.dropout(attention_weights)

        # (batch_size, num_heads, seq_len, seq_len) @ (batch_size, num_heads, seq_len, head_dim) -> (batch_size, num_heads, seq_len, head_dim)
        context = torch.matmul(attention_weights, V)

        # Concatenate heads and put through final linear layer
        context = context.transpose(1, 2).contiguous().view(batch_size, -1, self.embed_dim)
        output = self.out_linear(context)
        return output, attention_weights

class FeedForwardNetwork(nn.Module):
    def __init__(self, embed_dim, ff_dim, dropout=0.1):
        super().__init__()
        self.linear1 = nn.Linear(embed_dim, ff_dim)
        self.dropout = nn.Dropout(dropout)
        self.linear2 = nn.Linear(ff_dim, embed_dim)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.dropout(x)
        x = self.linear2(x)
        return x

class EncoderLayer(nn.Module):
    def __init__(self, embed_dim, num_heads, ff_dim, dropout=0.1):
        super().__init__()
        self.self_attn = MultiHeadSelfAttention(embed_dim, num_heads, dropout)
        self.feed_forward = FeedForwardNetwork(embed_dim, ff_dim, dropout)
        self.norm1 = nn.LayerNorm(embed_dim)
        self.norm2 = nn.LayerNorm(embed_dim)
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)

    def forward(self, src, src_mask=None):
        # Self-attention block
        attn_output, _ = self.self_attn(src, src, src, mask=src_mask)
        src = src + self.dropout1(attn_output) # Add & Norm
        src = self.norm1(src)

        # Feed-forward block
        ff_output = self.feed_forward(src)
        src = src + self.dropout2(ff_output) # Add & Norm
        src = self.norm2(src)
        return src

class PositionalEncoding(nn.Module):
    def __init__(self, embed_dim, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, embed_dim)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, embed_dim, 2).float() * (-math.log(10000.0) / embed_dim))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0) # Add batch dimension
        self.register_buffer('pe', pe)

    def forward(self, x):
        # x is (batch_size, seq_len, embed_dim)
        # pe is (1, max_len, embed_dim)
        x = x + self.pe[:, :x.size(1)]
        return x

class TokenEmbedding(nn.Module):
    def __init__(self, vocab_size, embed_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.embed_dim = embed_dim

    def forward(self, tokens):
        return self.embedding(tokens) * math.sqrt(self.embed_dim) # Scale embeddings

class Encoder(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_heads, ff_dim, num_layers, dropout=0.1, max_len=5000):
        super().__init__()
        self.token_embedding = TokenEmbedding(vocab_size, embed_dim)
        self.positional_encoding = PositionalEncoding(embed_dim, max_len)
        self.dropout = nn.Dropout(dropout)
        self.layers = nn.ModuleList([
            EncoderLayer(embed_dim, num_heads, ff_dim, dropout)
            for _ in range(num_layers)
        ])
        self.norm = nn.LayerNorm(embed_dim) # Final normalization

    def forward(self, src, src_mask=None):
        # src is (batch_size, seq_len)
        src = self.token_embedding(src) # (batch_size, seq_len, embed_dim)
        src = self.positional_encoding(src)
        src = self.dropout(src)

        for layer in self.layers:
            src = layer(src, src_mask)

        src = self.norm(src) # Apply final normalization
        return src

# Example Usage:
if __name__ == "__main__":
    # Hyperparameters
    vocab_size = 10000
    embed_dim = 512
    num_heads = 8
    ff_dim = 2048
    num_layers = 6
    dropout = 0.1
    max_seq_len = 100
    batch_size = 2

    # Create a dummy input
    # Batch of sequences, each sequence has max_seq_len tokens
    dummy_input = torch.randint(0, vocab_size, (batch_size, max_seq_len))

    # Create a dummy mask (e.g., for padding)
    # 1 for actual tokens, 0 for padding
    # For self-attention, mask should be (batch_size, 1, seq_len, seq_len) or (batch_size, seq_len, seq_len)
    # Here, we'll create a simple causal mask for demonstration, though encoder typically doesn't use it.
    # For a typical encoder, you'd mask padding tokens.
    # Let's assume no padding for simplicity in this example, so no mask needed for now.
    # If you had padding, you'd create a mask like:
    # src_key_padding_mask = (dummy_input == PAD_IDX).unsqueeze(1).unsqueeze(2)
    # This mask would be (batch_size, 1, 1, seq_len) and broadcast.
    # For a full self-attention mask, it would be (batch_size, 1, seq_len, seq_len)
    # where 0s indicate positions to be masked.

    # Initialize the Encoder
    encoder = Encoder(vocab_size, embed_dim, num_heads, ff_dim, num_layers, dropout, max_len=max_seq_len)

    # Forward pass
    print(f"Input shape: {dummy_input.shape}")
    output = encoder(dummy_input)
    print(f"Output shape: {output.shape}")

    # Verify output shape
    expected_output_shape = (batch_size, max_seq_len, embed_dim)
    assert output.shape == expected_output_shape, \
        f"Expected output shape {expected_output_shape}, but got {output.shape}"
    print("Encoder output shape is correct!")

    # Test with a simple mask (e.g., for padding)
    # Let's say token 0 is padding
    PAD_IDX = 0
    dummy_input_with_padding = torch.randint(1, vocab_size, (batch_size, max_seq_len))
    # Introduce some padding
    dummy_input_with_padding[0, 50:] = PAD_IDX
    dummy_input_with_padding[1, 70:] = PAD_IDX

    # Create a padding mask: True where token is NOT padding, False where it IS padding
    # For attention, we want to mask out (set to -inf) the padded positions.
    # So, mask should be 0 where we want to mask, 1 otherwise.
    # (batch_size, 1, 1, seq_len) for key_padding_mask
    src_key_padding_mask = (dummy_input_with_padding == PAD_IDX).unsqueeze(1).unsqueeze(2)
    # This mask will be broadcast to (batch_size, num_heads, seq_len, seq_len)
    # where the last dimension corresponds to the keys.

    print(f"\nInput shape with padding: {dummy_input_with_padding.shape}")
    print(f"Padding mask shape: {src_key_padding_mask.shape}")
    output_with_padding = encoder(dummy_input_with_padding, src_mask=src_key_padding_mask)
    print(f"Output shape with padding: {output_with_padding.shape}")
    assert output_with_padding.shape == expected_output_shape, \
        f"Expected output shape {expected_output_shape}, but got {output_with_padding.shape} with padding"
    print("Encoder with padding mask output shape is correct!")

