#!/usr/bin/env python3
"""
Test script for the video organizer functionality
"""

import sys
import os
from complete_video_organizer import VideoOrganizer

def test_session_detection():
    """Test session number detection with various title formats."""
    organizer = VideoOrganizer()
    
    test_cases = [
        ("Sesi 1 - Pengenalan Usul Dirayat Hadis", 1),
        ("Session 15 - Advanced Topics", 15),
        ("25 - Hadis Classification", 25),
        ("[30] Important Concepts", 30),
        ("Part 45 - Detailed Analysis", 45),
        ("Usul Dirayat Hadis 60 - Final Session", 60),
        ("Episode 75: Critical Thinking", 75),
        ("90. Methodology Review", 90),
        ("Random Video Title", 0),  # Should not match
        ("Sesi 150 - Out of Range", 0),  # Should not match (out of range)
    ]
    
    print("Testing session number detection:")
    print("-" * 50)
    
    all_passed = True
    for title, expected in test_cases:
        result = organizer.extract_session_number(title)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{title}' -> {result} (expected {expected})")
        if result != expected:
            all_passed = False
    
    print(f"\nSession detection test: {'PASSED' if all_passed else 'FAILED'}")
    return all_passed

def test_title_cleaning():
    """Test title cleaning functionality."""
    organizer = VideoOrganizer()
    
    test_cases = [
        ("Sesi 1 - Pengenalan Usul Dirayat Hadis", 1, "Pengenalan"),
        ("Session 15 - Advanced Topics in Hadis", 15, "Advanced Topics in Hadis"),
        ("25 - Hadis Classification Methods", 25, "Hadis Classification Methods"),
        ("Usul Dirayat Hadis - Important Concepts", 30, "Important Concepts"),
        ("Random Title Without Session", 45, "Random Title Without Session"),
    ]
    
    print("\nTesting title cleaning:")
    print("-" * 50)
    
    all_passed = True
    for title, session_num, expected_contains in test_cases:
        result = organizer.clean_video_title(title, session_num)
        status = "✓" if expected_contains in result else "✗"
        print(f"{status} Session {session_num}: '{title}' -> '{result}'")
        if expected_contains not in result:
            all_passed = False
    
    print(f"\nTitle cleaning test: {'PASSED' if all_passed else 'FAILED'}")
    return all_passed

def test_json_loading():
    """Test JSON file loading."""
    organizer = VideoOrganizer('usul_dirayat_hadis/usul_dirayat_hadis.json')
    
    print("\nTesting JSON loading:")
    print("-" * 50)
    
    if organizer.data:
        print(f"✓ Successfully loaded {len(organizer.data)} sessions")
        
        # Check structure
        if organizer.data[0].get('session') and organizer.data[0].get('title') and organizer.data[0].get('link'):
            print("✓ JSON structure is correct")
            return True
        else:
            print("✗ JSON structure is incorrect")
            return False
    else:
        print("✗ Failed to load JSON file")
        return False

def main():
    """Run all tests."""
    print("Video Organizer Test Suite")
    print("=" * 50)
    
    tests = [
        test_session_detection,
        test_title_cleaning,
        test_json_loading
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"✗ Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    print(f"Success rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n🎉 All tests passed! The video organizer is ready to use.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())