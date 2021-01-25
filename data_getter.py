from DataReciver import messages_creator
import sys
import time

# Create new MessagesCreator object
msgCreator = messages_creator.MessagesCreator()

time.sleep(10)

#
msgCreator.publish()

sys.exit()
