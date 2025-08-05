from pathlib import Path
import header
from header import __root__


def rename_directories_with_dots(root: Path) -> None:
    """
    Рекурсивно переименовывает директории: заменяет точки на подчеркивания.
    
    Args:
        root (Path): Корневая директория для поиска.
    """
    for path in sorted(root.rglob("*"), reverse=True):
        if path.is_dir() and '.' in path.name:
            new_name = path.name.replace('.', '_')
            new_path = path.parent / new_name
            if not new_path.exists():
                path.rename(new_path)
                print(f"Renamed: {path} → {new_path}")
            else:
                print(f"Skipped (already exists): {new_path}")

if __name__ == "__main__":
    root_dir = Path('.').resolve()  # Текущая директория
    rename_directories_with_dots(__root__ / 'src' / 'suppliers' / 'suppliers_list')
