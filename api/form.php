<?php
declare(strict_types=1);

ini_set('display_errors', '0');
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

function respond(int $status, string $message, array $extra = []): never
{
    http_response_code($status);
    echo json_encode(['message' => $message] + $extra, JSON_THROW_ON_ERROR);
    exit;
}

$method = $_SERVER['REQUEST_METHOD'] ?? '';
if (!in_array($method, ['GET', 'POST'], true)) {
    header('Allow: GET, POST');
    respond(405, 'This endpoint accepts GET and POST only.');
}

session_name('gla_enquiry');
session_set_cookie_params([
    'lifetime' => 0,
    'path' => '/',
    'secure' => !empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off',
    'httponly' => true,
    'samesite' => 'Strict',
]);
if (!session_start()) {
    error_log('GLA enquiry: could not start session.');
    respond(503, 'The enquiry service is unavailable. Please try again later.');
}

if (!isset($_SESSION['form_token'])) {
    $_SESSION['form_token'] = bin2hex(random_bytes(32));
    $_SESSION['form_token_created'] = time();
}
if ($method === 'GET') {
    if (time() - $_SESSION['form_token_created'] > 3600) {
        $_SESSION['form_token'] = bin2hex(random_bytes(32));
        $_SESSION['form_token_created'] = time();
    }
    respond(200, 'Ready to submit.', ['token' => $_SESSION['form_token']]);
}

$token = $_SERVER['HTTP_X_CSRF_TOKEN'] ?? '';
if (!hash_equals($_SESSION['form_token'], $token)
    || time() - $_SESSION['form_token_created'] > 3600) {
    respond(403, 'Your form session expired. Please submit again.');
}
session_write_close();

if (strtolower(trim(explode(';', $_SERVER['CONTENT_TYPE'] ?? '')[0])) !== 'application/json') {
    respond(415, 'Please submit the form as JSON.');
}
if ((int) ($_SERVER['CONTENT_LENGTH'] ?? 0) > 16384) {
    respond(413, 'The form is too large.');
}
$raw = file_get_contents('php://input', false, null, 0, 16385);
if ($raw === false || strlen($raw) > 16384) {
    respond(413, 'The form is too large.');
}
try {
    $input = json_decode($raw, true, 16, JSON_THROW_ON_ERROR);
} catch (JsonException $exception) {
    respond(400, 'The form data could not be read.');
}
if (!is_array($input) || array_is_list($input)) {
    respond(400, 'The form must contain named fields.');
}

$limits = [
    'submission_id' => 36, 'form_type' => 10, 'name' => 100, 'email' => 254,
    'phone' => 20, 'program' => 20, 'specialization' => 160, 'country' => 100,
    'state' => 100, 'city' => 100, 'company' => 150, 'message' => 3000,
    'source_path' => 500, 'website' => 200,
];
$fields = [];
foreach ($limits as $field => $limit) {
    $value = $input[$field] ?? '';
    if (!is_string($value) || strlen($value) > $limit * 4
        || preg_match('//u', $value) !== 1
        || preg_match('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/', $value)) {
        respond(422, 'A form field is invalid.', ['field' => $field]);
    }
    $length = preg_match_all('/./us', $value);
    if ($length === false || $length > $limit) {
        respond(422, 'A form field is too long.', ['field' => $field]);
    }
    $fields[$field] = trim($value);
}

if ($fields['website'] !== '') {
    respond(422, 'The enquiry could not be accepted.');
}
if (!preg_match('/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i', $fields['submission_id'])) {
    respond(422, 'The submission identifier is invalid.');
}
if (!in_array($fields['form_type'], ['enquiry', 'contact'], true)) {
    respond(422, 'Please select a valid form.');
}
if ($fields['name'] === '' || !filter_var($fields['email'], FILTER_VALIDATE_EMAIL)
    || !preg_match('/^\+?[0-9 ()-]{7,20}$/', $fields['phone'])
    || !preg_match('/^[0-9]{7,15}$/', preg_replace('/[^0-9]/', '', $fields['phone']))) {
    respond(422, 'Please enter your name, a valid email, and a valid phone number.');
}
if (($input['consent'] ?? null) !== true) {
    respond(422, 'Please consent to being contacted about your enquiry.');
}
if (!preg_match('~^/(?!/)[a-zA-Z0-9/_.%\-]*$~', $fields['source_path'])
    || str_contains($fields['source_path'], '..')) {
    respond(422, 'The source page is invalid.');
}
if ($fields['form_type'] === 'enquiry'
    && !in_array($fields['program'], ['MBA', 'MCA', 'BBA', 'BCA', 'BCOM_HONS'], true)) {
    respond(422, 'Please choose a program.');
}
if ($fields['form_type'] === 'contact') {
    foreach (['company', 'country', 'state', 'message'] as $required) {
        if ($fields[$required] === '') {
            respond(422, 'Please complete all required contact fields.', ['field' => $required]);
        }
    }
}

