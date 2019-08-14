<?php
//url使用base64加密并把+替换为- /替换为_ 删除=
function base64url_encode($data) {
    return rtrim(strtr(base64_encode($data), '+/', '-_'), '=');
}
//替换为base64字符,不足4位补=
function base64url_decode($data) {
    return base64_decode(str_pad(strtr($data, '-_', '+/'), strlen($data) % 4, '=', STR_PAD_RIGHT));
}
#字符替换加密(默认为大小写反转),修改此处顺序和添加数字替换可实现不同密码加密(需和采集caiji.py内密码一致)
function str_decode($str) {
    $find = array('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9');
    $replace = array('@a@', '@b@', '@c@', '@d@', '@e@', '@f@', '@g@', '@h@', '@i@', '@j@', '@k@', '@l@', '@m@', '@n@', '@o@', '@p@', '@q@', '@r@', '@s@', '@t@', '@u@', '@v@', '@w@', '@x@', '@y@', '@z@', '@A@', '@B@', '@C@', '@D@', '@E@', '@F@', '@G@', '@H@', '@I@', '@J@', '@K@', '@L@', '@M@', '@N@', '@O@', '@P@', '@Q@', '@R@', '@S@', '@T@', '@U@', '@V@', '@W@', '@X@', '@Y@', '@Z@', '@0@', '@1@', '@2@', '@3@', '@4@', '@5@', '@6@', '@7@', '@8@', '@9@');
    $find2 = array('@a@', '@b@', '@c@', '@d@', '@e@', '@f@', '@g@', '@h@', '@i@', '@j@', '@k@', '@l@', '@m@', '@n@', '@o@', '@p@', '@q@', '@r@', '@s@', '@t@', '@u@', '@v@', '@w@', '@x@', '@y@', '@z@', '@A@', '@B@', '@C@', '@D@', '@E@', '@F@', '@G@', '@H@', '@I@', '@J@', '@K@', '@L@', '@M@', '@N@', '@O@', '@P@', '@Q@', '@R@', '@S@', '@T@', '@U@', '@V@', '@W@', '@X@', '@Y@', '@Z@');
    $replace2 = array('!A!', '!B!', '!C!', '!D!', '!E!', '!F!', '!G!', '!H!', '!I!', '!J!', '!K!', '!L!', '!M!', '!N!', '!O!', '!P!', '!Q!', '!R!', '!S!', '!T!', '!U!', '!V!', '!W!', '!X!', '!Y!', '!Z!', '!a!', '!b!', '!c!', '!d!', '!e!', '!f!', '!g!', '!h!', '!i!', '!j!', '!k!', '!l!', '!m!', '!n!', '!o!', '!p!', '!q!', '!r!', '!s!', '!t!', '!u!', '!v!', '!w!', '!x!', '!y!', '!z!');
    $str2 = str_replace($find, $replace, $str);
    $find3 = array('@', '!');
    $replace3 = array('', '');
    $str3 = str_replace($find2, $replace2, $str2);
    return str_replace($find3, $replace3, $str3);
}
$geturl = $_GET['url'];
$gettitle = $_GET['title'];
$groups = $_GET['group'];
//strrev()为字符逆序输出
$url = base64url_decode(base64url_decode(strrev(str_decode($geturl))));;
$title = base64url_decode(base64url_decode(strrev(str_decode($gettitle))));;

header("HTTP/1.1 301 Moved Permanently");
header("location:" . $url);
//javascript方法跳转不会传送上级refresh
//echo "<script language='javascript' type='text/javascript'>"; 
//echo "window.location.href='$url'"; 
//echo "</script>"; 

class SQLiteDB extends SQLite3
{
  function __construct()
  {
     $this->open('../log.db');
  }
}
$db = new SQLiteDB();
if(!$db){
  echo $db->lastErrorMsg();
}
$sql =<<<EOF
      CREATE TABLE if not exists log
      (id INTEGER PRIMARY KEY AUTOINCREMENT,
      time      TEXT    NOT NULL,
      groups    TEXT,
      title     TEXT,
      url       TEXT,
      ip        TEXT,
      user_agent    TEXT,
      referer        TEXT);
EOF;

#数据库不存在自动创建，存在则跳过
$ret = $db->exec($sql);
if(!$ret){
  echo $db->lastErrorMsg();
}

$time = date("Y-m-d H:i:s");
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'];//生成短链接时的请求者ip，可参考ip.php中的内容，单机直连或其它CDN可用$_SERVER['HTTP_CLIENT_IP']、$_SERVER['REMOTE_ADDR']、$_SERVER['HTTP_X_FORWARDED_FOR']、$_SERVER['HTTP_X_REAL_IP']、$_SERVER['HTTP_CF_CONNECTING_IP']
if(!$ip) {
	$ip = $_SERVER['REMOTE_ADDR'];
}
$sql =<<<EOF
      INSERT INTO log (id,time,groups,title,url,ip,user_agent,referer)
      VALUES (null, '$time', '$groups', '$title', '$url', '$ip', '$_SERVER[HTTP_USER_AGENT]', '$_SERVER[HTTP_REFERER]');
EOF;
$ret = $db->exec($sql);
$db->close();

?>