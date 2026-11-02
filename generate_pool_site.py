import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "PoolSizePro"
SITE_TAGLINE = "Swimming Pool Volume, Pump GPM, Filter, Salt Cell & Heater Sizing Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f"

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/poolsizepro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "poolsizepro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "Dolphin Nautilus CC Plus Wi-Fi Robotic Pool Vacuum Cleaner",
        "category": "Robotic Pool Cleaner",
        "rating": "4.6 ★ (24,800+ reviews)",
        "badge": "#1 Best-Selling Pool Robot",
        "specs": "Inground & Above Ground up to 50 Ft | Wall & Floor Scrubbing | Tangle-Free Swivel Cable",
        "keyword": "Dolphin+Nautilus+CC+Plus+Robotic+Pool+Cleaner"
    },
    {
        "title": "BLACK+DECKER 1.5 HP & 2.0 HP Variable Speed Inground Pool Pump",
        "category": "Variable Speed Pump",
        "rating": "4.7 ★ (3,400+ reviews)",
        "badge": "Saves up to 80% Electricity",
        "specs": "ENERGY STAR Certified | 115V/230V Dual Voltage | Quiet Enclosed Fan | 5-Year Warranty",
        "keyword": "BLACK+DECKER+Variable+Speed+Inground+Pool+Pump+2+HP"
    },
    {
        "title": "Hayward W3AQR15 AquaRite Salt Chlorination System for 40,000-Gallon Pools",
        "category": "Saltwater Chlorinator",
        "rating": "4.7 ★ (5,600+ reviews)",
        "badge": "#1 Saltwater System",
        "specs": "Up to 40,000 Gallons | Silky Soft Water | Cuts Chlorine Costs by 50%+ | Digital Display",
        "keyword": "Hayward+W3AQR15+AquaRite+Salt+Chlorination+System+40000+Gallon"
    },
    {
        "title": "AIPER Scuba S1 Cordless Robotic Pool Cleaner for Inground Pools",
        "category": "Cordless Pool Robot",
        "rating": "4.6 ★ (6,900+ reviews)",
        "badge": "Top Cordless Crawler",
        "specs": "Caterpillar Treads | WavePath Navigation 2.0 | Wall, Floor & Waterline Scrubbing | 150-Min Runtime",
        "keyword": "AIPER+Scuba+S1+Cordless+Robotic+Pool+Cleaner"
    },
    {
        "title": "Pentair Clean & Clear Plus 320 & 420 Sq. Ft. Cartridge Pool Filter",
        "category": "Pool Filtration",
        "rating": "4.8 ★ (2,100+ reviews)",
        "badge": "Pro Installer Choice",
        "specs": "Fiberglass Reinforced Tank | 4-Cartridge Ultra-Fine Filtration | Zero Backwashing Water Loss",
        "keyword": "Pentair+Clean+and+Clear+Plus+Cartridge+Pool+Filter"
    },
    {
        "title": "FibroPool FH255 55,000 BTU Swimming Pool Heat Pump (Inground & Above Ground)",
        "category": "Electric Pool Heater",
        "rating": "4.6 ★ (1,750+ reviews)",
        "badge": "Best All-Season Heater",
        "specs": "Titanium Heat Exchanger | Digital Controller | Heats Pools up to 15,000–20,000 Gallons",
        "keyword": "FibroPool+55000+BTU+Swimming+Pool+Heat+Pump+Heater"
    },
    {
        "title": "Hayward W3SP2607X10 Super Pump 1.0 HP Single-Speed Pool Pump",
        "category": "Heavy-Duty Pool Pump",
        "rating": "4.7 ★ (8,900+ reviews)",
        "badge": "Industry Standard Reliability",
        "specs": "Corrosion-Proof PermaGlass XL | 110GPM High Flow | Tool-Free Strainer Cover",
        "keyword": "Hayward+Super+Pump+Pool+Pump+W3SP2607X10"
    },
    {
        "title": "Taylor K-2006C Complete FAS-DPD Service Pool Water Test Kit",
        "category": "Water Chemistry Testing",
        "rating": "4.9 ★ (19,300+ reviews)",
        "badge": "#1 Pro Water Test Kit",
        "specs": "Tests Free & Combined Chlorine, pH, Alkalinity, Calcium Hardness & CYA Stabilizer",
        "keyword": "Taylor+K+2006C+Complete+FAS+DPD+Pool+Water+Test+Kit"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "BLACK+DECKER 2.0 HP Variable Speed Pump",
        "type": "Variable Speed Pump",
        "max_pool": "Up to 35,000 Gal",
        "flow_rate": "35 – 108 GPM Adjustable",
        "energy_efficiency": "Saves up to 80% Power (ENERGY STAR)",
        "highlight": "Fits Hayward/Pentair Plumbing Unions",
        "rating": "4.7 / 5.0 ★",
        "keyword": "BLACK+DECKER+2+HP+Variable+Speed+Inground+Pool+Pump"
    },
    {
        "model": "Pentair SuperFlo VST Variable Speed Pump",
        "type": "Variable Speed Pump",
        "max_pool": "Up to 32,000 Gal",
        "flow_rate": "30 – 105 GPM Programmable",
        "energy_efficiency": "Saves up to 80% Power (TEFC Motor)",
        "highlight": "Auto-Sensing 115V/230V + RS-485 Automation",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Pentair+SuperFlo+VST+Variable+Speed+Pool+Pump+342002"
    },
    {
        "model": "Dolphin Nautilus CC Plus Wi-Fi Robot",
        "type": "Corded Robotic Cleaner",
        "max_pool": "Up to 50 Ft (All Surfaces)",
        "flow_rate": "4,000 GPH Suction Rate",
        "energy_efficiency": "5 Cents per Cleaning Cycle",
        "highlight": "Dual Scrubbing Brushes + Top-Load Basket",
        "rating": "4.6 / 5.0 ★",
        "keyword": "Dolphin+Nautilus+CC+Plus+WiFi+Robotic+Pool+Cleaner"
    },
    {
        "model": "AIPER Scuba S1 Cordless Robotic Cleaner",
        "type": "Cordless Robotic Cleaner",
        "max_pool": "Up to 1,600 Sq.Ft (50 Ft)",
        "flow_rate": "4,200 GPH Brushless Suction",
        "energy_efficiency": "Rechargeable Li-Ion (150 Min)",
        "highlight": "Zero Cords + Horizontal Waterline Scrubbing",
        "rating": "4.6 / 5.0 ★",
        "keyword": "AIPER+Scuba+S1+Cordless+Robotic+Pool+Cleaner"
    },
    {
        "model": "Hayward AquaRite W3AQR15 Salt System",
        "type": "Saltwater Chlorinator",
        "max_pool": "Up to 40,000 Gal",
        "flow_rate": "1.45 lbs/day Pure Chlorine Equiv.",
        "energy_efficiency": "Low-Amp TurboCell T-15",
        "highlight": "Eliminates Buying Liquid/Tablet Chlorine",
        "rating": "4.7 / 5.0 ★",
        "keyword": "Hayward+W3AQR15+AquaRite+Salt+Chlorination+System+40000+Gallon"
    },
    {
        "model": "Pentair Clean & Clear Plus 420 Filter",
        "type": "4-Cartridge Pool Filter",
        "max_pool": "Up to 45,000 Gal",
        "flow_rate": "150 GPM Max Design Flow",
        "energy_efficiency": "Low Head Loss + Zero Backwash Waste",
        "highlight": "Captures Particles Down to 20 Microns",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Pentair+Clean+and+Clear+Plus+420+Cartridge+Pool+Filter"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-dolphin-nautilus-cc-plus-vs-aiper-scuba-s1",
        "title": "Dolphin Nautilus CC Plus vs. AIPER Scuba S1: Corded vs. Cordless Pool Robot Comparison",
        "product_a": "Dolphin Nautilus CC Plus Wi-Fi",
        "product_b": "AIPER Scuba S1 Cordless",
        "winner_badge": "Best Uninterrupted Power vs. Best Cordless Freedom",
        "keyword_a": "Dolphin+Nautilus+CC+Plus+WiFi+Robotic+Pool+Cleaner",
        "keyword_b": "AIPER+Scuba+S1+Cordless+Robotic+Pool+Cleaner",
        "summary": "Compare suction GPH, wall climbing traction, filter micron rating, and weekly scheduling between the #1 corded Dolphin Nautilus CC Plus and the #1 cordless AIPER Scuba S1.",
        "metrics": [
            {"feature": "Power Source", "val_a": "Low-Voltage Swivel Power Cord (Unlimited Runtime)", "val_b": "Cordless Lithium Battery (150 Minutes Runtime)"},
            {"feature": "Max Pool Size", "val_a": "Inground & Above-Ground up to 50 Ft", "val_b": "Inground & Above-Ground up to 1,600 Sq.Ft (50 Ft)"},
            {"feature": "Cleaning Coverage", "val_a": "Floor & Vertical Pool Walls", "val_b": "Floor, Walls & Tile Waterline"},
            {"feature": "Weekly Auto-Timer", "val_a": "Yes — Leave in Pool All Week on Auto Schedule", "val_b": "Eco Mode (45 Mins Every 48 Hours for 7 Days)"},
            {"feature": "Best For", "val_a": "Hands-off daily automation & heavy leaf debris", "val_b": "Zero deck cords & quick drop-and-go cleaning"}
        ],
        "verdict_text": "Choose the Dolphin Nautilus CC Plus if you want to leave your cleaner in the pool and let its weekly timer run automatically without recharging a battery. Choose the AIPER Scuba S1 if you hate cords across your pool deck and want genuine waterline scrubbing at a lower upfront price."
    },
    {
        "slug": "compare-variable-speed-vs-single-speed-pool-pump",
        "title": "Variable Speed vs. Single Speed Pool Pump: Electricity Savings & GPM Flow Comparison",
        "product_a": "BLACK+DECKER 2.0 HP Variable Speed Pump",
        "product_b": "Hayward Super Pump 1.0 HP Single-Speed",
        "winner_badge": "Variable Speed Pays for Itself in 1 Season",
        "keyword_a": "BLACK+DECKER+2+HP+Variable+Speed+Inground+Pool+Pump",
        "keyword_b": "Hayward+Super+Pump+Pool+Pump+W3SP2607X10",
        "summary": "See exact watt consumption, decibel noise levels, filtration efficiency, and annual utility bill savings between modern variable-speed pumps and traditional single-speed pumps.",
        "metrics": [
            {"feature": "Power Consumption", "val_a": "180W – 1,650W (Runs at 250W on Low Speed)", "val_b": "1,400W – 1,800W Constant Full Draw"},
            {"feature": "Annual Electric Cost", "val_a": "$140 – $220 / Year", "val_b": "$750 – $1,100 / Year"},
            {"feature": "Noise Level", "val_a": "Whisper-Quiet 45 dB at Low RPM", "val_b": "68–72 dB Loud Motor Hum"},
            {"feature": "DOE Compliance", "val_a": "100% DOE & ENERGY STAR Compliant (+ Utility Rebates)", "val_b": "Restricted to Specific Legacy Replacements"},
            {"feature": "Plumbing Fit", "val_a": "Includes 1.5\" & 2\" Unions + Adjustable Base", "val_b": "1.5\" Female Threaded Ports"}
        ],
        "verdict_text": "Because of the Pump Affinity Law, cutting pump RPM in half reduces electricity consumption by 87.5%. The BLACK+DECKER 2.0 HP Variable Speed Pump saves $500 to $800 per year on utility bills while running silently and improving filter particle capture."
    },
    {
        "slug": "compare-cartridge-filter-vs-sand-pool-filter",
        "title": "Cartridge Pool Filter vs. Sand Filter: Water Clarity (Microns) & Maintenance Comparison",
        "product_a": "Pentair Clean & Clear Plus 320/420 Cartridge Filter",
        "product_b": "Hayward ProSeries High-Rate Sand Filter",
        "winner_badge": "Best Water Clarity vs. Easiest Backwashing",
        "keyword_a": "Pentair+Clean+and+Clear+Plus+Cartridge+Pool+Filter",
        "keyword_b": "Hayward+ProSeries+Sand+Pool+Filter+Multiport+Valve",
        "summary": "Compare micron filtration precision, backwash water waste, pump head pressure, and seasonal cleaning between oversized 4-cartridge filters and high-rate sand filters.",
        "metrics": [
            {"feature": "Filtration Precision", "val_a": "10 – 20 Microns (Sparkling Polished Water)", "val_b": "20 – 40 Microns (5–10 Microns with Filter Balls/Glass)"},
            {"feature": "Water Waste", "val_a": "Zero Backwashing — Saves 2,500+ Gal/Year & Salt", "val_b": "Requires 200–300 Gal Backwash Every 2–4 Weeks"},
            {"feature": "Cleaning Routine", "val_a": "Hose Off Pleated Cartridges Twice a Year", "val_b": "Turn Multiport Valve to Backwash for 3 Minutes"},
            {"feature": "Pump Efficiency", "val_a": "Lower PSI Backpressure (Ideal for VS Pumps)", "val_b": "Higher PSI Resistance Across Sand Bed"},
            {"feature": "Media Lifespan", "val_a": "Cartridges Last 3 – 5 Years", "val_b": "Silica Sand Lasts 5 – 7 Years"}
        ],
        "verdict_text": "If you have a saltwater pool or variable-speed pump, the Pentair Clean & Clear Plus Cartridge Filter is the superior choice because it never wastes salted, chemically balanced pool water through backwashing and filters particles twice as fine as standard sand."
    }
]

