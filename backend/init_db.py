# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.config.database import Base
# from app.models import User, MemeSoldier, Battle, BattleParticipant, BattleStatus
# from app.utils.auth import generate_nonce
# from app.config.settings import settings
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Create engine
# engine = create_engine(
#     settings.DATABASE_URL, 
#     connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
# )

# # Create tables
# def init_db():
#     logger.info("Creating database tables...")
#     Base.metadata.create_all(bind=engine)
#     logger.info("Database tables created successfully")

# # Create session
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def create_test_data():
#     """Create test data for development purposes"""
#     logger.info("Creating test data...")
#     db = SessionLocal()
    
#     try:
#         # Check if we already have users
#         if db.query(User).count() > 0:
#             logger.info("Test data already exists, skipping creation")
#             return
        
#         # Create test users
#         test_wallets = [
#             "0x1234567890abcdef1234567890abcdef12345678",
#             "0xabcdef1234567890abcdef1234567890abcdef12"
#         ]
        
#         test_users = []
#         for wallet in test_wallets:
#             user = User(
#                 wallet_address=wallet,
#                 nonce=generate_nonce(),
#                 is_active=True
#             )
#             db.add(user)
#             test_users.append(user)
        
#         # Commit to get user IDs
#         db.commit()
        
#         logger.info(f"Created {len(test_users)} test users")
        
#         # Create test meme soldiers
#         test_meme_data = [
#             {
#                 "name": "Bubble Tea Warrior",
#                 "prompt": "A pixel art bubble tea with a warrior face",
#                 "image_url": "/images/placeholder_bubble_tea.png",
#                 "coin_icon_url": "/images/placeholder_coin_bubble_tea.png"
#             },
#             {
#                 "name": "Hot Pot Hero",
#                 "prompt": "A pixel art hot pot with superhero features",
#                 "image_url": "/images/placeholder_hot_pot.png",
#                 "coin_icon_url": "/images/placeholder_coin_hot_pot.png"
#             },
#             {
#                 "name": "Beef Noodle Ninja",
#                 "prompt": "A sneaky ninja made of beef noodles",
#                 "image_url": "/images/placeholder_beef_noodle.png",
#                 "coin_icon_url": "/images/placeholder_coin_beef_noodle.png"
#             }
#         ]
        
#         meme_soldiers = []
#         for i, meme_data in enumerate(test_meme_data):
#             # Assign to alternating users
#             owner_id = test_users[i % len(test_users)].id
            
#             soldier = MemeSoldier(
#                 owner_id=owner_id,
#                 name=meme_data["name"],
#                 prompt=meme_data["prompt"],
#                 image_url=meme_data["image_url"],
#                 coin_icon_url=meme_data["coin_icon_url"],
#                 deployed_to_battlefield=(i % 2 == 0),  # Every other soldier is deployed
#                 token_amount=1000 * (i + 1),
#                 token_amount_deployed=500 if (i % 2 == 0) else 0
#             )
#             db.add(soldier)
#             meme_soldiers.append(soldier)
        
#         # Commit to get soldier IDs
#         db.commit()
        
#         logger.info(f"Created {len(meme_soldiers)} test meme soldiers")
        
#         # Create test battles
#         from datetime import datetime, timedelta
        
#         test_battles = [
#             {
#                 "name": "Epic Meme Showdown",
#                 "description": "The ultimate battle between meme legends",
#                 "status": BattleStatus.ACTIVE,
#                 "start_time": datetime.now() - timedelta(hours=1),
#                 "end_time": datetime.now() + timedelta(hours=23)
#             },
#             {
#                 "name": "Pixel Art Duel",
#                 "description": "The clash of pixel perfect characters",
#                 "status": BattleStatus.PENDING,
#                 "start_time": datetime.now() + timedelta(hours=2),
#                 "end_time": datetime.now() + timedelta(days=1)
#             },
#             {
#                 "name": "Meme Championship Finals",
#                 "description": "Only the dankest memes survive",
#                 "status": BattleStatus.COMPLETED,
#                 "start_time": datetime.now() - timedelta(days=1),
#                 "end_time": datetime.now() - timedelta(hours=2)
#             }
#         ]
        
#         battles = []
#         for battle_data in test_battles:
#             battle = Battle(
#                 name=battle_data["name"],
#                 description=battle_data["description"],
#                 status=battle_data["status"],
#                 start_time=battle_data["start_time"],
#                 end_time=battle_data["end_time"]
#             )
#             db.add(battle)
#             battles.append(battle)
        
#         # Commit to get battle IDs
#         db.commit()
        
#         logger.info(f"Created {len(battles)} test battles")
        
#         # Create battle participants
#         for i, soldier in enumerate(meme_soldiers):
#             # Add each soldier to a battle
#             battle_id = battles[i % len(battles)].id
            
#             participant = BattleParticipant(
#                 battle_id=battle_id,
#                 soldier_id=soldier.id,
#                 votes=i * 10 + 5  # Just some random vote count
#             )
#             db.add(participant)
        
#         # Commit everything
#         db.commit()
        
#         logger.info("Test data created successfully")
        
#     except Exception as e:
#         db.rollback()
#         logger.error(f"Error creating test data: {e}")
#     finally:
#         db.close()

# if __name__ == "__main__":
#     # Create directories for images if they don't exist
#     os.makedirs(settings.MEME_STORAGE_PATH, exist_ok=True)
    
#     # Create placeholder images for testing
#     placeholder_dir = os.path.join(settings.MEME_STORAGE_PATH)
    
#     # Initialize the database
#     init_db()
    
#     # Create test data
#     create_test_data()
    
#     logger.info("Database initialized successfully") 