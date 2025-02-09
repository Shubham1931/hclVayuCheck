import json
from typing import Dict, List

# Comprehensive list of Indian cities organized by state and region
INDIAN_CITIES_DATA: Dict[str, Dict[str, List[str]]] = {
    "North": {
        "Delhi": ["Delhi", "New Delhi", "Dwarka", "Rohini", "Pitampura", "Janakpuri"],
        "Uttar Pradesh": [
            "Lucknow", "Kanpur", "Varanasi", "Agra", "Meerut", "Ghaziabad", "Noida",
            "Allahabad", "Gorakhpur", "Aligarh", "Bareilly", "Moradabad", "Saharanpur"
        ],
        "Punjab": [
            "Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda", "Mohali",
            "Pathankot", "Hoshiarpur", "Batala", "Moga"
        ],
        "Haryana": [
            "Gurugram", "Faridabad", "Panipat", "Ambala", "Yamunanagar", "Rohtak",
            "Hisar", "Karnal", "Sonipat", "Panchkula"
        ],
        "Rajasthan": [
            "Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer", "Bikaner", "Bhilwara",
            "Alwar", "Sikar", "Sri Ganganagar"
        ]
    },
    "South": {
        "Karnataka": [
            "Bangalore", "Mysuru", "Hubli", "Mangalore", "Belgaum", "Gulbarga",
            "Davanagere", "Bellary", "Shimoga", "Tumkur"
        ],
        "Tamil Nadu": [
            "Chennai", "Coimbatore", "Madurai", "Trichy", "Salem", "Tirunelveli",
            "Vellore", "Erode", "Thoothukkudi", "Dindigul"
        ],
        "Kerala": [
            "Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam",
            "Palakkad", "Alappuzha", "Kannur", "Kottayam"
        ],
        "Andhra Pradesh": [
            "Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool",
            "Rajahmundry", "Tirupati", "Kakinada", "Kadapa"
        ],
        "Telangana": [
            "Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam",
            "Ramagundam", "Secunderabad", "Mahbubnagar"
        ]
    },
    "East": {
        "West Bengal": [
            "Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri", "Bardhaman",
            "Malda", "Baharampur", "Krishnanagar"
        ],
        "Bihar": [
            "Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Darbhanga", "Arrah",
            "Bihar Sharif", "Begusarai", "Chhapra"
        ],
        "Odisha": [
            "Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur",
            "Puri", "Balasore", "Brahmapur", "Bargarh"
        ],
        "Jharkhand": [
            "Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Deoghar", "Hazaribagh",
            "Giridih", "Ramgarh"
        ]
    },
    "West": {
        "Maharashtra": [
            "Mumbai", "Pune", "Nagpur", "Thane", "Nashik", "Aurangabad", "Solapur",
            "Kalyan", "Navi Mumbai", "Ahmednagar", "Kolhapur"
        ],
        "Gujarat": [
            "Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar",
            "Gandhinagar", "Junagadh", "Anand", "Bharuch"
        ],
        "Madhya Pradesh": [
            "Indore", "Bhopal", "Jabalpur", "Gwalior", "Ujjain", "Sagar",
            "Dewas", "Satna", "Ratlam"
        ],
        "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa", "Ponda"]
    },
    "Northeast": {
        "Assam": [
            "Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Nagaon", "Tinsukia",
            "Tezpur", "Karimganj"
        ],
        "Meghalaya": ["Shillong", "Tura", "Jowai", "Nongstoin", "Williamnagar"],
        "Tripura": ["Agartala", "Udaipur", "Dharmanagar", "Kailasahar"],
        "Manipur": ["Imphal", "Thoubal", "Kakching", "Ukhrul"],
        "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Tuensang"],
        "Arunachal Pradesh": ["Itanagar", "Naharlagun", "Pasighat", "Tawang"],
        "Sikkim": ["Gangtok", "Namchi", "Gyalshing", "Mangan"]
    }
}

def get_all_cities() -> List[str]:
    """Return a flat list of all cities"""
    all_cities = []
    for region in INDIAN_CITIES_DATA.values():
        for state_cities in region.values():
            all_cities.extend(state_cities)
    return sorted(all_cities)

def get_region_and_state(city: str) -> tuple:
    """Return the region and state for a given city"""
    for region, states in INDIAN_CITIES_DATA.items():
        for state, cities in states.items():
            if city in cities:
                return region, state
    return "Other", "Other"

# Population size categories (for pollution factor calculation)
CITY_SIZES = {
    "Mega": ["Mumbai", "Delhi", "Bangalore", "Kolkata", "Chennai", "Hyderabad"],
    "Large": ["Pune", "Ahmedabad", "Surat", "Lucknow", "Jaipur", "Nagpur"],
    # Add more categories as needed
}

def get_city_size_factor(city: str) -> float:
    """Return a population-based factor for the city"""
    if city in CITY_SIZES["Mega"]:
        return 1.4
    elif city in CITY_SIZES["Large"]:
        return 1.2
    return 1.0
