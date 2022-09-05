<?php session_start(); ?>
<?php include 'database-deneme.php'; ?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>login.php</title>
</head>

<body>

    <?php
    # Eger kullanici giris yapmissa login sayfasina ulasmasina izin verme
    if (isset($_SESSION['user_id'])) {
        header("Location: home.php");
    }
    ?>

    <p>Login</p>

    <form action="login.php" method="POST">
        <input type="text" name="username" placeholder="Username">
        <br><br>
        <input type="password" name="password" placeholder="Password">
        <br><br>
        <button type="submit">Login</button>
    </form>

    <?php

    if (isset($_POST["username"])) {
        # login butonuna basildi
        $stmt = getPDO()->prepare('SELECT * FROM users WHERE username = ? AND password = ?');
        if ($stmt->execute([$_POST['username'], $_POST['password']])) {

            $users = $stmt->fetchAll();

            if (sizeof($users) == 1) {
                # girilen bilgiler dogru
                $_SESSION['user_id'] = $users[0]['id'];
                $_SESSION['username'] = $users[0]['username'];
                $_SESSION['password'] = $users[0]['password'];
                header("Location: home.php");
            } else {
                # girilen bilgiler yanlis
                echo "<br> Giris bilgileri hatali!";
            }
        } else {
            # sorgu calistirilamadi
            echo "Hata meydana geldi!";
        }
    }
    ?>
</body>

</html>