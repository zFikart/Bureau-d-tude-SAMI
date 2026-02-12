import time
import datetime


def trace(*args ):

    ts = time.time()
    sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
    
    info =  "".join(map(str,args))
    
    # print( info )
    
    fh = open(".trace.txt","a", encoding='utf8')
    fh.write(sttime + info + '\n')
    fh.close()

    return len(info)



