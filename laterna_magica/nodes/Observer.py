from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from laterna_magica.nodes import ObservableOutput


class Observer:

    def notify(self, cause: 'ObservableOutput', data: Any):
        pass
