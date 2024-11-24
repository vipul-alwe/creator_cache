from flask import Blueprint, request, jsonify
from models import db, CreatorBible
from sqlalchemy.exc import IntegrityError

creator_bp = Blueprint('creators', __name__)

# Create a new entry in the creator_bible table
@creator_bp.route('/creators', methods=['POST'])
def create_creator_entry():
    data = request.get_json()

    # Check for duplicate entries
    existing_entry = CreatorBible.query.filter_by(
        brand_name=data['brand_name'],
        campaign_name=data['campaign_name'],
        creator_name=data['creator_name']
    ).first()

    if existing_entry:
        return jsonify({"message": "Entry already exists for this combination of Brand, Campaign, and Creator"}), 400

    # Create a new entry if no duplicate exists
    new_entry = CreatorBible(
        brand_name=data['brand_name'],
        campaign_name=data['campaign_name'],
        date=data['date'],
        creator_name=data['creator_name'],
        channel_link=data['channel_link'],
        ucid=data['ucid'],
        gender=data['gender'],
        language=data['language'],
        genre=data['genre'],
        trend_type=data['trend_type'],
        pct_13_17=data['pct_13_17'],
        yt_gen_z_13_24=data['yt_gen_z_13_24'],
        rpr=data['rpr'],
        last_cost=data['last_cost'],
        last_campaign=data['last_campaign'],
        contacts=data['contacts'],
        contact_number=data['contact_number'],
        email_id=data['email_id'],
        median_views=data['median_views'],
        last_deliverables=data['last_deliverables'],
        ig_link=data['ig_link'],
        ig_subs=data['ig_subs']
    )

    db.session.add(new_entry)
    db.session.commit()

    return jsonify({"message": "Entry created successfully!"}), 201

# Get entries with optional filters
@creator_bp.route('/creators', methods=['GET'])
def get_creators():
    filters = request.args
    query = CreatorBible.query

    if 'brand_name' in filters:
        query = query.filter(CreatorBible.brand_name.ilike(f"%{filters['brand_name']}%"))
    if 'campaign_name' in filters:
        query = query.filter(CreatorBible.campaign_name.ilike(f"%{filters['campaign_name']}%"))
    if 'language' in filters:
        query = query.filter(CreatorBible.language.ilike(f"%{filters['language']}%"))
    if 'gender' in filters:
        query = query.filter(CreatorBible.gender == filters['gender'])
    # Add more filters as needed...

    entries = query.all()
    results = [
        {
            "id": entry.id,
            "brand_name": entry.brand_name,
            "campaign_name": entry.campaign_name,
            "date": entry.date,
            "creator_name": entry.creator_name,
            "channel_link": entry.channel_link,
            "ucid": entry.ucid,
            "gender": entry.gender,
            "language": entry.language,
            "genre": entry.genre,
            "trend_type": entry.trend_type,
            "pct_13_17": entry.pct_13_17,
            "yt_gen_z_13_24": entry.yt_gen_z_13_24,
            "rpr": entry.rpr,
            "last_cost": entry.last_cost,
            "last_campaign": entry.last_campaign,
            "contacts": entry.contacts,
            "contact_number": entry.contact_number,
            "email_id": entry.email_id,
            "median_views": entry.median_views,
            "last_deliverables": entry.last_deliverables,
            "ig_link": entry.ig_link,
            "ig_subs": entry.ig_subs
        }
        for entry in entries
    ]

    return jsonify(results), 200
