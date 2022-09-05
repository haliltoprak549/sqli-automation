<?php

function getPDO()
{
    return new PDO('mysql:host=127.0.0.1:3306;dbname=deneme', 'root', '');
}
