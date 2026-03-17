import pytest
import mysql.connector

def test_verify_unique_salts():
    """
    PROOFS: Even with identical passwords, the database stores unique hashes.
    This proves salt is unique per user (remediating Rainbow Table risks).
    """
    # Connect using credentials that match your init.sql and docker setup
    db = mysql.connector.connect(
        host="localhost",           # Use "127.0.0.1" if localhost fails
        user="user",                # Matches init.sql
        password="supersecretpw",   # Matches init.sql
        database="password_manager" # Matches init.sql
    )
    cursor = db.cursor(dictionary=True)

    try:
        # Fetch the users created during your Selenium IDE tests
        # We use these specific names because they are in your recorded scripts
        usernames = ('alex_test_final', 'alex_final_demo_01')
        query = "SELECT username, password FROM users WHERE username IN (%s, %s)"
        cursor.execute(query, usernames)
        rows = cursor.fetchall()

        # Ensure we found exactly two users to compare
        assert len(rows) == 2, f"Test failed: Found {len(rows)} users, but expected 2. Did you clear your DB?"

        # Extract the hashes
        hash_1 = rows[0]['password']
        hash_2 = rows[1]['password']

        # THE CRITICAL ASSERTIONS:
        
        # 1. Verify it's using bcrypt (indicated by $2y$ or $2a$ in PHP/Blowfish)
        # This proves the plain-text 'alexpassword' was successfully hashed
        assert hash_1.startswith("$2y$"), f"FAILED: {rows[0]['username']} has an insecure password format!"
        assert hash_2.startswith("$2y$"), f"FAILED: {rows[1]['username']} has an insecure password format!"

        # 2. Verify Salting: Even with identical 'alexpassword' inputs, hashes MUST be different
        # This protects against Rainbow Table and collision attacks
        assert hash_1 != hash_2, "FAILED: Both users have the same hash! Salting is NOT unique."
        
        print("\n[SUCCESS] Unique salts verified for both test users.")

    finally:
        cursor.close()
        db.close()