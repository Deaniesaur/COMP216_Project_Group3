import os
import threading

scripts = [
  'python group_3_dynamic_chart.py',
  'python group_3_dynamic_chart.py',
  'python group_3_dynamic_chart.py'
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