# %%
import torch

print(torch.__version__)

# %%
print("Hello World")

# %%
X = torch.tensor([1, 2, 3, 4], dtype=torch.float32, requires_grad=True)
y = X**2 + 5

print(y)

# %%
y.backward()
print(f"Grad is: {X.grad}")
# %%