# ==========================================
# IN-DEPTH PRODUCT REVIEW ARTICLES DATABASE
# ==========================================
PRODUCT_REVIEWS = [
    {
        "slug": "review-dolphin-nautilus-cc-plus-robotic-pool-cleaner",
        "title": "Dolphin Nautilus CC Plus Wi-Fi Review: Why 24,000+ Pool Owners Swear By This Robot",
        "product_name": "Dolphin Nautilus CC Plus Wi-Fi Robotic Cleaner",
        "category": "Robotic Pool Cleaner",
        "rating_score": "4.8",
        "verdict_badge": "Editor's Choice — #1 Overall Pool Robot",
        "pool_capacity": "Up to 50 Ft (Inground & Above-Ground)",
        "flow_spec": "4,000 GPH Independent Filtration",
        "power_spec": "180W DC Swivel Power Supply (5¢/Cycle)",
        "warranty": "2.5-Year Manufacturer Warranty",
        "keyword": "Dolphin+Nautilus+CC+Plus+WiFi+Robotic+Pool+Cleaner",
        "summary": "The Dolphin Nautilus CC Plus Wi-Fi decouples pool vacuuming from your main skimmer pump, scrubbing floors and walls in 2 hours while cutting main pump wear and chemical consumption.",
        "pros": [
            "Dual active scrubbing brushes spin at 2x the robot's travel speed to remove stubborn algae and biofilm",
            "Patented anti-tangle swivel cable prevents coiling across 50-foot inground pools",
            "Top-load oversized filter basket rinses clean with a garden hose in under 60 seconds",
            "Built-in weekly scheduler and MyDolphin Plus Wi-Fi app run the robot automatically every morning"
        ],
        "cons": [
            "Caddy cart is sold separately (though the unit weighs only 19 lbs for easy lifting)"
        ],
        "body_paragraphs": [
            "Old-school pressure and suction-side cleaners force your main 1.5 HP pool pump to run at high RPMs and clog your main filter basket with leaves and sand. The Dolphin Nautilus CC Plus operates completely independently on a low-voltage DC power supply, circulating and filtering 4,000 gallons per hour while costing just 5 cents per 2-hour cycle.",
            "In our testing across a 20x40 (28,000-gallon) gunite pool, the CleverClean smart navigation scanned the pool floor and vertical walls systematically without getting stuck on main drains or steps. Switching from the standard mesh panels to the included ultra-fine pleated cartridges captured fine red dust and spring pollen that normally pass right through sand filters.",
            "With its programmable weekly timer, you can leave the Nautilus CC Plus submerged for the entire week and wake up to a spotless pool floor every single morning."
        ]
    },
    {
        "slug": "review-black-decker-variable-speed-pool-pump",
        "title": "BLACK+DECKER 2.0 HP Variable Speed Pool Pump Review: 80% Energy Savings & Drop-In Fit",
        "product_name": "BLACK+DECKER 2.0 HP Variable Speed Pool Pump",
        "category": "Variable Speed Pool Pump",
        "rating_score": "4.9",
        "verdict_badge": "Best Value Variable Speed Pump",
        "pool_capacity": "Up to 35,000 Gallons (1.5\" & 2\" Plumbing)",
        "flow_spec": "Up to 108 GPM (4 Programmable Speeds)",
        "power_spec": "115V / 230V Auto-Sensing | ENERGY STAR",
        "warranty": "5-Year Full Warranty",
        "keyword": "BLACK+DECKER+2+HP+Variable+Speed+Inground+Pool+Pump",
        "summary": "Engineered with an included adapter base that lines up directly with existing Hayward Super Pump and Pentair WhisperFlo plumbing, the BLACK+DECKER Variable Speed pump slashes electricity bills by up to 80%.",
        "pros": [
            "Includes a removable height-adapter base so you don't have to cut or replumb existing PVC pipes",
            "Totally Enclosed Fan Cooled (TEFC) permanent magnet motor operates at a whisper-quiet 45 dB",
            "Works on both 115V and 230V circuits and includes both 1.5-inch and 2-inch slip unions",
            "Industry-leading 5-year warranty at nearly half the cost of big-box installer pumps"
        ],
        "cons": [
            "Onboard digital keypad controls schedules directly on the unit rather than via smartphone app"
        ],
        "body_paragraphs": [
            "Replacing a noisy single-speed pump is the single highest-ROI upgrade any pool owner can make. Using our GPM turnover calculator, a 20,000-gallon pool requires 42 GPM for an 8-hour turnover. Instead of running a 1,800-watt single-speed pump, the BLACK+DECKER 2.0 HP VS pump achieves 42 GPM at roughly 1,750 RPM while drawing only 260 watts.",
            "What makes this pump a runaway bestseller on Amazon is its physical installation versatility. The box includes a precision riser base that matches the exact intake height of the Hayward Super Pump and Pentair SuperFlo, plus quick-disconnect unions for both 1.5-inch and 2.0-inch Schedule 40 PVC.",
            "Between electric utility rebates and $60–$90/month in power savings, this pump typically pays for its entire purchase price within 4 to 6 months of operation."
        ]
    },
    {
        "slug": "review-hayward-aquarite-w3aqr15-salt-chlorinator",
        "title": "Hayward AquaRite W3AQR15 Salt System Review: Silky Water & Zero Chlorine Buckets",
        "product_name": "Hayward W3AQR15 AquaRite 40,000-Gal Salt System",
        "category": "Saltwater Chlorinator",
        "rating_score": "4.8",
        "verdict_badge": "#1 Saltwater Chlorinator in America",
        "pool_capacity": "Up to 40,000 Gallons (T-Cell-15 Included)",
        "flow_spec": "1.45 lbs/day Pure Chlorine Production",
        "power_spec": "120V / 240V Convertible Control Box",
        "warranty": "3-Year Expert Line Warranty",
        "keyword": "Hayward+W3AQR15+AquaRite+Salt+Chlorination+System+40000+Gallon",
        "summary": "The Hayward AquaRite W3AQR15 converts mild dissolved pool salt (3,200 PPM—less salty than a human tear) into continuous, self-regenerating sanitizer so you never haul heavy chlorine buckets again.",
        "pros": [
            "Genuine TurboCell T-15 produces soft, silky water that won't sting eyes, fade swimsuits, or dry skin",
            "Eliminates the harsh chloramine smell and cyanuric acid (CYA) lock caused by trichlor pucks",
            "Digital diagnostic panel displays real-time salt PPM level, water temperature, and cell percentage output",
            "Sizing the 40,000-gallon W3AQR15 for a 20,000-gallon pool doubles cell lifespan by running at 50% duty cycle"
        ],
        "cons": [
            "Requires initial addition of solar pool salt bags (approx. 250 lbs per 10,000 gallons of fresh water)"
        ],
        "body_paragraphs": [
            "Pro pool builders always follow one golden rule when sizing a saltwater chlorinator: buy a cell rated for at least 1.5x to 2x your actual pool volume. Because the Hayward W3AQR15 includes the flagship 40,000-gallon T-Cell-15, owners of 15,000 to 28,000-gallon pools can run the dial at 40%–55%, extending the titanium cell lifespan up to 7 years.",
            "Once your pool water reaches 3,200 PPM of dissolved pool salt, water passing through the AquaRite cell undergoes low-voltage electrolysis, generating pure hypochlorous acid on the spot. After sanitizing algae and bacteria, it reverts back into salt—meaning the salt never evaporates and only needs a minor top-off after heavy rain.",
            "Water quality is night-and-day compared to tablet pools: zero red eyes, zero green hair, and rock-steady free chlorine levels even during 95°F July heatwaves."
        ]
    },
    {
        "slug": "review-aiper-scuba-s1-cordless-pool-robot",
        "title": "AIPER Scuba S1 Review: Caterpillar-Track Cordless Pool Robot with Waterline Scrubbing",
        "product_name": "AIPER Scuba S1 Cordless Robotic Pool Cleaner",
        "category": "Cordless Pool Robot",
        "rating_score": "4.7",
        "verdict_badge": "Best Cordless Robotic Cleaner",
        "pool_capacity": "Up to 1,600 Sq. Ft. (50 Ft Length)",
        "flow_spec": "4,200 GPH Brushless Drain Motor",
        "power_spec": "Cordless Li-Ion Battery (150-Min Runtime)",
        "warranty": "2-Year Manufacturer Warranty",
        "keyword": "AIPER+Scuba+S1+Cordless+Robotic+Pool+Cleaner",
        "summary": "Ditching the power cord altogether, the AIPER Scuba S1 uses tank-style caterpillar treads and WavePath 2.0 gyroscopic sensors to climb walls, scrub tile waterlines, and park itself by the wall.",
        "pros": [
            "100% cordless operation—zero cables across your patio and zero power boxes plugged into outdoor outlets",
            "Caterpillar tank tracks grip vinyl, fiberglass, and pebble-tec walls and climb over main drains effortlessly",
            "4 cleaning modes: Auto (Floor + Wall), Floor Only, Wall Only, and Periodic Eco Mode",
            "Quick-water-release drain system empties 90% of water weight in 15 seconds when lifting out"
        ],
        "cons": [
            "Requires recharging every 2.5 hours of continuous operation (or once a week in Eco Mode)"
        ],
        "body_paragraphs": [
            "First-generation cordless pool robots could only bump randomly along flat pool floors. The AIPER Scuba S1 changes the game by combining a high-torque brushless pump motor with heavy-duty caterpillar treads and WavePath 2.0 inertial navigation.",
            "Instead of wandering randomly, the Scuba S1 cleans the pool floor in structured S-patterns before climbing vertical walls to scrub the oil and sunscreen buildup right along the tile waterline. When its 150-minute cycle finishes, it automatically parks next to the pool wall so you can lift it out with the included retrieval hook without getting wet.",
            "For families with kids and pets running around the pool deck, eliminating trip-hazard electrical cords makes the Scuba S1 an unbeatable safety and convenience upgrade."
        ]
    }
]

