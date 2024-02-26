<?php

class CustomTemplate {
    public $lock_file_path;

    public function __construct($lock_file_path) {
        $this->lock_file_path = $lock_file_path;
    }
}

$newObject = new CustomTemplate("/home/carlos/morale.txt");

$serializedObject = serialize($newObject);

echo $serializedObject;
