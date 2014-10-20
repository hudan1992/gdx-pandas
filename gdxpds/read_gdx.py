
import gdxdict
import pandas as pds

import gdxpds.tools

import os

class Translator:
    def __init__(self, gdx_file, gams_dir = None):
        self._gdx_loader = gdxpds.tools.GdxLoader(gdx_file, gams_dir)
        
    @property
    def gams_dir(self):
        return self._gdx_loader.gams_dir
        
    @gams_dir.setter
    def gams_dir(self, value):
        self._gdx_loader.gams_dir = value
        
    @property 
    def gdx_file(self):
        return self._gdx_loader.gdx_file
        
    @gdx_file.setter
    def gdx_file(self, value):
        self._gdx_loader.gdx_file = value
        self._dataframes = None
        
    @property
    def gdx(self):
        return self._gdx_loader.gdx
        
    @property
    def dataframes(self):
        if self._dataframes is None:
            self._translate()
        return self._dataframes
                
    def _translate(self):    
        # recursive helper function
        def collect_data(data, entry, dim):
            assert isinstance(dim, gdxdict.gdxdim)
            for key, value in dim.items.items():
                if isinstance(value,gdxdict.gdxdim):
                    collect_data(data,entry + [key],value)
                else:
                    data.append(entry + [key, value])
        
        # main body        
        assert self._dataframes is None
        self._dataframes = {}
        for symbol_name in self.gdx:
            symbol_info = gdx.getinfo(symbol_name)
            if symbol_info['records'] > 0:
                cols = [d['key'] for d in symbol_info["domain"]]
                cols.append('value')
                data = []; entry = []
                collect_data(data,entry,self.gdx[symbol_name])
                self._dataframes[symbol_name] = pds.DataFrame(data = data, columns = cols)

def to_dataframes(gdx_file, gams_dir = None):
    """
    Parameters:
      - gdxfile (string): path to a gdx file
      - gamsdir (string): path to GAMS directory
      
    Returns a dict of Pandas DataFrames, one item for each symbol in the GDX 
    file, keyed with the symbol name.
    """
    return gdxpds.read_gdx.Translator(gdx_file, gams_dir).dataframes
    