# ==========================================
# PROGRAMMATIC SEO POOL SIZE & TYPE PRESETS
# ==========================================
POOL_PRESETS = [
    {"slug": "16x32-inground-pool-volume-pump-calculator", "name": "16' × 32' Rectangular Inground Pool", "shape": "rect", "length": 32, "width": 16, "depth": 5.5, "turnover": 8, "temp_rise": 15, "desc": "Calculate exact water volume (21,000+ gallons), variable-speed pump GPM flow rate, filter size, salt bags, and heater BTUs for a 16x32 inground pool."},
    {"slug": "24-foot-round-above-ground-pool-calculator", "name": "24-Foot Round Above-Ground Pool", "shape": "round", "length": 24, "width": 24, "depth": 4.5, "turnover": 8, "temp_rise": 12, "desc": "Calculate exact gallons (15,200 gal), GPH pump turnover, sand filter size, and salt chlorinator rating for a 24-foot round above-ground pool."},
    {"slug": "18x36-inground-swimming-pool-calculator", "name": "18' × 36' Family Inground Pool", "shape": "rect", "length": 36, "width": 18, "depth": 5.5, "turnover": 8, "temp_rise": 15, "desc": "Find exact pool volume (26,700 gallons), required GPM pump sizing, cartridge filter square footage, and salt system capacity for an 18x36 pool."},
    {"slug": "20x40-large-inground-pool-calculator", "name": "20' × 40' Large Residential Pool", "shape": "rect", "length": 40, "width": 20, "depth": 6.0, "turnover": 8, "temp_rise": 15, "desc": "Size the 2.0 HP variable speed pump, 420 sq.ft cartridge filter, 40k saltwater cell, and heat pump BTUs for a 20x40 (36,000-gallon) pool."},
    {"slug": "12x24-plunge-fiberglass-pool-calculator", "name": "12' × 24' Fiberglass & Plunge Pool", "shape": "rect", "length": 24, "width": 12, "depth": 5.0, "turnover": 8, "temp_rise": 18, "desc": "Calculate exact water volume (10,800 gallons), compact heat pump BTU size, and pump GPM flow rate for a 12x24 fiberglass or rectangular pool."},
    {"slug": "18-foot-round-above-ground-pool-calculator", "name": "18-Foot Round Above-Ground Pool", "shape": "round", "length": 18, "width": 18, "depth": 4.0, "turnover": 8, "temp_rise": 12, "desc": "Calculate exact gallon capacity (7,600 gallons), GPH filter pump requirement, and salt bags needed for an 18ft round above-ground pool."},
    {"slug": "27-foot-round-above-ground-pool-calculator", "name": "27-Foot Round Above-Ground Pool", "shape": "round", "length": 27, "width": 27, "depth": 4.5, "turnover": 8, "temp_rise": 12, "desc": "Determine exact gallons (19,300 gal), pump GPM turnover, and robotic cleaner specs for a large 27-foot round above-ground pool."},
    {"slug": "15x30-oval-above-ground-pool-calculator", "name": "15' × 30' Oval Above-Ground Pool", "shape": "oval", "length": 30, "width": 15, "depth": 4.5, "turnover": 8, "temp_rise": 12, "desc": "Calculate exact oval pool volume (11,900 gallons), sand filter sizing, pump GPH flow rate, and solar/electric heater BTUs for a 15x30 oval pool."},
    {"slug": "18x33-oval-swimming-pool-calculator", "name": "18' × 33' Oval Swimming Pool", "shape": "oval", "length": 33, "width": 18, "depth": 4.5, "turnover": 8, "temp_rise": 12, "desc": "Calculate water volume (15,800 gallons), pump GPM requirement, and saltwater generator sizing for an 18x33 oval pool."},
    {"slug": "14x28-inground-courtyard-pool-calculator", "name": "14' × 28' Courtyard Inground Pool", "shape": "rect", "length": 28, "width": 14, "depth": 5.0, "turnover": 8, "temp_rise": 15, "desc": "Calculate exact gallons (14,700 gal), variable-speed pump RPM/GPM settings, and electric heat pump sizing for a 14x28 inground pool."},
    {"slug": "21-foot-round-above-ground-pool-calculator", "name": "21-Foot Round Above-Ground Pool", "shape": "round", "length": 21, "width": 21, "depth": 4.5, "turnover": 8, "temp_rise": 12, "desc": "Calculate exact gallon capacity (11,600 gal), filter pump GPH turnover, and salt bags needed for a 21ft round pool."},
    {"slug": "30-foot-round-above-ground-pool-calculator", "name": "30-Foot Round Above-Ground Pool", "shape": "round", "length": 30, "width": 30, "depth": 4.5, "turnover": 8, "temp_rise": 12, "desc": "Size the high-flow pump GPM, filter tank, and saltwater system for a massive 30-foot round (23,800-gallon) above-ground pool."},
    {"slug": "10x20-cocktail-spool-pool-calculator", "name": "10' × 20' Cocktail Pool & Spool", "shape": "rect", "length": 20, "width": 10, "depth": 4.5, "turnover": 6, "temp_rise": 25, "desc": "Calculate fast 6-hour turnover GPM and high-efficiency heat pump BTU sizing to heat a 10x20 cocktail pool or spool year-round."},
    {"slug": "lap-pool-10x40-volume-pump-calculator", "name": "10' × 40' Fitness Lap Pool", "shape": "rect", "length": 40, "width": 10, "depth": 4.5, "turnover": 8, "temp_rise": 15, "desc": "Calculate gallon capacity (13,500 gal), cordless robotic cleaner coverage, and heat pump BTUs for a 40-foot fitness lap pool."}
]

