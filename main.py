from controller.twitter_bot import main
from db.base import create_tables

if __name__ == '__main__':
    create_tables()
    main()
