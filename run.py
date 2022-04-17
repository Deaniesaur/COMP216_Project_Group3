import os
import threading

scripts = [
  'python3 temperature_publisher.py --topic="room_temp_1"',
  'python3 temperature_publisher.py --topic="room_temp_2"',
  'python3 temperature_publisher.py --topic="room_temp_3"'
]

threads = []

if __name__ == '__main__':
  print(scripts)
  for script in scripts:
    print(script)
    thread = threading.Thread(target=os.system, args=[script])
    thread.setDaemon(True)
    thread.start()
    threads.append(thread)

  for thread in threads:
    thread.join()
  
  print('Exiting')