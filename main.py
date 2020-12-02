from DataReciver import messages_creator
import time

test = messages_creator.MessagesCreator()

time.sleep(5)

test.start_loop()
