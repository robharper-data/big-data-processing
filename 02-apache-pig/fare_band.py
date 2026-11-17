from pig_util import outputSchema

@outputSchema('fare_band:chararray')
def fare_band(fare):
    # Handle None or invalid fare values
    if fare is None:
        return 'Unknown'
    
    # Try to convert fare to float
    try:
        fare = float(fare)
    except (ValueError, TypeError):
        return 'Unknown'
    
    # Determine fare band
    if fare <= 15:
        return 'LOW'
    elif 15 < fare <= 30:
        return 'MID'
    else:
        return 'HIGH'

