"""
Rate limiting implementation for API endpoints.
"""
from functools import wraps
from flask import request, jsonify
import time
from collections import defaultdict

class RateLimiter:
    """Rate limiter class to prevent abuse of API endpoints."""
    
    def __init__(self, requests_per_minute=10):
        self.requests_per_minute = requests_per_minute
        # Store request timestamps by IP address
        self.request_records = defaultdict(list)
        
    def is_rate_limited(self, ip_address):
        """
        Check if the IP address has exceeded the rate limit.
        
        Args:
            ip_address: The client's IP address
            
        Returns:
            Boolean indicating if the client is rate limited
        """
        current_time = time.time()
        # Remove timestamps older than 1 minute
        self.request_records[ip_address] = [
            timestamp for timestamp in self.request_records[ip_address]
            if current_time - timestamp < 60
        ]
        
        # Check if the number of requests in the last minute exceeds the limit
        if len(self.request_records[ip_address]) >= self.requests_per_minute:
            return True
            
        # Add current request timestamp
        self.request_records[ip_address].append(current_time)
        return False
        
    def get_remaining_requests(self, ip_address):
        """Get the number of remaining requests for the IP address."""
        current_time = time.time()
        # Count requests in the last minute
        recent_requests = len([
            timestamp for timestamp in self.request_records[ip_address]
            if current_time - timestamp < 60
        ])
        
        return max(0, self.requests_per_minute - recent_requests)

def rate_limit(limiter):
    """
    Decorator for rate limiting routes.
    
    Args:
        limiter: RateLimiter instance
        
    Returns:
        Decorated function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip_address = request.remote_addr or 'unknown'
            
            if limiter.is_rate_limited(ip_address):
                response = {
                    'status': 'error',
                    'message': 'Rate limit exceeded. Please try again later.',
                    'remaining_requests': 0,
                    'retry_after': 60  # seconds
                }
                return jsonify(response), 429
                
            remaining = limiter.get_remaining_requests(ip_address)
            # Add rate limit headers
            response = f(*args, **kwargs)
            
            # If response is a tuple (response, status_code), modify the response
            if isinstance(response, tuple):
                resp, status_code = response
                resp.headers['X-RateLimit-Limit'] = str(limiter.requests_per_minute)
                resp.headers['X-RateLimit-Remaining'] = str(remaining)
                return resp, status_code
            
            # Otherwise, add headers to the response
            response.headers['X-RateLimit-Limit'] = str(limiter.requests_per_minute)
            response.headers['X-RateLimit-Remaining'] = str(remaining)
            return response
            
        return decorated_function
    return decorator