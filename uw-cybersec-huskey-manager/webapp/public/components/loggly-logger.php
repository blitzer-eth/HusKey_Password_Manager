<?php

require __DIR__ . '/../../vendor/autoload.php';

use Monolog\Logger;
use Monolog\Handler\LogglyHandler;
use Monolog\Formatter\LogglyFormatter;
use Monolog\Handler\BufferHandler;

$logglyToken = $_ENV["LOGGLY_TOKEN"];

$logger = new Logger('UW HusKey Manager');

$logglyHandler = new LogglyHandler($logglyToken.'/tag/monolog', Logger::INFO);
$logger->pushHandler(new BufferHandler($logglyHandler));

$logger->info('Loggly Sending Informational Message');
?>