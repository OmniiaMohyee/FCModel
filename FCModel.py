import numpy as np
from enum import Enum


class Memory:
    memory = None
    x = 0
    y = 0
    size = 0
    busy = False

    def __init__(self, x, y):
        if(x > 0 and y > 0):
            print(x, y)
            self.x = x.copy()
            self.y = y.copy()
            self.size = x * y
            self.memory = np.random.randint(0, 256, [x, y])  # np.zeros([x, y])

    def read(self, address):
        if(address >= self.size):
            print("Address out of Range!")
            return
        else:
            i = int(address / self.y)
            j = int(address % self.y)
            return self.memory[i][j]

    def write(self, address, data):
        if(self.busy):
            return
        if(address >= self.size):
            print("Address out of Range!")
            return
        else:
            i = int(address / self.y)
            j = int(address % self.y)
            self.memory[i][j] = data.copy()
            return

    def Print(self):
        for i in range(self.x):
            for j in range(self.y):
                print(self.memory[i][j])
        return

    def acquire(self):
        if (self.busy):
            return False
        self.busy = True
        return self.busy

    def release(self):
        self.busy = False
        return True


class ImageCache:
    cache = None
    memory = None
    address = None
    x = 0  # number of Rows
    y = 0  # number of Columns

    def __init__(self, cacheX, cacheY, mem, address):
        if(cacheX > 0 and cacheY > 0):
            self.x = cacheX.copy()
            self.y = cacheY.copy()
            self.cache = np.zeros([cacheX, cacheY])
            self.memory = mem
            self.address = address.copy()
            self.currentCol = 0

    def initialize(self):
        for i in range(self.cacheX):
            for j in range(self.cacheY):
                if (self.memory.acquire()):
                    self.cache[i][j] = self.memory.read(self.address)
                    self.address += 1
        self.memory.release()
        return

    def shift(self, col_number):
        if(col_number > self.y):
            return None
        return self.cache[:, col_number]

    def insert(self, col_number, data):
        if(col_number > self.y):
            return False
        else:
            for i in range(self.x - 1):
                self.cache[i, col_number] = self.cache[i + 1, col_number].copy()
            self.cache[self.x - 1, col_number] = data.copy()
            return True


class ImageWindow:
    window = None
    x = 0
    y = 0
    size = 0
    imageCache = None
    column = 0

    def __init__(self, imageWindowX, imageWindowY, imageCache):
        if(imageWindowX > 0 and imageWindowY > 0):
            self.x = imageWindowX.copy()
            self.y = imageWindowY.copy()
            self.window = np.zeros([self.x, self.y])
            self.imageCache = imageCache
            self.size = self.x * self.y

    def initialize(self):
        for j in range(self.y):
                self.window[:, j] = self.imageCache.shift(self.column).copy()
                self.column = (self.column + 1) % 28
        return

    def shift(self):
        for j in range(self.y - 1):
            self.window[:, j] = self.window[:, j + 1].copy()
        self.window[:, self.y - 1] = self.imageCache.shift(self.column).copy()
        self.column = (self.column + 1) % 28

        return


class FilterWindow:
    memory = None
    address = None
    x = 0  # number of Rows
    y = 0  # number of Columns
    size = 0
    window = None

    def __init__(self, filterWindowX, filterWindowY, address):
        if(filterWindowX > 0 and filterWindowY > 0):
            self.x = filterWindowX.copy()
            self.y = filterWindowX.copy()
            self.window = np.zeros([self.x, self.y])
            self.address = address.copy()
            self.size = self.x * self.y

    def initialize(self, start_offset):
        self.address += start_offset
        for i in range(self.x):
            for j in range(self.y):
                while(self.memory.acquire()):
                    continue
                self.window[i, j] = self.memory.read(self.address)
                self.address += 1
        self.memory.release()


class ComputationUnit:
    imageWindow = None
    filterWindow = None
    result = 0
    latency = 0
    clk = 0

    def __init__(self, imageWindow, filterWindow, latency, clk):
        self.imageWindow = imageWindow
        self.filterWindow = filterWindow
        self.latency = latency.copy()
        self.clk = clk

    def compute(self, relu, pool, prev_val):
        tmp = 0
        self.result = 0
        if pool:
            self.result = np.sum(self.imageWindow) / 32
        else:
            self.result = np.sum(np.multiply(self.imageWindow, self.filterWindow))
        if relu:
            self.result = np.max(self.result + prev_val, 0)
        else:
            self.result = self.result + prev_val
        # waiting.
        while(tmp != self.latency):
            tmp += self.clk


class ControllerState(Enum):
    InitCache = 0
    InitImageWindow = 1
    InitFilterWindow = 1
    FetchToCache = 2
    FetchToImageWindow = 3
    FetchToFilterWindow = 4
    DoConvolution = 5
    WriteToMemory = 6
    DoFC = 7


class Controller:
    memory = None
    image_cache = None
    image_window = None
    filter_window = None
    computation_unit = None
    clk = 0

    stride = 0
    filterType = 0
    relu = False
    pool = False
    prev_val = 0

    state = None
    next_state = None

    next_pixel_addr = 28 * 5
    current_column = 0

    next_write_addr = 64 * 64 / 2 - 28 * 28

    def __init__(self):
        self.state = ControllerState.InitCache
        self.next_state = ControllerState.InitCache

    def fetch_block_info(self):
        # should fetch this from memory instead.
        self.stride = 1
        self.filterType = 0
        self.relu = False
        self.pool = False
        self.previous_value = 0  # Important!!

    def main(self):
        memory = Memory(64, 64)
        image_cache = ImageCache(5, 28, memory, 0)
        image_window = ImageWindow(5, 5, image_cache)
        filter_window = FilterWindow(5, 5, 64 * 64 / 2)
        computation_unit = ComputationUnit(image_window, filter_window, 0, 0)
        done = False
        while not done:
            self.state = self.next_state
            if self.state == ControllerState.InitCache:
                image_cache.initialize()
                self.next_state = ControllerState.InitImageWindow
            elif self.state == ControllerState.InitImageWindow:
                image_window.initialize()
                self.next_state = ControllerState.InitFilterWindow
            elif self.state == ControllerState.InitFilterWindow:
                filter_window.initialize(0)
                self.next_state = ControllerState.DoConvolution
            elif self.state == ControllerState.DoConvolution:
                #  To-do: Fetch initial value / bias.
                #  To-do: Fetch layer information.
                self.fetch_block_info()
                computation_unit.compute(self.relu, self.pool, self.previous_value)
                # if ( current filter is done ) self.next_state = ControllerState.FetchToFilterWindow
                self.next_state = ControllerState.FetchToCache
            elif self.state == ControllerState.FetchToCache:
                new_pixel = memory.read(self.next_pixel_addr)
                image_cache.insert(self.current_column, new_pixel)
                self.current_column = self.current_column + 1
                self.next_state = ControllerState.FetchToFilterWindow
            elif self.state == ControllerState.FetchToFilterWindow:
                filter_window.initialize(4)
                self.next_state = ControllerState.FetchToImageWindow
            elif self.state == ControllerState.FetchToImageWindow:
                image_window.shift()
                self.next_state = ControllerState.WriteToMemory
            elif self.state == ControllerState.WriteToMemory:
                # to-do: fix next write address computation
                memory.write(self.next_write_addr, computation_unit.result)
                self.next_write_addr = self.next_write_addr - 1
                self.next_state = ControllerState.DoConvolution
            # to-do: check if we're done and break.
