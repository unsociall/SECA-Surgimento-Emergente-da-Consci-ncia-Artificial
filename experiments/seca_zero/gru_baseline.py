"""SECA-Zero: GRU experimental, initialized from scratch.

No pretrained weights, language data, network calls, or third-party source imports.
This module defines the model only. Importing requires PyTorch; no experiment
is executed by this file.
"""
from __future__ import annotations

import torch
from torch import nn


class SECAZeroGRU(nn.Module):
    """Predict the next nonlinguistic sensory vector and action values.

    Input shape: (batch, sequence, sensory_dim).
    The recurrent state may be carried between chunks by the experiment runner.
    """

    def __init__(
        self,
        sensory_dim: int,
        action_dim: int,
        hidden_dim: int = 64,
        num_layers: int = 1,
    ) -> None:
        super().__init__()
        if min(sensory_dim, action_dim, hidden_dim, num_layers) <= 0:
            raise ValueError("All dimensions must be positive.")
        self.sensory_dim = sensory_dim
        self.action_dim = action_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.encoder = nn.Linear(sensory_dim, hidden_dim)
        self.recurrent = nn.GRU(
            input_size=hidden_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
        )
        self.prediction_head = nn.Linear(hidden_dim, sensory_dim)
        self.action_head = nn.Linear(hidden_dim, action_dim)
        self.reset_parameters()

    def reset_parameters(self) -> None:
        """Create new random parameters; never load an external checkpoint."""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.xavier_uniform_(module.weight)
                nn.init.zeros_(module.bias)
            elif isinstance(module, nn.GRU):
                for name, parameter in module.named_parameters():
                    if "weight_ih" in name:
                        nn.init.xavier_uniform_(parameter)
                    elif "weight_hh" in name:
                        nn.init.orthogonal_(parameter)
                    elif "bias" in name:
                        nn.init.zeros_(parameter)

    def initial_state(self, batch_size: int, *, device=None, dtype=None) -> torch.Tensor:
        if batch_size <= 0:
            raise ValueError("batch_size must be positive")
        ref = next(self.parameters())
        return torch.zeros(
            self.num_layers, batch_size, self.hidden_dim,
            device=device if device is not None else ref.device,
            dtype=dtype if dtype is not None else ref.dtype,
        )

    def forward(
        self,
        sensory_sequence: torch.Tensor,
        state: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        if sensory_sequence.ndim != 3 or sensory_sequence.shape[-1] != self.sensory_dim:
            raise ValueError("Expected [batch, time, sensory_dim] input")
        if sensory_sequence.shape[1] == 0:
            raise ValueError("Sequence must contain at least one timestep")
        encoded = torch.tanh(self.encoder(sensory_sequence))
        outputs, next_state = self.recurrent(encoded, state)
        next_sensory_prediction = self.prediction_head(outputs)
        action_values = self.action_head(outputs)
        return next_sensory_prediction, action_values, next_state
