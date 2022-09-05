<?php session_start(); ?>
<?php include 'database-deneme.php'; ?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>home.php</title>
</head>

<body>

    <?php
    if (!isset($_SESSION['user_id'])) {
        # giris yapilmamis
        header("Location: login.php");
    } else {
        # giris yapilmis
        echo "<h1> Welcome " . $_SESSION['username'];
        echo "
        <form action='home.php' method='POST'>
            <input type='hidden' name='logout'>
            <button type='submit'>Log out</button>
        </form>
        ";

        if (isset($_POST['logout'])) {
            session_destroy();
            header("Location: login.php");
        }
    }
    ?>

</body>

</html>