<?php
session_start();

// Part 2: Including the logger component
include './components/loggly-logger.php';

$hostname = 'backend-mysql-database';
$username = 'user';
$password = 'supersecretpw';
$database = 'password_manager';

$conn = new mysqli($hostname, $username, $password, $database);

if ($conn->connect_error) {
    if (isset($logger)) {
        $logger->error("Database connection failed: " . $conn->connect_error);
    }
    die("Connection failed: " . $conn->connect_error);
}

unset($error_message);

// EXTRA CREDIT: BRUTE FORCE PROTECTION
$max_attempts = 5;
if (!isset($_SESSION['login_attempts'])) {
    $_SESSION['login_attempts'] = 0;
}

if ($_SESSION['login_attempts'] >= $max_attempts) {
    $error_message = "This account is temporarily locked due to too many failed login attempts.";
    $logger->error("Ongoing blocked access attempt from IP: " . $_SERVER['REMOTE_ADDR']);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && $_SESSION['login_attempts'] < $max_attempts) {
    
    $username = $_POST['username'];
    $password = $_POST['password'];

    // ============== START SQLi REMEDIATION ==============
    // Use Prepared Statements to fetch user (prevents SQLi)
    $stmt = $conn->prepare("SELECT * FROM users WHERE username = ? AND approved = 1");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();
    // ============== END SQLi REMEDIATION ==============

    if($result->num_rows > 0) {
        $userFromDB = $result->fetch_assoc();

        // ============== START SALTING VERIFICATION ==============
        // Securely verify the password against the salted hash
        if (password_verify($password, $userFromDB['password'])) {
            // ============== END SALTING VERIFICATION ==============
            $_SESSION['login_attempts'] = 0; // Reset counter
            $logger->info("Successful login for user: $username");

            $_SESSION['authenticated'] = $username;     

            if ($userFromDB['default_role_id'] == 1) {        
                $_SESSION['isSiteAdministrator'] = 1;                
            } else {
                unset($_SESSION['isSiteAdministrator']); 
            }
            header("Location: index.php");
            exit();
        }
    }

    // Login Failed logic below
    $_SESSION['login_attempts']++;
    $remaining = $max_attempts - $_SESSION['login_attempts'];

    if ($_SESSION['login_attempts'] >= $max_attempts) {
        $error_message = "Too many failed attempts. You are now locked out.";
        $logger->critical("BRUTE FORCE DETECTED: 5 consecutive failures for username: $username");
    } else {
        $error_message = "Invalid username or password. You have $remaining attempts left.";
        $logger->warning("Login failed for username: $username");
    }
    
    $stmt->close();
}
$conn->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <title>Login Page</title>
</head>
<body>
    <div class="container mt-5">
        <div class="col-md-6 offset-md-3">
            <h2 class="text-center">Login</h2>
            <?php if (isset($error_message)) : ?>
                <div class="alert alert-danger" role="alert">
                    <?php echo $error_message; ?>
                </div>
            <?php endif; ?>
            
            <?php if ($_SESSION['login_attempts'] < $max_attempts) : ?>
            <form action="login.php" method="post">
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" class="form-control" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" class="form-control" id="password" name="password" required>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Login</button>
            </form>
            <?php endif; ?>

            <div class="mt-3 text-center">
                <a href="./users/request_account.php" class="btn btn-secondary btn-block">Request an Account</a>
            </div>
        </div>
    </div>
</body>
</html>