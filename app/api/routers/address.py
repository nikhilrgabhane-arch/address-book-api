from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Address as AddressModel
from app.schemas.address import AddressCreate, AddressUpdate, AddressResponse
from app.services.geocoding import calculate_distance
from app.core.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter()

@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(address_in: AddressCreate, db: Session = Depends(get_db)):
    """Create a new address in the directory."""
    logger.info(f"Received request to create address: {address_in.name}")
    db_address = AddressModel(**address_in.model_dump())
    db.add(db_address)
    try:
        db.commit()
        db.refresh(db_address)
        logger.info(f"Successfully created address ID: {db_address.id}")
        return db_address
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to create address: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving the address."
        )

@router.get("/", response_model=List[AddressResponse])
def get_addresses(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: Session = Depends(get_db)):
    """Retrieve existing addresses with pagination."""
    addresses = db.query(AddressModel).offset(skip).limit(limit).all()
    return addresses

@router.get("/nearby", response_model=List[AddressResponse])
def get_nearby_addresses(
    latitude: float = Query(..., ge=-90.0, le=90.0, description="Target location latitude"),
    longitude: float = Query(..., ge=-180.0, le=180.0, description="Target location longitude"),
    distance_km: float = Query(..., gt=0, description="Radius in kilometers to search within"),
    db: Session = Depends(get_db)
):
    """
    Retrieve addresses that are within a given distance from specific location coordinates.
    Fetches all addresses from DB, and filters them in memory via the geodesic formula.
    (In a multi-million row production DB, we'd use PostGIS instead. For SQLite, this works).
    """
    logger.info(f"Searching for addresses within {distance_km}km of ({latitude}, {longitude})")
    
    all_addresses = db.query(AddressModel).all()
    nearby = []
    
    for address in all_addresses:
        try:
            dist = calculate_distance(latitude, longitude, address.latitude, address.longitude)
            if dist <= distance_km:
                nearby.append(address)
        except ValueError:
            # Skip invalid coordinates safely
            logger.warning(f"Address {address.id} has invalid coordinates. Skipping distance check.")
            continue
            
    logger.info(f"Found {len(nearby)} addresses out of {len(all_addresses)} total.")
    return nearby

@router.get("/{address_id}", response_model=AddressResponse)
def get_address(address_id: int, db: Session = Depends(get_db)):
    """Retrieve a single address by ID."""
    address = db.query(AddressModel).filter(AddressModel.id == address_id).first()
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return address

@router.put("/{address_id}", response_model=AddressResponse)
def update_address(address_id: int, address_in: AddressUpdate, db: Session = Depends(get_db)):
    """Update an existing address given its ID."""
    logger.info(f"Received request to update address ID: {address_id}")
    db_address = db.query(AddressModel).filter(AddressModel.id == address_id).first()
    
    if not db_address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
        
    update_data = address_in.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")
        
    for key, value in update_data.items():
        setattr(db_address, key, value)
        
    try:
        db.commit()
        db.refresh(db_address)
        logger.info(f"Successfully updated address ID: {address_id}")
        return db_address
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update address ID {address_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the address."
        )

@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_id: int, db: Session = Depends(get_db)):
    """Delete an existing address given its ID."""
    logger.info(f"Received request to delete address ID: {address_id}")
    db_address = db.query(AddressModel).filter(AddressModel.id == address_id).first()
    
    if not db_address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
        
    db.delete(db_address)
    try:
        db.commit()
        logger.info(f"Successfully deleted address ID: {address_id}")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete address ID {address_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the address."
        )
