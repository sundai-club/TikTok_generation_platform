<?php

function adminer_object() {
  class AdminerSoftware extends Adminer {
    function permanentLogin($i = false) {
      return 'x';
    }
  }
  return new AdminerSoftware;
}

if (empty($_COOKIE['adminer_permanent'])) {
  $_POST['auth'] = [
    'driver'    => 'pgsql',
    'server'    => '127.0.0.1',
    'username'  => 'postgres',
    'password'  => 'postgres',
    'db'        => 'app',
    'permanent' => 1,
  ];
}

$_GET['pgsql'] = '127.0.0.1';
$_GET['username'] = 'postgres';
$_GET['db'] = 'app';

include '/opt/adminer.php';
