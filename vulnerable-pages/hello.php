<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>hello.php</title>
</head>

<body>
    <form action="hello.php" method="post">
        <label for="name">Name: </label>
        <input type="text" name="name" placeholder="Your Name">
        <button type="submit" name="submit">Say My Name</button>
    </form>

    <?php
    if (isset($_POST["name"])) {
        echo "<br>";
        echo "Hello " . $_POST["name"];
        # <script>alert(1)</script>
    }
    ?>
</body>

</html>