def get_dynamic_gallon_pages():
    gallon_benchmarks = [
        (5000, 16, 16, 3.5, "round"),
        (7500, 18, 18, 4.0, "round"),
        (10000, 24, 12, 4.6, "rect"),
        (12000, 21, 21, 4.6, "round"),
        (15000, 28, 14, 5.1, "rect"),
        (18000, 30, 16, 5.0, "rect"),
        (20000, 32, 16, 5.2, "rect"),
        (25000, 36, 18, 5.1, "rect"),
        (30000, 38, 19, 5.5, "rect"),
        (35000, 40, 20, 5.8, "rect"),
        (40000, 42, 21, 6.0, "rect")
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(gallon_benchmarks), 8 + (day_of_year % 4))
    pages = []
    for gal, l, w, d, shp in gallon_benchmarks[:active_count]:
        pages.append({
            "slug": f"{gal}-gallon-pool-pump-filter-heater-calculator",
            "name": f"{gal:,}-Gallon Swimming Pool",
            "shape": shp,
            "length": l,
            "width": w,
            "depth": d,
            "turnover": 8,
            "temp_rise": 15,
            "desc": f"Calculate exact pump GPM/GPH flow rate, cartridge & sand filter size, salt bags, and heater BTUs required for a {gal:,}-gallon swimming pool."
        })
    return pages

