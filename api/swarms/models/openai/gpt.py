from ..base_model import BaseSwarmModel


class GPT4(BaseSwarmModel):
    def __init__(self, version) -> None:
        super().__init__()
        self.version = version
