import pytest
import requests

def test_prevent_path_traversal():
    # Attack payload: attempt to reach the root directory
    payload = "../../../../../etc/passwd"
    url = f"http://localhost/vaults/download_file.php?file={payload}&vault_id=1"
    
    response = requests.get(url)
    
    # If remediated, the server should not return the passwd file content
    assert "root:" not in response.text, "VULNERABILITY: Path Traversal allowed access to /etc/passwd!"
    assert response.status_code != 200 or "Access Denied" in response.text