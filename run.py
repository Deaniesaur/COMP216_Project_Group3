import os
import threading

scripts = [
  'python3 temperature_publisher.py --topic="sensor1"',
  'python3 temperature_publisher.py --topic="sensor2"',
  'python3 temperature_publisher.py --topic="sensor3"',
  'python3 temperature_client.py',
  'python3 temperature_client.py'
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