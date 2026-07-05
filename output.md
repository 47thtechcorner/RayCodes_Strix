┌─ STRIX SECURITY SCAN ────────────────────────────────────────────────────────┐
│                                                                              │
│  TARGET: ./dummy_app                                                         │
│  MODE:   Quick Scan                                                          │
│  STATUS: Completed                                                           │
│                                                                              │
│  VULNERABILITIES FOUND: 1                                                    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

# [CRITICAL] Remote Code Execution (RCE) via eval()

**Location**: `dummy_app/dummy_target.py:8`

### Description
The application insecurely passes untrusted user input directly to the `eval()` function in `process_data()`. This allows a malicious actor to inject and execute arbitrary Python code on the host system, leading to full system compromise.

### Proof of Concept (PoC)
To exploit this vulnerability, an attacker can pass a payload containing system commands:

```python
# Payload
__import__("os").system("whoami")
```

When passed as an argument to the application:
```bash
python dummy_app/dummy_target.py '__import__("os").system("whoami")'
```

### Remediation Guidance
Never use `eval()` to process user-supplied data.
- If you need to evaluate Python literals securely, use `ast.literal_eval()`.
- If evaluating math expressions, use a dedicated expression parser.
- Sanitize and validate all user inputs against a strict allowlist.