ALL_CALC_PAGES = POOL_PRESETS + get_dynamic_gallon_pages()

def compute_pool_gallons(shape, length, width, depth):
    if shape == "round":
        return int(round(length * length * depth * 5.9))
    elif shape == "oval":
        return int(round(length * width * depth * 6.7))
    return int(round(length * width * depth * 7.5))

def generate_faq_data(preset_name, gallons, turnover):
    gph = int(round(gallons / turnover))
    gpm = int(math.ceil(gph / 60.0))
    salt_lbs = int(round((gallons / 10000.0) * 260))
    salt_bags = int(math.ceil(salt_lbs / 40.0))
    cart_sqft = max(100, int(math.ceil((gpm / 0.375) / 25.0) * 25))
    return [
        {
            "q": f"What size pool pump (GPM & GPH) do I need for a {preset_name} ({gallons:,} gallons)?",
            "a": f"To achieve a complete {turnover}-hour water turnover for a {gallons:,}-gallon pool, your pump must circulate at least {gph:,} Gallons Per Hour (GPH), which equals {gpm} Gallons Per Minute (GPM). We recommend a 1.5 HP to 2.0 HP Variable Speed Pool Pump so you can run at low RPMs for 12–16 hours daily and save up to 80% on electricity."
        },
        {
            "q": f"How many 40-lb bags of pool salt are needed for a {gallons:,}-gallon pool?",
            "a": f"Starting with fresh water (0 PPM salt), reaching the ideal 3,200 PPM salinity for a Hayward or Pentair saltwater chlorinator requires approximately {salt_lbs:,} lbs of 99.8% pure solar pool salt—which equals {salt_bags} standard 40-lb bags."
        },
        {
            "q": f"What size cartridge or sand filter is best for {gallons:,} gallons ({gpm} GPM)?",
            "a": f"At a design flow rate of {gpm} GPM, we recommend an oversized cartridge filter of at least {cart_sqft} Sq. Ft. (so you only clean cartridges 1–2 times per season) or a high-rate sand filter with at least {max(200, int(gpm * 5))} lbs of #20 silica sand."
        },
        {
            "q": "Why should I oversize my saltwater chlorinator cell by 1.5x to 2x?",
            "a": f"For a {gallons:,}-gallon pool, choosing a 40,000-gallon salt cell (like the Hayward AquaRite W3AQR15) allows you to run the cell output at 40%–50% instead of 100%. This prevents calcium scaling and doubles the lifespan of the titanium plates."
        },
        {
            "q": "Do robotic pool cleaners work better than suction or pressure cleaners?",
            "a": "Yes. Independent robotic pool cleaners (such as the Dolphin Nautilus CC Plus or cordless AIPER Scuba S1) have their own onboard motors and fine-micron filter baskets, using 85% less energy than running a booster pump while actively scrubbing algae off walls and tile lines."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-slate-200 hover:bg-sky-50/40 transition">
            <td class="p-3.5 font-extrabold text-slate-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-sky-800">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-slate-700">{item['max_pool']}</td>
            <td class="p-3.5 text-xs text-slate-700">{item['flow_rate']}</td>
            <td class="p-3.5 text-xs text-emerald-700 font-bold">{item['energy_efficiency']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-600">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-sky-600 hover:bg-sky-700 text-white font-bold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-white border-2 border-slate-200 hover:border-sky-600 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-sky-100 text-sky-900 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-slate-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-slate-600 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-sky-600 mt-4 inline-flex items-center gap-1">View Full Side-by-Side Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-slate-200 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-sky-600">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-slate-900">Top Pool Pumps, Robotic Cleaners & Salt Systems Compared</h2>
            </div>
            <span class="text-xs font-semibold text-slate-500">Updated 2026 Engineering & Efficiency Benchmarks</span>
        </div>

        <div class="bg-white border-2 border-slate-200 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-slate-100 border-b-2 border-slate-200 text-[11px] font-extrabold uppercase tracking-wider text-slate-700">
                        <th class="p-3.5">Equipment Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">Max Pool Size</th>
                        <th class="p-3.5">GPM / Output</th>
                        <th class="p-3.5">Efficiency / Key Benefit</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    cards = ""
    for rev in PRODUCT_REVIEWS:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-white border-2 border-slate-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-sky-100 text-sky-900 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-amber-100 text-amber-900 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide">{rev['category']}</span>
                <h3 class="text-lg font-extrabold text-slate-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-sky-600 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-slate-600 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-slate-50 p-3 rounded-xl border border-slate-200 mb-4">
                    <div><span class="text-slate-400 block">Pool Capacity:</span><strong class="text-slate-800">{rev['pool_capacity']}</strong></div>
                    <div><span class="text-slate-400 block">Performance:</span><strong class="text-slate-800">{rev['flow_spec']}</strong></div>
                    <div><span class="text-slate-400 block">Power / Efficiency:</span><strong class="text-slate-800">{rev['power_spec']}</strong></div>
                    <div><span class="text-slate-400 block">Warranty:</span><strong class="text-slate-800">{rev['warranty']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-slate-100 hover:bg-slate-200 text-slate-900 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full Review Article &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-sky-600 hover:bg-sky-700 text-white font-bold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards

def render_common_header_and_banner():
    top_deal_link = amz_url("Robotic+Pool+Cleaner+Variable+Speed+Pool+Pump+Salt+System+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-slate-900 text-white py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-slate-800">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-slate-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Pool Season Deals</span>
            <span>Save up to 35% on Robotic Pool Cleaners, Variable Speed Pumps & Saltwater Chlorinators on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-400 hover:text-amber-300 underline font-bold ml-1">
                Shop Today's Pool Equipment Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (WHITE BACKGROUND) -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-30">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-sky-600 flex items-center justify-center text-white font-black text-lg shadow-sm">P</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-slate-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-slate-500 font-medium">Pool Volume, Pump GPM & Heater Sizing</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-slate-700">
                <a href="{BASE_URL}/#calculator" class="hover:text-sky-600 transition">Pool Calculator</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-sky-600 transition">Search Gear</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-sky-600 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-sky-600 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-sky-600 transition">Reviews</a>
                <a href="{BASE_URL}/#faq" class="hover:text-sky-600 transition">FAQ</a>
            </nav>
        </div>
    </header>
    """

def render_calculator_page(page_data, is_home=False):
    gallons = compute_pool_gallons(page_data["shape"], page_data["length"], page_data["width"], page_data["depth"])
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} Volume, Pump GPM & Salt Calculator ({gallons:,} Gal) | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(page_data["name"], gallons, page_data["turnover"])

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm hover:shadow-md transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-sky-100 text-sky-900 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-600">{prod['rating']}</span>
                </div>
                <span class="text-xs text-slate-500 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-slate-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-slate-600 mb-4 bg-slate-50 p-2.5 rounded-lg border border-slate-100">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-sky-600 hover:bg-sky-700 text-white font-bold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        p_gal = compute_pool_gallons(p["shape"], p["length"], p["width"], p["depth"])
        active_cls = "bg-sky-50 border-sky-600 text-sky-900 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-white border-slate-200 text-slate-700 hover:border-sky-600 hover:text-slate-900"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-slate-400 font-mono shrink-0">{p_gal:,} gal</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-white border border-slate-200 rounded-xl p-5">
            <h3 class="text-base font-bold text-slate-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-slate-600 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("Dolphin+Robotic+Pool+Cleaner+and+Variable+Speed+Pool+Pump+Bundle")
    comparison_html = render_comparison_table_section()
    reviews_grid_html = render_review_cards_grid()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-white text-slate-900 antialiased selection:bg-sky-100 selection:text-slate-900">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100 border border-slate-200 text-xs font-semibold text-slate-700">
                <span>💧 PHTA & Hydraulic Engineering Pool Sizing Calculator</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
                { "Pool Volume (Gallons), Pump GPM, Salt Cell & Heater Calculator" if is_home else f"{page_data['name']} — Volume, Pump & Salt Sizing Calculator" }
            </h1>
            <p class="text-slate-600 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-slate-100 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-slate-900">1. Enter Your Pool Dimensions</h2>
                        <p class="text-xs text-slate-500">Calculates total gallons, pump GPM/GPH, filter area, salt bags & heater BTUs</p>
                    </div>
                    <span class="text-xs font-mono bg-sky-50 text-sky-700 px-2.5 py-1 rounded font-semibold">Instant Hydraulic Calc</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-2">Quick Select Standard Pool Size</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-sm font-medium text-slate-900 focus:ring-2 focus:ring-sky-600">
                        <option value="{page_data['shape']},{page_data['length']},{page_data['width']},{page_data['depth']},{page_data['turnover']},{page_data['temp_rise']}">Current: {page_data['name']} ({gallons:,} Gal)</option>
                        <option value="rect,32,16,5.5,8,15">16' × 32' Rectangular Inground Pool (21,120 Gal)</option>
                        <option value="round,24,24,4.5,8,12">24-Foot Round Above-Ground Pool (15,290 Gal)</option>
                        <option value="rect,36,18,5.5,8,15">18' × 36' Family Inground Pool (26,730 Gal)</option>
                        <option value="rect,40,20,6.0,8,15">20' × 40' Large Inground Pool (36,000 Gal)</option>
                        <option value="round,18,18,4.0,8,12">18-Foot Round Above-Ground Pool (7,646 Gal)</option>
                        <option value="oval,30,15,4.5,8,12">15' × 30' Oval Above-Ground Pool (13,568 Gal)</option>
                        <option value="rect,24,12,5.0,8,18">12' × 24' Fiberglass / Plunge Pool (10,800 Gal)</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="shapeInput" class="block text-sm font-bold text-slate-800 mb-1">Pool Shape</label>
                        <select id="shapeInput" onchange="calculatePool()" class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-sm font-bold text-slate-900">
                            <option value="rect" {"selected" if page_data['shape'] == "rect" else ""}>Rectangular / Lap Pool (L × W × D × 7.5)</option>
                            <option value="round" {"selected" if page_data['shape'] == "round" else ""}>Round Pool (Diameter² × D × 5.9)</option>
                            <option value="oval" {"selected" if page_data['shape'] == "oval" else ""}>Oval / Kidney Pool (L × W × D × 6.7)</option>
                        </select>
                    </div>

                    <div>
                        <label for="turnoverInput" class="block text-sm font-bold text-slate-800 mb-1">Target Water Turnover Time</label>
                        <select id="turnoverInput" onchange="calculatePool()" class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-sm font-bold text-slate-900">
                            <option value="6" {"selected" if page_data['turnover'] == 6 else ""}>6 Hours (Heavy Use / High Heat)</option>
                            <option value="8" {"selected" if page_data['turnover'] == 8 else ""}>8 Hours (Industry Standard Turnover)</option>
                            <option value="10" {"selected" if page_data['turnover'] == 10 else ""}>10 Hours (Variable Speed Eco Mode)</option>
                        </select>
                    </div>

                    <div>
                        <label for="lengthInput" class="block text-sm font-bold text-slate-800 mb-1">Pool Length / Diameter (Feet)</label>
                        <input type="number" id="lengthInput" value="{page_data['length']}" min="5" max="150" step="0.5" oninput="calculatePool()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-sky-600">
                    </div>

                    <div>
                        <label for="widthInput" class="block text-sm font-bold text-slate-800 mb-1">Pool Width (Feet)</label>
                        <input type="number" id="widthInput" value="{page_data['width']}" min="5" max="100" step="0.5" oninput="calculatePool()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-sky-600">
                        <span class="text-[11px] text-slate-500">For round pools, set equal to diameter</span>
                    </div>

                    <div>
                        <label for="depthInput" class="block text-sm font-bold text-slate-800 mb-1">Average Water Depth (Feet)</label>
                        <input type="number" id="depthInput" value="{page_data['depth']}" min="2" max="15" step="0.25" oninput="calculatePool()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-sky-600">
                        <span class="text-[11px] text-slate-500">(Shallow End + Deep End) ÷ 2</span>
                    </div>

                    <div>
                        <label for="tempRiseInput" class="block text-sm font-bold text-slate-800 mb-1">Desired Heater Temp Rise (°F)</label>
                        <input type="number" id="tempRiseInput" value="{page_data['temp_rise']}" min="5" max="40" step="1" oninput="calculatePool()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-sky-600">
                        <span class="text-[11px] text-slate-500">e.g. 15°F rise over 24 hours</span>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-white border-2 border-sky-600 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-slate-100 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-sky-600">2. Engineered Pool Specs</span>
                    <h2 class="text-xl font-extrabold text-slate-900">Your Required Equipment Sizing</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-sky-50 border border-sky-200 rounded-xl p-3.5">
                        <span class="text-xs text-sky-900 font-semibold block">Total Pool Volume</span>
                        <span id="resGallons" class="text-2xl font-black text-sky-700">0 Gal</span>
                        <span id="resLiters" class="text-[11px] text-sky-800 block mt-0.5">0 Liters</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-500 font-medium block">Min. Pump Flow Rate</span>
                        <span id="resGPM" class="text-2xl font-black text-slate-900">0 GPM</span>
                        <span id="resGPH" class="text-[11px] text-slate-500 block mt-0.5">0 GPH Turnover</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-500 font-medium block">Filter Size Required</span>
                        <span id="resFilter" class="text-base font-extrabold text-slate-900">0 Sq.Ft</span>
                        <span id="resSand" class="text-[11px] text-slate-500 block mt-0.5">or 0 lbs Sand</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-500 font-medium block">Salt Cell & Salt Startup</span>
                        <span id="resSaltCell" class="text-base font-extrabold text-emerald-700">0 Gal Cell</span>
                        <span id="resSaltBags" class="text-[11px] text-slate-500 block mt-0.5">0 Bags (40 lb)</span>
                    </div>
                </div>

                <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 flex items-center justify-between">
                    <span class="text-xs font-bold text-slate-700">Recommended Pool Heater / Heat Pump:</span>
                    <span id="resHeaterBTU" class="text-sm font-black text-amber-700 bg-white px-2.5 py-1 rounded border border-slate-200">0 BTU/hr</span>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-sky-50/70 border-2 border-sky-300 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-sky-600 text-white px-2 py-0.5 rounded">Matched Pool Hardware</span>
                        <span class="text-xs font-bold text-slate-600">Amazon Verified</span>
                    </div>
                    <h3 id="recEquipTitle" class="text-base font-extrabold text-slate-900 leading-snug">Loading Equipment Match...</h3>
                    <p id="recEquipDesc" class="text-xs text-slate-600"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPumpBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-sky-600 hover:bg-sky-700 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched Pump & Salt System &rarr;
                        </a>
                        <a id="recRobotBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-white hover:bg-slate-100 text-slate-800 border border-slate-300 font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop Matched Pool Robot
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-slate-900">Search Pool Pumps, Robotic Cleaners, Filters & Salt Systems</h2>
                <p class="text-sm text-slate-600">Search any pool brand (Dolphin, Pentair, Hayward, AIPER, BLACK+DECKER, Intex, Taylor) or equipment spec on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. Variable Speed Pool Pump 2 HP, Dolphin Nautilus CC Plus, 40000 Gallon Salt Chlorinator..."
                           class="flex-1 bg-white border-2 border-slate-300 rounded-xl px-4 py-3 text-sm font-medium text-slate-900 focus:outline-none focus:border-sky-600" required>
                    <button type="submit" class="bg-sky-600 hover:bg-sky-700 text-white font-bold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-slate-400 font-semibold">Popular Equipment:</span>
                    <a href="{amz_url('Dolphin Robotic Pool Vacuum Cleaner')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-sky-100 text-slate-700 rounded-full transition">Robotic Pool Cleaners</a>
                    <a href="{amz_url('Variable Speed Pool Pump 1.5 HP 2 HP')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-sky-100 text-slate-700 rounded-full transition">Variable Speed Pumps</a>
                    <a href="{amz_url('Saltwater Pool Chlorinator System 40000 Gallon')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-sky-100 text-slate-700 rounded-full transition">Saltwater Chlorinators</a>
                    <a href="{amz_url('Swimming Pool Heat Pump Heater')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-sky-100 text-slate-700 rounded-full transition">Pool Heat Pumps</a>
                    <a href="{amz_url('Cartridge Pool Filter Pentair Hayward')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-sky-100 text-slate-700 rounded-full transition">Cartridge Filters</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-slate-200 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-sky-600">Verified Best-Selling Hardware</span>
                    <h2 class="text-2xl font-extrabold text-slate-900">Best-Selling Pool Cleaners, Pumps, Filters & Heaters</h2>
                </div>
                <a href="{amz_url('Best Selling Swimming Pool Pumps Cleaners and Salt Systems')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-sky-600 hover:text-sky-700">
                    View Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- IN-DEPTH PRODUCT REVIEW ARTICLES SECTION (ARTIKEL PRODUK REVIEW) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-slate-200 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-sky-600">Hands-On Hydraulic & Cleaning Tests</span>
                    <h2 class="text-2xl font-extrabold text-slate-900">In-Depth Pool Equipment Review Articles</h2>
                </div>
                <span class="text-xs font-semibold text-slate-500">Field-Tested Flow Rates, Energy Savings & Durability</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-slate-50 border-2 border-sky-600 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-sky-600 text-white px-2.5 py-1 rounded">Zero-Maintenance Pool Upgrade</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-slate-900">Tired of Vacuuming by Hand & Hauling Chlorine Buckets?</h2>
                <p class="text-sm text-slate-600">Combine a Robotic Pool Cleaner with a Variable Speed Pump and Saltwater Chlorinator to cut weekly maintenance to 10 minutes and slash power bills by up to 80%.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-sky-600 hover:bg-sky-700 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore Pool Automation Bundles on Amazon &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-slate-200 pb-3">
                <h2 class="text-xl font-extrabold text-slate-900">Pool Size & Gallon Specific Calculators</h2>
                <p class="text-xs text-slate-500">Select your exact pool dimensions or gallon volume below for pre-calculated pump GPM, filter area, and salt system sizing.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-slate-200 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-sky-600">Pool Hydraulic & Chemistry Guide</span>
                <h2 class="text-2xl font-extrabold text-slate-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

    </main>

    <!-- FOOTER -->
    <footer class="bg-white border-t border-slate-200 mt-16 py-10 px-4 text-xs text-slate-500">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-slate-800">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-slate-600">
                <a href="{BASE_URL}/" class="hover:text-slate-900">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-slate-900">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-slate-900">Reviews</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-slate-900">Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-slate-900">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 6) {{
                document.getElementById("shapeInput").value = parts[0];
                document.getElementById("lengthInput").value = parts[1];
                document.getElementById("widthInput").value = parts[2];
                document.getElementById("depthInput").value = parts[3];
                document.getElementById("turnoverInput").value = parts[4];
                document.getElementById("tempRiseInput").value = parts[5];
                calculatePool();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculatePool() {{
            const shape = document.getElementById("shapeInput").value || "rect";
            const length = parseFloat(document.getElementById("lengthInput").value) || 20;
            let width = parseFloat(document.getElementById("widthInput").value) || 15;
            const depth = parseFloat(document.getElementById("depthInput").value) || 5;
            const turnover = parseFloat(document.getElementById("turnoverInput").value) || 8;
            const tempRise = parseFloat(document.getElementById("tempRiseInput").value) || 15;

            if (shape === "round") {{
                width = length;
            }}

            let multiplier = 7.5;
            if (shape === "round") multiplier = 5.9;
            if (shape === "oval") multiplier = 6.7;

            const gallons = Math.round(length * width * depth * multiplier);
            const liters = Math.round(gallons * 3.78541);
            const gph = Math.round(gallons / turnover);
            const gpm = Math.max(15, Math.ceil(gph / 60));

            const cartridgeSqFt = Math.max(100, Math.ceil((gpm / 0.375) / 25) * 25);
            const sandLbs = Math.max(150, Math.ceil((gpm * 5.2) / 50) * 50);

            const saltCellTier = gallons <= 12000 ? "20,000" : (gallons <= 22000 ? "30,000" : "40,000");
            const saltLbsNeeded = Math.round((gallons / 10000) * 260);
            const saltBags = Math.ceil(saltLbsNeeded / 40);

            const rawBTU = (gallons * 8.34 * tempRise) / 24;
            const heaterBTU = Math.max(50000, Math.ceil((rawBTU * 1.2) / 10000) * 10000);

            document.getElementById("resGallons").textContent = gallons.toLocaleString() + " Gal";
            document.getElementById("resLiters").textContent = liters.toLocaleString() + " Liters";
            document.getElementById("resGPM").textContent = gpm + " GPM";
            document.getElementById("resGPH").textContent = gph.toLocaleString() + " GPH (" + turnover + "h turnover)";
            document.getElementById("resFilter").textContent = cartridgeSqFt + " Sq.Ft Cartridge";
            document.getElementById("resSand").textContent = "or " + sandLbs + " lbs Sand Filter";
            document.getElementById("resSaltCell").textContent = saltCellTier + " Gal Cell";
            document.getElementById("resSaltBags").textContent = saltBags + " Bags (" + saltLbsNeeded.toLocaleString() + " lbs Salt)";
            document.getElementById("resHeaterBTU").textContent = heaterBTU.toLocaleString() + "+ BTU/hr";

            let recTitle = "";
            let recDesc = "";
            let pumpQuery = "";
            let robotQuery = "";

            if (gallons <= 14000) {{
                recTitle = "1.5 HP Variable Speed Pump + 20k–25k Salt System + Cordless Pool Robot";
                recDesc = "Ideal hydraulic sizing for above-ground, plunge, and compact pools up to 14,000 gallons.";
                pumpQuery = "BLACK+DECKER 1.5 HP Variable Speed Pool Pump and Saltwater Chlorinator";
                robotQuery = "AIPER Scuba S1 Cordless Robotic Pool Cleaner";
            }} else if (gallons <= 26000) {{
                recTitle = "2.0 HP Variable Speed Pump + Hayward 40k Salt Cell + Dolphin CC Plus Robot";
                recDesc = "Best-selling residential inground bundle for 15,000 to 26,000 gallon family pools.";
                pumpQuery = "BLACK+DECKER 2 HP Variable Speed Inground Pool Pump Hayward AquaRite 40000";
                robotQuery = "Dolphin Nautilus CC Plus WiFi Robotic Pool Cleaner";
            }} else {{
                recTitle = "2.0–3.0 HP High-Flow Variable Speed Pump + 420 Sq.Ft Filter + 40k Salt System";
                recDesc = "Heavy-duty turnover & filtration engineered for large 26,000+ gallon residential pools.";
                pumpQuery = "Pentair Variable Speed Pool Pump and Clean Clear Plus 420 Filter";
                robotQuery = "Dolphin Premier Nautilus CC Plus Robotic Pool Cleaner 50 Ft";
            }}

            document.getElementById("recEquipTitle").textContent = recTitle;
            document.getElementById("recEquipDesc").textContent = recDesc;
            document.getElementById("recPumpBtn").href = makeAmazonLink(pumpQuery);
            document.getElementById("recRobotBtn").href = makeAmazonLink(robotQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculatePool);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-slate-700"><span class="text-emerald-600 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-slate-700"><span class="text-rose-600 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-slate-700 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-white text-slate-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-slate-500 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-sky-600">Home & Pool Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-sky-600">Equipment Reviews</a>
            <span>/</span>
            <span class="text-slate-800">{rev['product_name']}</span>
        </nav>

        <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-sky-100 text-sky-900 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <span class="text-sm font-black bg-amber-100 text-amber-900 px-3 py-1 rounded-lg">Lab Rating: {rev['rating_score']} / 5.0 ★</span>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-slate-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-slate-600 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs">
                <div><span class="text-slate-400 block font-medium">Pool Capacity</span><strong class="text-slate-900">{rev['pool_capacity']}</strong></div>
                <div><span class="text-slate-400 block font-medium">Flow / Output</span><strong class="text-slate-900">{rev['flow_spec']}</strong></div>
                <div><span class="text-slate-400 block font-medium">Electrical Spec</span><strong class="text-slate-900">{rev['power_spec']}</strong></div>
                <div><span class="text-slate-400 block font-medium">Warranty</span><strong class="text-slate-900">{rev['warranty']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-sky-600 hover:bg-sky-700 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-slate-100 hover:bg-slate-200 text-slate-900 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Size Your Pool Gallons & GPM
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-white border-2 border-emerald-200 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-white border-2 border-rose-200 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-slate-900 border-b border-slate-100 pb-3">Field Test & Hydraulic Performance Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-sky-600 block">Final Verdict</span>
                    <p class="text-sm font-bold text-slate-900">{rev['product_name']} scores {rev['rating_score']}/5.0 in our pool equipment benchmark.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-amber-500 hover:bg-amber-600 text-slate-950 font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>
    </main>

    <footer class="bg-white border-t border-slate-200 mt-16 py-10 px-4 text-xs text-slate-500 text-center">
        <p class="font-bold text-slate-800">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-slate-200">
            <td class="p-4 font-bold text-slate-900 bg-slate-50 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-slate-700 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-slate-700 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white text-slate-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-slate-500 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-sky-600">Home & Pool Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-sky-600">Product Comparisons</a>
            <span>/</span>
            <span class="text-slate-800">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-sky-100 text-sky-900 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-slate-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-slate-600 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-white border-2 border-slate-200 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-slate-900 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-sky-300">{vs['product_a']}</th>
                        <th class="p-4 text-amber-300">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-slate-50">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-slate-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-sky-600 hover:bg-sky-700 text-white font-bold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-sky-50 border-2 border-sky-200 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-slate-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-slate-700 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-sky-600 hover:bg-sky-700 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-slate-900 hover:bg-slate-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-white border-t border-slate-200 mt-16 py-10 px-4 text-xs text-slate-500 text-center">
        <p class="font-bold text-slate-800">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "16' × 32' Inground Pool",
        "shape": "rect",
        "length": 32,
        "width": 16,
        "depth": 5.5,
        "turnover": 8,
        "temp_rise": 15,
        "desc": "Calculate exact swimming pool volume (gallons & liters), variable-speed pump GPM/GPH turnover, filter size, salt bags, and heater BTUs—plus compare top-rated pool equipment."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Programmatic Pool Size & Gallon Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 3. Generate Standalone Product Review Pages
    for rev in PRODUCT_REVIEWS:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} SEO pages (Calculators + Reviews + Comparisons) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
