from time import sleep,localtime,time

class clock:
    def __init__ (self,h,m,s):
        self.h=h
        self.m=m
        self.s=s

    @classmethod
    def now(cls):
        ctime=localtime(time())
        return cls(ctime.tm_hour,ctime.tm_min,ctime.tm_sec)

    def run(self):
        self.s+=1
        if(self.s==60):
            self.s=0
            self.m+=1
            if(self.m==60):
                self.m=0
                self.h+=1
                if(self.h==24):
                    self.h=0
    def show(self):
        print("%d:%d:%d" % (self.h,self.m,self.s))

if __name__ =='__main__':
    Clock=clock.now()
    while True:
        sleep(1)
        Clock.run()
        Clock.show()