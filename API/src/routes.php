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
        exec("python3 ../bin/decrypt_key.py " . $filename_tmp, $output);
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

$app->post('/answer/{hwid}', function($request, $response, $args) {
    
    $hwid = $request->getAttribute('hwid');
    $json_req = $request->getParsedBody();
    $json_req = array_values($json_req);
    $str = file_get_contents('../bin/questions.json');
    $questions = json_decode($str, true);
    $questions = array_values($questions[0]);
    if (count($json_req) != count($questions)) {
        return $response->withStatus(200)
        ->withHeader('Content-type', 'application/json')
        ->withJson(array(
            "STATUS" => "MALFORMED"
        ));
    } else {
        $err = false;
        for($i = 0; $i < count($json_req); $i++) {
            if($json_req[$i] != $questions[$i]) {
                $err = true;
            }
        }
        $ret['STATUS'] = 'OK';
        if($err) {
            $ret['STATUS'] = 'WRONG_ANSWERS';
        } else {
            $qry = $this->db->prepare("UPDATE users SET locked=0 WHERE hwid = ?");
            $qry->execute(array($hwid));
        }
        return $response->withStatus(200)
            ->withHeader('Content-type', 'application/json')
            ->withJson($ret);
    }
 
 });
