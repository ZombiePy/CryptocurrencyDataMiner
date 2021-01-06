from DataReciver import messages_creator
import sys
import time

msgCreator = messages_creator.MessagesCreator()

time.sleep(10)

msgCreator.publish()

sys.exit()
