import sys

out = sys.argv

for i, item in enumerate(sys.argv):
    if item == "--path":
        outItem = i+1
        print(out[outItem])
    
        