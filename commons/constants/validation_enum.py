class ValidationEnum:
    NULL_ERR = "null"
    MIN_LENGTH_ERR = "minLength"
    MAX_LENGTH_ERR = "maxLength"
    PATTERN_ERR = "pattern"
    MAX_LENGTH_EMAIL = 254
    MAX_LENGTH_PASSWORD = 128
    REGREX_EMAIL = "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    REGREX_PASSWORD = "[a-zA-Z0-9!-/:-@¥[-`{-~]{8,100}"
    PASSWORD_PATTERN = "password_pattern"
    DOES_NOT_EXIST = 'does not exist'
