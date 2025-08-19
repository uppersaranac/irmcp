"""PubChem Server Troubleshooting

If you encounter connection errors like:
- ConnectError(EndOfStream()) during TLS handshake
- Request timeouts or connection failures

This is typically due to:
1. Intermittent network connectivity to pubchem.ncbi.nlm.nih.gov
2. Rate limiting from PubChem's servers
3. SSL/TLS connection issues

The server is configured with:
- Connection pooling (max 10 connections, 5 keepalive)
- 30 second timeout with 10 second connect timeout
- Custom User-Agent header

Most connection errors are transient and will resolve on retry.
"""
