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
        # insert comment

        $query = "INSERT INTO comments (comment) VALUES (?);";
        getPDO()->prepare($query)->execute([htmlentities($_POST["comment"], ENT_QUOTES | ENT_HTML5, "utf-8")]);
    }

    ?>

    <form action="comments.php" method="POST">
        <label for="comment">Your thoughts: </label>
        <input type="text" name="comment" placeholder="Your Comment">
        <button type="submit">Send</button>
    </form>

    <br>

    <?php # SELECT

    $query = "SELECT * FROM comments;";
    $stmt = getPDO()->prepare($query);

    if ($stmt->execute()) {
        $comments = $stmt->fetchAll();
    }

    for ($i = 0; $i < sizeof($comments); $i++) {
        echo "{$comments[$i]["id"]} - {$comments[$i]["comment"]} <br>";
    }

    ?>
</body>

</html>
