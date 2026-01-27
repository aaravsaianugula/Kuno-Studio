import torch
import torchtune.models.llama3_2 as llama

print("Instantiating Llama 3.2 3B...")
# Use the same config as heartmula if possible, or default
model = llama.llama3_2(
        vocab_size=128_256,
        num_layers=1, # 1 layer enough
        num_heads=24,
        num_kv_heads=8,
        embed_dim=3072,
        max_seq_len=2048,
        intermediate_dim=8192,
        attn_dropout=0.0,
        norm_eps=1e-5,
        rope_base=500_000,
        scale_factor=32,
    )

layer = model.layers[0]
print("\n=== Layer Attributes ===")
print(layer.__dict__.keys())

print("\n=== Attention Attributes ===")
print(layer.attn.__dict__.keys())

if hasattr(layer.attn, 'pos_embeddings'):
    print("\n[!] Found pos_embeddings in attn")
    print(layer.attn.pos_embeddings)
    
if hasattr(layer.attn, 'rope'):
    print("\n[!] Found rope in attn")

if hasattr(layer.attn, 'rotary_emb'):
    print("\n[!] Found rotary_emb in attn")

# Check for buffers
print("\n=== Attn Buffers ===")
for name, buf in layer.attn.named_buffers():
    print(name)
    
print("\n=== Attn Parameters ===")
for name, param in layer.attn.named_parameters():
    print(name)
