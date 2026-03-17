<?php
if (isset($_GET['file'])) {
    // REMEDIATION: basename() strips out all path sequences like ../
    $fileName = basename($_GET['file']);
    $uploadDir = './uploads/'; 
    $filePath = $uploadDir . $fileName;

    // Check if file exists and is a real file
    if (file_exists($filePath) && is_file($filePath)) {
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="' . $fileName . '"');
        readfile($filePath);
        exit;
    } else {
        // Return a 403 error so the test sees the block
        http_response_code(403);
        die('Access Denied: Path traversal attempt blocked.');
    }
}
?>