$configPath = getenv('GLA_DB_CONFIG') ?: dirname(__DIR__, 2) . DIRECTORY_SEPARATOR . 'gla-database.ini';
if (!is_file($configPath) || !is_readable($configPath)) {
    error_log('GLA enquiry: private database configuration is missing.');
    respond(503, 'The enquiry service is not configured. Please contact us by phone.');
}
$config = parse_ini_file($configPath, false, INI_SCANNER_RAW);
if ($config === false) {
    error_log('GLA enquiry: private database configuration could not be parsed.');
    respond(503, 'The enquiry service is unavailable. Please contact us by phone.');
}
foreach (['host', 'database', 'username', 'password'] as $key) {
    if (!isset($config[$key]) || !is_string($config[$key]) || $config[$key] === '') {
        error_log('GLA enquiry: incomplete database configuration.');
        respond(503, 'The enquiry service is unavailable. Please contact us by phone.');
    }
}
if (!preg_match('/^[a-zA-Z0-9_.-]+$/', $config['host'])
    || !preg_match('/^[a-zA-Z0-9_]+$/', $config['database'])) {
    error_log('GLA enquiry: invalid database connection settings.');
    respond(503, 'The enquiry service is unavailable. Please contact us by phone.');
}
$port = filter_var($config['port'] ?? '3306', FILTER_VALIDATE_INT, [
    'options' => ['min_range' => 1, 'max_range' => 65535],
]);
if ($port === false) {
    error_log('GLA enquiry: invalid database port.');
    respond(503, 'The enquiry service is unavailable. Please contact us by phone.');
}

$ipHash = hash_hmac('sha256', $_SERVER['REMOTE_ADDR'] ?? '', $config['password']);
$lockName = 'gla-form-' . substr($ipHash, 0, 40);
$pdo = null;
$locked = false;
$status = 201;
$message = 'Thank you. Your enquiry has been saved. Our team will contact you.';
try {
    $pdo = new PDO(
        "mysql:host={$config['host']};port={$port};dbname={$config['database']};charset=utf8mb4",
        $config['username'],
        $config['password'],
        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_EMULATE_PREPARES => false,
            PDO::ATTR_TIMEOUT => 5],
    );
    $lock = $pdo->prepare('SELECT GET_LOCK(?, 5)');
    $lock->execute([$lockName]);
    $locked = (int) $lock->fetchColumn() === 1;
    if (!$locked) {
        $status = 503;
        $message = 'The enquiry service is busy. Please try again.';
    } else {
        $duplicate = $pdo->prepare('SELECT ip_hash FROM form_submissions WHERE submission_id = ?');
        $duplicate->execute([$fields['submission_id']]);
        $existingHash = $duplicate->fetchColumn();
        if ($existingHash !== false) {
            if (!hash_equals($existingHash, $ipHash)) {
                $status = 409;
                $message = 'The submission identifier is already in use. Please reload the page.';
            } else {
                $status = 200;
            }
        } else {
            $count = $pdo->prepare(
                'SELECT COUNT(*) FROM form_submissions WHERE ip_hash = ? AND created_at > UTC_TIMESTAMP() - INTERVAL 10 MINUTE',
            );
            $count->execute([$ipHash]);
            if ((int) $count->fetchColumn() >= 5) {
                $status = 429;
                $message = 'Too many enquiries were submitted. Please try again in 10 minutes.';
            } else {
                $insert = $pdo->prepare(
                    'INSERT INTO form_submissions
                    (submission_id, form_type, name, email, phone, program, specialization,
                    country, state, city, company, message, source_path, ip_hash, consent, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, UTC_TIMESTAMP())',
                );
                $insert->execute([
                    $fields['submission_id'], $fields['form_type'], $fields['name'],
                    $fields['email'], $fields['phone'], $fields['program'],
                    $fields['specialization'], $fields['country'], $fields['state'],
                    $fields['city'], $fields['company'], $fields['message'],
                    $fields['source_path'], $ipHash,
                ]);
            }
        }
    }
} catch (PDOException $exception) {
    error_log('GLA enquiry: database operation failed (SQLSTATE ' . $exception->getCode() . ').');
    $status = 503;
    $message = 'Your enquiry could not be saved. Please try again later or contact us by phone.';
} finally {
    if ($locked && $pdo !== null) {
        try {
            $release = $pdo->prepare('SELECT RELEASE_LOCK(?)');
            $release->execute([$lockName]);
        } catch (PDOException $exception) {
            error_log('GLA enquiry: could not release database submission lock.');
        }
    }
}
if ($status === 429) {
    header('Retry-After: 600');
}
respond($status, $message, ['saved' => $status === 200 || $status === 201]);
