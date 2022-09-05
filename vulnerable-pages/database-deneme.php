<?php
function connect()
{
    $hostname = "localhost";
    $username = "root";
    $password = "";
    $database = "deneme";

    return mysqli_connect($hostname, $username, $password, $database);;
}

function getUsersById($id)
{
    $conn = connect();
    $query = "SELECT * FROM users WHERE id=$id;";
    $result = mysqli_query($conn, $query);
    $users = mysqli_fetch_all($result, MYSQLI_ASSOC);

    return $users;
}
