#!/usr/bin/env python
# coding: utf-8

# In[17]:


import numpy as np

class Memory:
    memory = None
    x = 0
    y = 0
    size = 0
    busy = False
    def __init__(self,x,y):
        if(x > 0 and y >0):
            print(x,y)
            self.x = x.copy()
            self.y = y.copy()
            self.size = x*y
            self.memory = np.zeros([x,y])
        
        
    def read(self,address):
        if(address >= self.size):
            print("Address out of Range!")
            return
        else:
            i = int(address/self.y)
            j = int(address%self.y)
            return self.memory[i][j] 
        
        
    def write(self,address,data):
        if(self.busy):
            return
        if(address>=self.size):
            print("Address out of Range!")
            return
        else:
            i = int(address/self.y)
            j = int(address%self.y)
            
            self.memory[i][j] = data.copy()
            return
    def Print(self):
        for i in range (x):
            for j in range(y):
                print(self.memory[i][j])
        return
    def acquire(self):
        if(self.busy):
            return False
        self.busy = True
        return self.busy
    
    def release(self):
        self.busy = False
        return True


# In[2]:


class ImageCache:
    
    cache = None
    memory = None
    address = None
    x = 0 #number of Rows
    y = 0 #number of Columns
    def __init__(self,cacheX,cacheY,mem,address):
        if(cacheX > 0 and cacheY > 0):
            self.x = cacheX.copy()
            self.y = cacheY.copy()
            self.cache = numpy.zeros([cacheX,cacheY])
            self.memory= mem
            self.address = address.copy()
            self.currentCol = 0
    def initialize(self):
        for i in range(cacheX):
            for j in range(cacheY):
                if (memory.acquire()):
                    cache[i][j] = memory.read(address)
                    address += 1
        memory.release()
        return
    
    def shift(self,ColNumber):
        if(colNumber > self.y):
            return None
        return cache[:,colNumber]
    
    def insert(self,ColNumber,data):
        if(colNumber > self.y):
            return False
        else:
            for i in range(self.x-1):
                cache[i,colNumber] = cache[i+1,colNumber].copy()
            cache[self.x-1,colNumber] = data.copy()
            return True
        


# In[5]:


class ImageWindow:
    window = None
    x = 0
    y = 0
    size = 0
    imageCache = None
    column = 0 
    def __init__(self,imageWindowX,imageWindowY,imageCache):
        if(imageWindowX > 0 and imageWindowY > 0):
            self.x = imageWindowX.copy()
            self.y = imageWindowY.copy()
            self.window = np.zeros([self.x,self.y])
            self.imageCache = imageCache
            self.size = self.x*self.y
    
    def initialize(self):
        for j in range(self.y):
                self.window[:,j] = self.imageCache.shift(column).copy()
                self.column = (self.column+1)%28
        return
    
    
    def shift(self):
        for j in range(self.y-1):
            self.window[:,j] = self.window[:,j+1].copy()
            
        self.window[:,self.y-1] = self.imageCache.shift(column).copy()
        self.column = (self.column+1)%28
        
        return

        
    
    


# In[6]:


class FilterWindow:
    memory = None
    address = None
    x = 0 #number of Rows
    y = 0
    size = 0
    window = None
    
    def __init__(self,filterWindowX,filterWindowY,address):
        if(imageWindowX > 0 and imageWindowY > 0):
            self.x = filterWindowX.copy()
            self.y = filterWindowX.copy()
            self.window = np.zeros([self.x,self.y])
            self.address = address.copy()
            self.size = self.x*self.y
        
    def initialize(self):
        for i in range(self.x):
            for j in range(self.y):
                while(!memory.acquire()): 
                    continue   
                self.window[i,j]= self.memory.read(address)
                address+=1
        memory.release()
        
    
    


# In[7]:


class ComputationUnit:
    imageWindow = None
    filterWindow = None
    result = 0
    latency = 0
    clk = 0
    
    def __init__(self,imageWindow,filterWindow,latency,clk):
        self.imageWindow = imageWindow
        self.filterWindow = filterWindow
        self.latency = latency.copy()
        self.clk = clk 
        
    def compute(self):
        tmp = 0
        self.result = np.sum(np.multiply(self.imageWindow,self.filterWindow))
        #waiting.
        while(tmp != latency):
            tmp += clk
        
        


# In[ ]:


class Controller:
    
    memory = None
    imageCache = None
    imageWindow = None
    filterWindow = None
    
    clk = 0
    
    stride = 0
    filterType = 0
    
    def __init__(self,imageCache,imageWindow,filterWindow,filterSize,filterType,stride,memory,clk):
        self.imageCache = imageCache
        self.imageWindow = imageWindow
        self.filterWindow = filterWindow
        self.memory = memory
        self.clk = clk
        self.filterType = filterType
        self.stride = stride
        

