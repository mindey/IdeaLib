import pandas as pd
import itertools
import datetime
import copy

class Idea():
    def __init__(self, plan={}):
        self.time_unit = datetime.timedelta(days=1)
        self.money_unit = 'LTL'
        self.start_time = datetime.datetime.today()
        if type(plan) in [str,unicode]:
            self.from_idl(plan)
        else:
            self.plan = plan
    def from_idl(self, text):
        self.__init__()
        ''' Converts a multiline string to self.plan list of tuples of dicts. '''
        result = []
        for i,line in enumerate(text.split('\n')):
            line = line.strip()
            first_whitespace = line.find(' ')
            line_to_dict =  lambda x: dict([attribute.strip().split(' ') for attribute in x.split(',')])
            if i % 2 == 0:
                domain = line[first_whitespace:].strip()
                if ' ' not in domain: # assume it is first one, the idea name
                    domain += ' 1'    # just so that line_to_dict would work.
            elif i % 2 == 1:
                codomain = line[first_whitespace:].strip()
                result.append((line_to_dict(domain),line_to_dict(codomain)))
        self.plan = result
    def __str__(self):
        return str(self.plan)
    def __repr__(self):
        self.view = ''
        for i, p in enumerate(self.plan):
            if i == 0: self.view += '' + str(p[0]) + '\n:  ' + str(p[1]) +'\n';
            if i > 0: self.view += '' + str(p[0]) + '\n-> ' + str(p[1]) +'\n';
        return self.view
    def _plan_convert_index_sets_to_dicts(self):
        for i, x in enumerate(self.plan):
            if type(self.plan[i][0]) == set:
                self.plan[i] = ({'action': ''.join(self.plan[i][0])}, self.plan[i][1])
    def _plan_values_to_lists(self):
        ''' Converts Plan Dictionary Values to Lists '''
        for i, x in enumerate(self.plan):
            for j, y in enumerate(self.plan[i]):
                for k, z in enumerate(self.plan[i][j]):
                    self.plan[i][j][z] = [self.plan[i][j][z]] if type(self.plan[i][j][z]) != list else self.plan[i][j][z]
    def scenario_mean_values(self):
        ''' Takes the means for value lists, to be used for mean scenario. '''
        p = copy.deepcopy(self.plan)
        for i,x in enumerate(p):
            for j, y in enumerate(p[i]):
                for k, z in enumerate(p[i][j]):
                    p[i][j][z] = sum(p[i][j][z])/len(p[i][j][z]) \
                    if type(self.plan[i][j][z][0]) in [int, float] \
                    else p[i][j][z][len(p[i][j][z])/2]
        self.p = p
        self.scenario = p
    def scenario_max_in_min_out(self):
        ''' This takes max values for the domain, and min values for codomain.'''
        p = copy.deepcopy(self.plan)
        for i,x in enumerate(p):
            for j, y in enumerate(p[i]):
                for k, z in enumerate(p[i][j]):
                    if j == 0: # max in
                        p[i][j][z] = max(p[i][j][z]) \
                        if type(self.plan[i][j][z][0]) in [int, float] \
                        else p[i][j][z][len(p[i][j][z])/2]
                    if j == 1: # min out
                        p[i][j][z] = min(p[i][j][z]) \
                        if type(self.plan[i][j][z][0]) in [int, float] \
                        else p[i][j][z][len(p[i][j][z])/2]
        self.p = p
        self.scenario = p
    def scenario_min_in_max_out(self):
        ''' This takes max values for the domain, and min values for codomain.'''
        p = copy.deepcopy(self.plan)
        for i,x in enumerate(p):
            for j, y in enumerate(p[i]):
                for k, z in enumerate(p[i][j]):
                    if j == 0: # min in
                        p[i][j][z] = min(p[i][j][z]) \
                        if type(self.plan[i][j][z][0]) in [int, float] \
                        else p[i][j][z][len(p[i][j][z])/2]
                    if j == 1: # max out
                        p[i][j][z] = max(p[i][j][z]) \
                        if type(self.plan[i][j][z][0]) in [int, float] \
                        else p[i][j][z][len(p[i][j][z])/2]
        self.p = p
        self.scenario = p
    def scenario_n(self,n=0):
        ''' This takes mean values for the domain, and nth values for codomain.'''
        p = copy.deepcopy(self.plan)
        for i,x in enumerate(p):
            for j, y in enumerate(p[i]):
                for k, z in enumerate(p[i][j]):
                    if j == 0: # domain
                        p[i][j][z] = sum(p[i][j][z])/len(p[i][j][z]) \
                        if type(self.plan[i][j][z][0]) in [int, float] \
                        else p[i][j][z][len(p[i][j][z])/2]
                    if j == 1: # codomain
                        p[i][j][z] = p[i][j][z][n] \
                        if len(self.plan[i][j][z])+1 >= n \
                        else p[i][j][z][min(n,len(p[i][j][z]-1))]
        self.p = p
        self.scenario = p        
    def _plan_add_dummy_index_keys(self):
        ''' Unifies the domain index. '''
        types, index, values = zip(*[[t[0].keys(),tuple(t[0].values()), t[1]] for l,t in enumerate(self.plan)])
        types = set(itertools.chain(*types))
        for i, x in enumerate(self.plan):
            absent_keys = types - set(self.plan[i][0].keys())
            self.plan[i] = (dict(self.plan[i][0], **dict(zip(absent_keys, [[0]]*(len(absent_keys))))), self.plan[i][1])
    def to_df(self, scenario='normal', dates=False, value=False, resample=False, fill=False, silent=False, convert='numeric'):
        ''' Converts a scenario to DataFrame. '''
        self._plan_convert_index_sets_to_dicts()
        self.u = self._plan_values_to_lists()
        self.v = self._plan_add_dummy_index_keys()
        if scenario == 'normal':
            self.scenario_mean_values()
        if scenario == 'best':
            self.scenario_min_in_max_out()
        if scenario == 'worst':
            self.scenario_max_in_min_out()
        if type(scenario) == int:
            self.scenario_n(scenario)
        types, index, values = zip(*[[t[0].keys(),tuple(t[0].values()), t[1]] for l,t in enumerate(self.p)])
        if len(set(itertools.chain(*types))) == 1: index = [i[0] for i in index]; # in the case of only 1 variable-index
        self.df = pd.DataFrame(dict(zip(index,values))).T.reindex(index).fillna(method='ffill').fillna(0)
        self.df.index.names = types[0]
        if convert == 'numeric':
            self.df = self.df.convert_objects(convert_numeric=True)
        if dates:
            df = self.df.reset_index()
            df['time'] = df['time'].convert_objects(convert_numeric=True).apply(lambda x: self.time_unit*int(x))
            df['date'] = self.start_time + df['time'].cumsum()
            self.df = df.set_index(self.df.index.names+['date'])
        if value:
            values = zip(self.df.columns, value) if type(value)==list and len(value)==len(self.df.columns) else zip(self.df.columns, len(self.df.columns)*[1])
            self.df['value'] = (self.df*zip(*values)[1]).sum(axis=1)
        if resample:
            if type(resample) in [str, unicode]:
                self.df = self.df.reset_index().set_index('date').resample(resample)
            else: # just some default resampling
                self.df = self.df.reset_index().set_index('date')
                duration = (self.df.index[-1]-self.df.index[0]).total_seconds()
                if 0 <= duration and duration <= 3600:
                    self.df.resample('1Min')
                if 3600 < duration and duration <= 86400:
                    self.df.resample('1H')
                if 86400 < duration and duration <= 432000:
                    self.df.resample('1D')
                if 432000 < duration and duration <= 12096000:
                    self.df.resample('1W')
                if 12096000 < duration and duration <= 47520000:
                    self.df.resample('1M')
                if 47520000 < duration:
                    self.df.resample('1A')
        if fill:
            if fill == 'interpolate':
                self.df = self.df.apply(pd.Series.interpolate)
            else:
                self.df = self.df.fillna(method='ffill')
        if not silent:
            return self.df
    def plot(self, scenario='normal', dates=True, value=True, resample=True, fill=True):
        self.to_df(scenario=scenario, dates=dates, value=value, resample=resample, fill=fill)['value'].plot()

class IdeaList(list):
    def _compute_data_frames(self):
        for i in range(list.__len__(self)):
            list.__getitem__(self, i).to_df(scenario='normal', dates=True, value=True, resample=True, fill=True, silent=True)
    def _compute_common_index(self):
        if not list.__len__(self) > 0:
            return False
        self.index = list.__getitem__(self,0).df.index
        for i in range(1,list.__len__(self)):
            self.index = self.index.union(list.__getitem__(self, i).df.index)
    def _reindex_data_frames(self):
        for i in range(list.__len__(self)):
            list.__getitem__(self, i).df = list.__getitem__(self, i).df.reindex(self.index)
    def align(self):
        self._compute_data_frames()
        self._compute_common_index()
        self._reindex_data_frames()
    def plot(self):
        self.align()
        for i in range(list.__len__(self)):
            list.__getitem__(self, i).df['value'].plot()
