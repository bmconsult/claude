#!/usr/bin/env python3
"""
Time Calibrator - Tracks actual vs estimated times to improve future predictions
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class TimeCalibrator:
    def __init__(self, data_file: str = "time_calibration.json"):
        self.data_file = data_file
        self.records = self._load_records()
    
    def _load_records(self) -> List[Dict]:
        """Load existing time records from file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_records(self):
        """Save time records to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.records, f, indent=2)
    
    def add_record(self, task: str, estimated_min: float, actual_min: float):
        """Add a new time record"""
        record = {
            "task": task,
            "estimated_min": estimated_min,
            "actual_min": actual_min,
            "error_ratio": actual_min / estimated_min if estimated_min > 0 else 1.0,
            "timestamp": datetime.now().isoformat()
        }
        self.records.append(record)
        self._save_records()
        return record
    
    def get_calibration_factor(self, task_filter: Optional[str] = None) -> float:
        """Calculate average error ratio to calibrate future estimates"""
        if not self.records:
            return 1.0
        
        relevant_records = self.records
        if task_filter:
            relevant_records = [r for r in self.records if task_filter.lower() in r["task"].lower()]
        
        if not relevant_records:
            return 1.0
        
        avg_ratio = sum(r["error_ratio"] for r in relevant_records) / len(relevant_records)
        return avg_ratio
    
    def calibrate_estimate(self, estimated_min: float, task_filter: Optional[str] = None) -> float:
        """Apply calibration factor to a new estimate"""
        factor = self.get_calibration_factor(task_filter)
        calibrated = estimated_min * factor
        return round(calibrated, 1)
    
    def get_stats(self) -> Dict:
        """Get summary statistics"""
        if not self.records:
            return {"message": "No records yet"}
        
        ratios = [r["error_ratio"] for r in self.records]
        return {
            "total_records": len(self.records),
            "avg_calibration_factor": round(sum(ratios) / len(ratios), 2),
            "min_ratio": round(min(ratios), 2),
            "max_ratio": round(max(ratios), 2),
            "avg_overestimate_pct": round((sum(ratios) / len(ratios) - 1) * 100, 1)
        }
    
    def show_recent(self, n: int = 5):
        """Display recent records"""
        recent = self.records[-n:]
        print(f"\n=== Last {len(recent)} Records ===")
        for r in recent:
            print(f"Task: {r['task']}")
            print(f"  Estimated: {r['estimated_min']} min | Actual: {r['actual_min']} min")
            print(f"  Ratio: {r['error_ratio']:.2f}x\n")

def test_time_calibrator():
    """Test the time calibrator with sample data"""
    print("=== Time Calibrator Test ===\n")
    
    # Create calibrator
    cal = TimeCalibrator("test_calibration.json")
    
    # Add sample records
    cal.add_record("Email responses", 30, 21)
    cal.add_record("Code review", 45, 38)
    cal.add_record("Meeting prep", 20, 25)
    cal.add_record("Email responses", 25, 18)
    
    # Show statistics
    print("Statistics:")
    stats = cal.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test calibration
    print(f"\nCalibration factor: {cal.get_calibration_factor():.2f}x")
    print(f"New estimate: 30 min → Calibrated: {cal.calibrate_estimate(30)} min")
    print(f"Email-specific: 30 min → Calibrated: {cal.calibrate_estimate(30, 'email')} min")
    
    # Show recent records
    cal.show_recent(3)
    
    # Cleanup test file
    if os.path.exists("test_calibration.json"):
        os.remove("test_calibration.json")
    
    print("✓ Test complete!")

if __name__ == "__main__":
    test_time_calibrator()