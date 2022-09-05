<?php include 'database-deneme.php'; ?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>comment.php</title>
</head>

<body>

    <?php # Insert

    if (isset($_POST["comment"])) {
        $conn = connect();
        $insert_query = "INSERT INTO comments(comment) VALUES (\"{$_POST['comment']}\")";
        # a"); DROP TABLE comments;";#
        mysqli_multi_query($conn, $insert_query);
        mysqli_close($conn);
    }

    ?>

    <form action="comment.php" method="POST">
        <label for="comment">Your thoughts: </label>
        <input type="text" name="comment" placeholder="Your Comment">
        <button type="submit">Send</button>
    </form>

    <br>

    <?php # SELECT

    $conn = connect();
    $query = "SELECT * FROM comments";
    $result = mysqli_query($conn, $query);
    $comments = mysqli_fetch_all($result, MYSQLI_ASSOC);

    for ($i = 0; $i < sizeof($comments); $i++) {
        echo "{$comments[$i]["id"]} - {$comments[$i]["comment"]} <br>";
    }

    mysqli_close($conn);

    ?>
</body>

</html>