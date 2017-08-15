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
    $qry = $this->db->prepare('INSERT INTO users (priv_key, hwid) VALUES (?, ?)');
    if($qry->execute(array($priv_key, $hwid))) {
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
    $qry = $this->db->prepare("SELECT locked FROM users WHERE hwid = ?");
    $qry->execute(array($hwid));
    $data = $qry->fetchAll();
    $is_locked = intval($data[0]['locked']);
    $ret['priv_key'] = 'ENCRPYTED';
    if($is_locked == 0) {
        echo 'DO SOME DECPRYTION NOW';
        $ret['priv_key'] = 'Decrypted now';
    }

    return $response->withStatus(200)
        ->withHeader('Content-type', 'application/json')
        ->withJson($ret);
});
