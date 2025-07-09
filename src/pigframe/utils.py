from .object import WorldEntities
import json
from typing import Type, Callable
from .base_world import BaseWorld
from .component import Component

# コンポーネントクラス登録用のグローバル辞書
_component_registry = {}

def register_component(component_class: Type[Component]):
    """コンポーネントクラスを登録するためのデコレータまたは関数

    使用例:
    
    # デコレータとして使用
    @register_component
    @dataclass
    class Position(Component):
        x: int
        y: int
        
    # または関数として使用
    register_component(Position)

    Parameters
    ----------
    component_class : Type[Component]
        登録するコンポーネントクラス
        
    Returns
    -------
    Type[Component]
        登録したコンポーネントクラス（デコレータとして使用する場合）
    """
    _component_registry[component_class.__name__] = component_class
    return component_class


def get_registered_component(component_name: str) -> Type[Component]:
    """登録されたコンポーネントクラスを名前で取得する

    Parameters
    ----------
    component_name : str
        コンポーネントの名前

    Returns
    -------
    Type[Component]
        コンポーネントクラス
    
    Raises
    ------
    KeyError
        コンポーネントが登録されていない場合
    """
    if component_name not in _component_registry:
        raise KeyError(f"Component class '{component_name}' is not registered. Use register_component() before loading.")
    return _component_registry[component_name]


def save_game(world_entities: WorldEntities, file_path: str):
    data = []
    for key, items in world_entities.value.items():
        entity_data = {"id": key, "components": {}}
        for component_type, component in items.items():
            component_name = component_type.__name__
            entity_data["components"][component_name] = component.__dict__
        data.append(entity_data)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_game(world: BaseWorld, file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    max_entity_id = 0
    for entity_data in data:
        entity_id = int(entity_data["id"])
        world.create_entity(id=entity_id)
        for component_name, component_data in entity_data["components"].items():
            try:
                # 登録されたコンポーネントクラスを取得
                component_class = get_registered_component(component_name)
                world.add_component_to_entity(entity_id, component_class, **component_data)
            except KeyError as e:
                print(f"Warning: {e}")
        max_entity_id = max(max_entity_id, entity_id)

    # Set the next entity ID to be greater than any existing ID
    world.set_next_entity_id(max_entity_id + 1)
