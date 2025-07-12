"""
Main entry point for Ukraine Support Gravity Analysis

Run this script to execute the concentricity analysis by default.
You can modify the function call to run different analyses.
"""

from ukraine_support_gravity import (
    run_support_gravity_center, 
    run_concentricity, 
    extract_support_gravity_center
)

if __name__ == '__main__':
    # Run the concentricity analysis by default
    # Uncomment the line below to extract data first if needed:
    # extract_support_gravity_center()
    
    run_concentricity()
    
    # Uncomment to run the gravity center analysis:
    # run_support_gravity_center()
