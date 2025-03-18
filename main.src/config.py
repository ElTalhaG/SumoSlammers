# Vindue indstillinger
BREDDE = 800  # Spillevinduets bredde i pixels
HØJDE = 600   # Spillevinduets højde i pixels

# Farver i RGB format (Rød, Grøn, Blå)
HVID = (255, 255, 255)  # Baggrundsfarve
RØD = (255, 0, 0)      # Spiller 1's farve
BLÅ = (0, 0, 255)      # Spiller 2's farve
GRØN = (0, 255, 0)     # Platformens farve
SORT = (0, 0, 0)       # Tekst farve

# Fysik indstillinger
TYNGDEKRAFT = 0.5      # Hvor hurtigt spillerne falder
HOPPE_KRAFT = -10      # Hvor højt spillerne hopper (negativ = op)
BEVÆGELSE_FART = 5     # Hvor hurtigt spillerne bevæger sig
BREMSE = 0.85          # Hvor hurtigt spillerne bremser (0-1)

# Kamp indstillinger
GRUND_SKUB = 8         # Minimum kraft når spillere kolliderer
MAX_SKUB = 35          # Maksimum kraft når spillere kolliderer
SPILLER_STØRRELSE = 25 # Spillerens radius
SKADE_MÆNGDE = 7      # Hvor meget skade der gives ved hit
MAX_SKADE = 100       # Maksimal skade en spiller kan have

# Dash indstillinger
DASH_KRAFT = 20        # Hvor hurtigt man bevæger sig under et dash
DASH_LÆNGDE = 12       # Hvor mange frames et dash varer
DASH_VENTETID = 200    # Antal frames mellem hver dash

# Platform indstillinger
PLATFORM_X = 100       # Platformens start x-position
PLATFORM_Y = 500       # Platformens y-position
PLATFORM_BREDDE = 600  # Platformens bredde
PLATFORM_HØJDE = 20    # Platformens højde 