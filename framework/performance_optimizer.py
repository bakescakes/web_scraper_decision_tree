"""
Performance Optimizer - Simplified Railway Version
Provides performance monitoring for Railway deployment
"""

import time
from typing import Dict, Any, List


class PerformanceOptimizer:
    """Simplified performance optimizer for Railway deployment"""
    
    def __init__(self):
        self.metrics = {
            'extraction_times': [],
            'success_rates': [],
            'error_counts': 0
        }
        self.max_execution_time = 35  # Railway timeout consideration
    
    def start_timer(self) -> float:
        """Start performance timer"""
        return time.time()
    
    def end_timer(self, start_time: float) -> float:
        """End timer and return duration"""
        duration = time.time() - start_time
        self.metrics['extraction_times'].append(duration)
        return duration
    
    def record_success(self, success: bool):
        """Record extraction success/failure"""
        self.metrics['success_rates'].append(success)
        if not success:
            self.metrics['error_counts'] += 1
    
    def optimize_extraction_strategy(self, url: str, expected_count: int = None) -> Dict[str, Any]:
        """Optimize extraction strategy for performance"""
        # Simplified optimization for Railway
        return {
            'strategy': 'enhanced_fallback',
            'timeout': min(self.max_execution_time, 30),
            'priority': 'speed_over_completeness' if expected_count and expected_count > 50 else 'balanced'
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        return {
            'average_extraction_time': sum(self.metrics['extraction_times']) / len(self.metrics['extraction_times']) if self.metrics['extraction_times'] else 0,
            'success_rate': sum(self.metrics['success_rates']) / len(self.metrics['success_rates']) if self.metrics['success_rates'] else 0,
            'total_extractions': len(self.metrics['extraction_times']),
            'error_count': self.metrics['error_counts']
        }