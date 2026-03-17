<?php
session_start();
$hostname = 'backend-mysql-database';
$username = 'user';
$password = 'supersecretpw';
$database = 'password_manager';
$conn = new mysqli($hostname, $username, $password, $database);
if ($conn->connect_error) { die ('A fatal error occurred.'); }

$vaultId = isset($_GET['vault_id']) ? (int)$_GET['vault_id'] : 0;

// REMEDIATION: SQL Injection (Add Password)
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['addUsername'])) {
    $stmt = $conn->prepare("INSERT INTO vault_passwords (vault_id, username, website, password, notes) VALUES (?, ?, ?, ?, ?)");
    $stmt->bind_param("issss", $_POST['vaultId'], $_POST['addUsername'], $_POST['addWebsite'], $_POST['addPassword'], $_POST['addNotes']);
    $stmt->execute();
    header("Location: vault_details.php?vault_id=" . $_POST['vaultId']);
    exit();
}

// REMEDIATION: SQL Injection (Search Logic)
$searchQuery = $_GET['searchQuery'] ?? "";
if (!empty($searchQuery)) {
    $searchTerm = "%$searchQuery%";
    $stmt = $conn->prepare("SELECT * FROM vault_passwords WHERE vault_id = ? AND (username LIKE ? OR website LIKE ?)");
    $stmt->bind_param("iss", $vaultId, $searchTerm, $searchTerm);
} else {
    $stmt = $conn->prepare("SELECT * FROM vault_passwords WHERE vault_id = ?");
    $stmt->bind_param("i", $vaultId);
}
$stmt->execute();
$resultPasswords = $stmt->get_result();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <title>Vault Details</title>
</head>
<body>
    <div class="container mt-4">
        <h2>Vault Passwords</h2>
        <button type="button" class="btn btn-primary mb-2" data-toggle="modal" data-target="#addPasswordModal">Add Password</button>
        
        <table class="table table-bordered">
            <thead><tr><th>Username</th><th>Notes</th></tr></thead>
            <tbody>
                <?php while ($row = $resultPasswords->fetch_assoc()): ?>
                    <tr>
                        <td><?php echo htmlspecialchars($row['username']); ?></td>
                        <td><?php echo htmlspecialchars($row['notes']); ?></td>
                    </tr>
                <?php endwhile; ?>
            </tbody>
        </table>
    </div>

    <div class="modal" id="addPasswordModal">
        <div class="modal-dialog">
            <div class="modal-content">
                <form method="POST" id="addPasswordForm">
                    <input type="hidden" name="vaultId" value="<?php echo $vaultId; ?>">
                    <div class="modal-body">
                        <input type="text" id="addUsername" name="addUsername" placeholder="Username" class="form-control mb-2">
                        <input type="text" id="addWebsite" name="addWebsite" placeholder="Website" class="form-control mb-2">
                        <input type="password" id="addPassword" name="addPassword" placeholder="Password" class="form-control mb-2">
                        <textarea id="addNotes" name="addNotes" class="form-control"></textarea>
                    </div>
                    <div class="modal-footer"><button type="submit" class="btn btn-primary">Save</button></div>
                </form>
            </div>
        </div>
    </div>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
</body>
</html>