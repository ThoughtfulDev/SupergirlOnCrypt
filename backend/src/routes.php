<?php
// Routes


$app->get('/', function ($request, $response, $args) {
    return $response->withStatus(501);
});

$app->get('/users', function($request, $response, $args) {

    $sql = "SELECT * FROM users";
    $qry = $this->db->prepare($sql);
    $qry->execute();
    $data = $qry->fetchAll();
    return $response->withStatus(200)
        ->withHeader('Content-type', 'application/json')
        ->withJson($data);
});

$app->post('/users/add', function($request, $response, $args) {
    $json = $request->getParsedBody();
    $uuid = $json['uuid'];
    $priv_key = $json['priv_key'];
    $qry = $this->db->prepare('INSERT INTO users (priv_key, hwid) VALUES (?, ?)');
    if($qry->execute(array($uuid, $priv_key))) {
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
