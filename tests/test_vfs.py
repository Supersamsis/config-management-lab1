"""Тесты для виртуальной файловой системы."""
import os
import tempfile

from src.vfs import VFS


def test_create_default_vfs():
    """VFS по умолчанию содержит корень."""
    vfs = VFS()
    assert vfs.root.name == "/"
    assert vfs.root.is_dir
    assert vfs.cwd is vfs.root


def test_create_dir():
    """create_dir добавляет новую директорию."""
    vfs = VFS()
    assert vfs.create_dir("test") is True
    assert "test" in vfs.root.children
    assert vfs.root.children["test"].is_dir


def test_create_dir_existing():
    """Повторное создание возвращает False."""
    vfs = VFS()
    vfs.create_dir("test")
    assert vfs.create_dir("test") is False


def test_get_node():
    """get_node находит узел по абсолютному пути."""
    vfs = VFS()
    vfs.create_dir("a")
    node = vfs.get_node("/a")
    assert node is not None
    assert node.name == "a"


def test_get_node_missing():
    """get_node возвращает None для несуществующего пути."""
    vfs = VFS()
    assert vfs.get_node("/nope") is None


def test_json_roundtrip():
    """Сериализация и десериализация сохраняют структуру."""
    vfs = VFS()
    vfs.create_dir("dir1")
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False,
        encoding="utf-8",
    ) as file:
        vfs.to_json(file.name)
        loaded = VFS.from_json(file.name)
    os.unlink(file.name)
    assert loaded.root.name == "/"
    assert "dir1" in loaded.root.children


def test_from_json_example():
    """Загрузка из examples/vfs/minimal.json."""
    path = os.path.join("examples", "vfs", "minimal.json")
    vfs = VFS.from_json(path)
    assert vfs.root.name == "/"
    assert "etc" in vfs.root.children
    assert "home" in vfs.root.children
