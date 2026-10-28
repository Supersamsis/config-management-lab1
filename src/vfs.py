"""Виртуальная файловая система (VFS)."""
import json
from typing import Any, Dict, Optional


class VFSNode:
    """Узел VFS: файл или директория."""

    def __init__(self, name: str, is_dir: bool = False, content: str = ""):
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.children: Dict[str, "VFSNode"] = {}

    def to_dict(self) -> Dict[str, Any]:
        """Сериализация узла в словарь."""
        result: Dict[str, Any] = {
            "name": self.name,
            "is_dir": self.is_dir,
            "content": self.content,
        }
        if self.is_dir:
            result["children"] = {
                key: value.to_dict() for key, value in self.children.items()
            }
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VFSNode":
        """Десериализация узла из словаря."""
        node = cls(
            name=data["name"],
            is_dir=data.get("is_dir", False),
            content=data.get("content", ""),
        )
        if node.is_dir and "children" in data:
            for key, child_data in data["children"].items():
                node.children[key] = cls.from_dict(child_data)
        return node


class VFS:
    """Виртуальная файловая система в памяти."""

    def __init__(self, root: Optional[VFSNode] = None):
        if root is None:
            self.root = VFSNode("/", is_dir=True)
        else:
            self.root = root
        self.cwd = self.root

    @classmethod
    def from_json(cls, path: str) -> "VFS":
        """Загружает VFS из JSON-файла."""
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        root = VFSNode.from_dict(data)
        return cls(root)

    def to_json(self, path: str) -> None:
        """Сохраняет VFS в JSON-файл."""
        with open(path, "w", encoding="utf-8") as file:
            json.dump(self.root.to_dict(), file, ensure_ascii=False, indent=2)

    def _resolve_step(self, current: VFSNode, part: str) -> Optional[VFSNode]:
        """Обрабатывает один шаг пути."""
        if part == ".":
            return current
        if part == "..":
            return self._parent_of(current)
        if not current.is_dir:
            return None
        return current.children.get(part)

    def get_node(self, path: str) -> Optional[VFSNode]:
        """Возвращает узел по абсолютному или относительному пути."""
        current = self.root if path.startswith("/") else self.cwd
        parts = [part for part in path.split("/") if part]

        for part in parts:
            current = self._resolve_step(current, part)
            if current is None:
                return None
        return current

    def create_dir(self, path: str) -> bool:
        """Создаёт директорию по указанному пути."""
        current = self.root if path.startswith("/") else self.cwd
        parts = [part for part in path.split("/") if part]

        if not parts:
            return False

        for part in parts[:-1]:
            current = self._resolve_step(current, part)
            if current is None or not current.is_dir:
                return False

        new_dir_name = parts[-1]
        if new_dir_name in current.children:
            return False
        current.children[new_dir_name] = VFSNode(new_dir_name, is_dir=True)
        return True

    def _parent_of(self, node: VFSNode) -> VFSNode:
        """Возвращает родительский узел."""
        if node is self.root:
            return self.root
        return self._find_parent(self.root, node) or self.root

    def _find_parent(self, current: VFSNode, target: VFSNode)\
          -> Optional[VFSNode]:
        """Рекурсивно ищет родителя target в дереве."""
        for child in current.children.values():
            if child is target:
                return current
            if child.is_dir:
                found = self._find_parent(child, target)
                if found is not None:
                    return found
        return None