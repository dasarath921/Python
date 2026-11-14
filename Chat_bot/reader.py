
from pathlib import Path

def load_policies():
    policy_folder = Path(__file__).parent / "company_policy_files"

    all_policies = ""

    for file_path in policy_folder.glob("*.txt"):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        all_policies += f"\n\n--- {file_path.name} ---\n"
        all_policies += content

    return all_policies
