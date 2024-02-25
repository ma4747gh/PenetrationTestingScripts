<?php

class User {
    public $username;
    public $admin;

    public function __construct($username, $admin) {
        $this->username = $username;
        $this->admin = $admin;
    }
}

if ($argc < 2) {
    die("Usage: php script.php <serialized_object_string>\n");
}

$serializedObject = $argv[1];

$deserializedObject = unserialize($serializedObject);

$deserializedObject->admin = true;

$serializedObjectAfterChange = serialize($deserializedObject);

echo $serializedObjectAfterChange;
