import multiprocessing

def run_script1():
    import subprocess
    subprocess.run(["python", "program1.py"])

def run_script2():
    import subprocess
    subprocess.run(["python", "program2.py"])

def run_script3():
    import subprocess
    subprocess.run(["python", "program3.py"])

if __name__ == "__main__":
    # Create two separate processes to run script1 and script2
    process1 = multiprocessing.Process(target=run_script1)
    process2 = multiprocessing.Process(target=run_script2)
    process3 = multiprocessing.Process(target=run_script3)


    # Start the processes
    process1.start()
    process2.start()
    process3.start()

    # Wait for both processes to finish
    process1.join()
    process2.join()
    process3.join()
