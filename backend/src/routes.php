<?php
// Routes


$app->get('/', function ($request, $response, $args) {
    return $response->withStatus(501);
});


$app->get('/users/{hwid}', function($request, $response, $args) {
    $hwid = $request->getAttribute('hwid');
    $qry = $this->db->prepare("SELECT * FROM users WHERE hwid = ?");
    $qry->execute(array($hwid));
    $data = $qry->fetchAll();
    return $response->withStatus(200)
        ->withHeader('Content-type', 'application/json')
        ->withJson($data);
});

$app->post('/users/add', function($request, $response, $args) {
    $json = $request->getParsedBody();
    $hwid = $json['hwid'];
    $priv_key = $json['priv_key'];
    $platform = $json['platform'];
    $qry = $this->db->prepare('INSERT INTO users (priv_key, hwid, platform) VALUES (?, ?, ?)');
    if($qry->execute(array($priv_key, $hwid, $platform))) {
        $data['status'] = 'OK';
        return $response->withStatus(200)
            ->withHeader('Content-type', 'application/json')
            ->withJson($data);
    }
    else {
        $data['status'] = 'ERROR';
        $data['error_code'] = 'PDO_EXCEPTION';
        return $response->withStatus(500)
            ->withHeader('Content-type', 'application/json')
            ->withJson($data);
    }

});

$app->get('/decrypt/{hwid}', function($request, $response, $args) {
   $hwid = $request->getAttribute('hwid');
    $qry = $this->db->prepare("SELECT locked, priv_key FROM users WHERE hwid = ?");
    $qry->execute(array($hwid));
    $data = $qry->fetchAll();
    $is_locked = intval($data[0]['locked']);
    if($is_locked == 0) {
        $filename_tmp = md5(uniqid(rand(), true));
        $tmp_data = fopen($filename_tmp, "w");
        fwrite($tmp_data, $data[0]['priv_key']);
        fclose($tmp_data);

        $output = '';
        exec("python ./bin/decrypt_key.py " . $filename_tmp, $output);
        $ret['priv_key'] = $output[0];
        $ret['STATUS'] = "SUCCESS";
        unlink($filename_tmp);
        return $response->withStatus(200)
            ->withHeader('Content-type', 'application/json')
            ->withJson($ret);
    }
    else {
        return $response->withStatus(418)
            ->withJson(array(
               "STATUS" => "FAIL",
               "CODE" => "USER_LOCKED"
            ));
    }


});
