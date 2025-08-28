import re

# Security vulnerability patterns - the core of the scanner
SECURITY_PATTERNS = [
    # Hardcoded secrets (critical)
    {
        'name': 'hardcoded_api_key',
        'pattern': re.compile(r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\'][^"\']{10,}["\']'),
        'message': 'Hardcoded API key detected',
        'severity': 'critical',
        'cwe_id': 'CWE-798'
    },
    {
        'name': 'hardcoded_password',
        'pattern': re.compile(r'(?i)(password|passwd|pwd)\s*[=:]\s*["\'][^"\']{3,}["\']'),
        'message': 'Hardcoded password detected',
        'severity': 'critical',
        'cwe_id': 'CWE-798'
    },
    {
        'name': 'hardcoded_token',
        'pattern': re.compile(r'(?i)(token|auth[_-]?token)\s*[=:]\s*["\'][^"\']{15,}["\']'),
        'message': 'Hardcoded authentication token detected',
        'severity': 'critical',
        'cwe_id': 'CWE-798'
    },
    
    # Code injection (critical)
    {
        'name': 'eval_usage',
        'pattern': re.compile(r'\beval\s*\('),
        'message': 'eval() usage can lead to code injection',
        'severity': 'critical',
        'cwe_id': 'CWE-94'
    },
    {
        'name': 'exec_usage',
        'pattern': re.compile(r'\bexec\s*\('),
        'message': 'exec() usage can lead to code injection',
        'severity': 'critical',
        'cwe_id': 'CWE-94'
    },
    
    # Command injection (high)
    {
        'name': 'shell_injection',
        'pattern': re.compile(r'shell\s*=\s*True'),
        'message': 'subprocess with shell=True can lead to command injection',
        'severity': 'high',
        'cwe_id': 'CWE-78'
    },
    
    # SQL injection (high)
    {
        'name': 'sql_injection',
        'pattern': re.compile(r'(?i)(SELECT|INSERT|UPDATE|DELETE).*%[sd]'),
        'message': 'SQL query uses string formatting - potential SQL injection',
        'severity': 'high',
        'cwe_id': 'CWE-89'
    },
    
    # Weak crypto (medium)
    {
        'name': 'weak_hash_md5',
        'pattern': re.compile(r'\bhashlib\.md5\s*\('),
        'message': 'MD5 is cryptographically weak - use SHA-256 or better',
        'severity': 'medium',
        'cwe_id': 'CWE-327'
    },
    {
        'name': 'weak_hash_sha1',
        'pattern': re.compile(r'\bhashlib\.sha1\s*\('),
        'message': 'SHA-1 is cryptographically weak - use SHA-256 or better',
        'severity': 'medium',
        'cwe_id': 'CWE-327'
    },
    
    # Configuration issues (medium)
    {
        'name': 'debug_enabled',
        'pattern': re.compile(r'(?i)debug\s*[=:]\s*True'),
        'message': 'Debug mode enabled - should be False in production',
        'severity': 'medium',
        'cwe_id': 'CWE-489'
    },
    
    # Path traversal (high)
    {
        'name': 'path_traversal',
        'pattern': re.compile(r'os\.path\.join\([^)]*\.\./'),
        'message': 'Potential path traversal vulnerability',
        'severity': 'high',
        'cwe_id': 'CWE-22'
    },
]

# Convert to pattern objects for faster matching
COMPILED_PATTERNS = [
    {
        'name': p['name'],
        'pattern': p['pattern'],
        'message': p['message'],
        'severity': p['severity'],
        'cwe_id': p['cwe_id']
    } for p in SECURITY_PATTERNS
]

