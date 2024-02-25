<?php

class User {
    public $username;
    public $access_token;

    public function __construct($username, $access_token) {
        $this->username = $username;
        $this->admin = $access_token;
    }
}

if ($argc < 2) {
    die("Usage: php script.php <serialized_object_string>\n");
}

$serializedObject = $argv[1];

$deserializedObject = unserialize($serializedObject);

$deserializedObject->username = "administrator";

$deserializedObject->access_token = 0;

$serializedObjectAfterChange = serialize($deserializedObject);

echo $serializedObjectAfterChange;
