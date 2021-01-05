from DataReciver import messages_creator
import sys
import time

msgCreator = messages_creator.MessagesCreator()

msgCreator.sleep(1)

msgCreator.publish()

sys.exit()
